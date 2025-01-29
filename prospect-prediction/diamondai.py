import chainlit as cl
import operator
import asyncio
import websockets
import re
from google.cloud import bigquery
from typing import Annotated, List, Tuple, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph, START
from tools import (
    stats_analyser,
    injuries_analyser,
    advanced_stats_analyser,
    normal_responder,
    model_prediction,
    player_comparision
)

# --- Configuration and Constants ---
LLM_MODEL = 'gemini-2.0-flash-exp'
AGENT_PROMPT = """
You are a professional MLB prospect prediction agent. You have access to historical stats data, injury data, scouting reports,
and advanced prediction models to assess the potential success of MLB prospects. You are NOT an LLM or AI chatbot.
Help to execute the task that you are assigned to, and return the response in a clear and concise manner.
The user is interested in predicting the success of prospects based on available data.
Provide comprehensive analysis and recommendations based on the information gathered.
"""

# --- LLM and Tools ---
llm = ChatVertexAI(model_name=LLM_MODEL, temperature=0)
tools = [
    stats_analyser, injuries_analyser, advanced_stats_analyser, 
    model_prediction, player_comparision, normal_responder
]
agent_executor = create_react_agent(llm, tools, state_modifier=AGENT_PROMPT)

# --- Data Models ---
class Plan(BaseModel):
    """Plan to follow."""
    steps: List[str] = Field(description="Steps to follow, in order.")

class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple[str, str]], operator.add]
    response: Optional[str]
    intermediate_responses: List[str]

class Response(BaseModel):
    """Response to user."""
    response: str

class Act(BaseModel):
    """Action to perform (for replanning)."""
    response: Optional[Response] = None
    plan: Optional[Plan] = None

# --- Prompts ---
PLANNER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", rf"""You are a professional MLB prospect prediction agent.
    Your role is to deliver a thorough analysis of MLB prospects based on available data,
    focusing on strengths and potential. Follow these guidelines:
    
    - **Objective Understanding**: Interpret the user's inquiry accurately to form a relevant response.
    - **Plan Creation**: Develop a logical plan with distinct steps, using the appropriate tools for each task:
    - **Player Data**: Utilize {stats_analyser} for retrieving player statistics.
    - **Injury Analysis**: Apply {injuries_analyser} to assess injury histories when data is available.
    - **Performance Insights**: Use {advanced_stats_analyser} to evaluate player abilities.
    - **Player Comparison**: Leverage {player_comparision} for comparing prospects.
    - **Prediction Modeling**: Implement {model_prediction} for predicting player outcomes, including selection probability.
    - **General Queries**: Use {normal_responder} for non-specific MLB questions.
    - **Handling Missing Injury Data**: If injury history data is not available, interpret this as a positive indicator that there are no major recorded injuries, suggesting a potentially good future for the player. Highlight other strengths and metrics such as WAR to complement this positive outlook.
    - **Presentation of Basic Stats**: When providing basic statistical outputs, format them into a table for clarity. Include key metrics such as batting average, ERA, WAR, etc., to present a clear and concise statistical overview.
    - **Prediction of Selection Probability**: Combine all available data, including performance metrics, comparisons,
    and qualitative insights, to provide an informed prediction of the player's probability of being picked for MLB.
    Even if exact probabilities cannot be calculated, provide a qualitative assessment based on available data.
    
    - **Example**:
    - **Question**: Predict the future performance of Shohei Ohtani.
    - **Plan**:
        1. Gather latest statistics using {stats_analyser}.
        2. Analyze available injury data with {injuries_analyser}, if present; if not, note the absence of major injuries as a positive sign.
        3. Assess performance with {advanced_stats_analyser}, emphasizing WAR or other strengths.
        4. Compare with similar players using {player_comparision}.
        5. Predict selection probability using {model_prediction}, incorporating insights from all previous steps.
        6. Synthesize insights for a comprehensive prediction, focusing on strengths and available data.
        7. Provide an overall score for the player on a scale from 1 to 10, considering all the above metrics and assessments.
    Ensure that each step contributes towards a well-rounded analysis. The final output should be clear, informative, 
    and positive, emphasizing the potential and strengths of the prospect."""), 
    ("placeholder", "{messages}"),
])


REPLANNER_PROMPT = ChatPromptTemplate.from_template(
    """Create a step-by-step plan for the given objective.
    Each step should be a distinct task. The final step's result should be the final answer. Do not skip steps.
    Your objective:
    {input}
    Your original plan:
    {plan}
    Completed steps:
    {past_steps}
    Update the plan. Include only the steps that still NEED to be done, incorporating data from previous steps. Do NOT include previously completed steps."""
)

# --- Chains and Agents ---
planner = PLANNER_PROMPT | llm.with_structured_output(Plan)
replanner = REPLANNER_PROMPT | llm.with_structured_output(Act)

# --- Misc ---
def clean_newlines(text: str) -> str:
    """Removes extra newline characters from a string."""
    return text.replace("\n\n", "\n")

def clean_step_description(step: str) -> str:
    """Cleans the step description to remove unwanted parts."""
    pattern = r"(args_schema=<[^>]+>\s*|func=<[^>]+>\s*|tool\.)"
    cleaned_step = re.sub(pattern, "", step).strip()
    return cleaned_step

# --- Workflow Nodes ---
async def plan_step(state: PlanExecute):
    plan = await planner.ainvoke({"messages": [("user", state["input"])]})
    with cl.Step(name="Generated Plan"):
        await cl.Message(content="**Generated Plan:**").send()
        for step in plan.steps:
            clean_step = clean_step_description(step)
            await cl.Message(content=f" {clean_step}").send()
    return {"plan": plan.steps, "intermediate_responses": []}

async def execute_step(state: PlanExecute):
    plan = state["plan"]
    if not plan:
        return {"response": "No more steps in the plan."}

    task = plan[0]
    clean_task = clean_step_description(task)
    print(f"Executing task: {task}")  # Debug output

    try:
        agent_response = await agent_executor.ainvoke({"messages": [("user", task)]})
        final_response = agent_response["messages"][-1].content
        print(f"Response from agent: {final_response}")  # Debug output

        if final_response:
            await cl.Message(content=final_response).send()
        else:
            print("No response content returned from function execution.")  # Log if empty
    except Exception as e:
        print(f"Error executing task {task}: {e}")  # Error logging
        final_response = f"Error executing task {task}: {e}"

    return {
        "past_steps": state.get("past_steps", []) + [(task, final_response)],
        "plan": plan[1:],
        "intermediate_responses": state.get("intermediate_responses", []) + [final_response]
    }

async def replan_step(state: PlanExecute):
    all_responses = "\n".join(state["intermediate_responses"])
    all_steps = "\n".join([f"{step}: {response}" for step, response in state["past_steps"]])
    context = f"Here is the information gathered from the previous steps:\n{all_steps}\n\nHere are the direct responses from the tools:\n{all_responses}"

    output = await replanner.ainvoke({**state, "input": context})
    if output.response:
        cleaned_response = clean_newlines(output.response.response)
        with cl.Step(name="Final Response"):
            await cl.Message(content="**Final Response:**").send()
            await cl.Message(content=cleaned_response).send()
        return {"response": cleaned_response}
    else:
        return {"plan": output.plan.steps}

def should_end(state: PlanExecute):
    return END if "response" in state and state["response"] is not None else "agent"

# --- Workflow Definition ---
workflow = StateGraph(PlanExecute)
workflow.add_node("planner", plan_step)
workflow.add_node("agent", execute_step)
workflow.add_node("replan", replan_step)
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "agent")
workflow.add_edge("agent", "replan")
workflow.add_conditional_edges("replan", should_end, {"agent": "agent", END: END})
app = workflow.compile()

# --- Chainlit Interface ---
@cl.on_chat_start
async def start():
    await cl.Message(content="Hello! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    config = {"recursion_limit": 50}
    async for event in app.astream(
        {"input": message.content, "plan": [], "past_steps": [], "response": None, "intermediate_responses": []},
        config=config,
    ):
        if "response" in event:
            pass
        elif "plan" in event:
            pass
        elif "past_steps" in event:
            pass

