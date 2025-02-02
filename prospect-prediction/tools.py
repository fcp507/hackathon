from langchain_core.tools import tool
from search_stats import query_player_stats
from search_google import google_search_query
from search_injuries import query_player_injuries
from model_predictions import war_prediction
from player_compariosn import compare_players
from langchain.prompts import PromptTemplate
from langchain_google_vertexai import ChatVertexAI
from langchain.schema import AIMessage
import os
import json
import re

from utils.help_function import get_player_names

@tool
def stats_analyser(prompt: str) -> str:
    """Fetches player statistics based on the given prompt."""
    print("Fetching player statistics")
    player_stats = query_player_stats(prompt)

    if not player_stats:
        return "No statistics found for the given player."
    
    return json.dumps(player_stats, indent=4)

@tool
def injuries_analyser(prompt: str) -> str:
    """Fetches player injury history based on the given prompt."""
    print("Fetching player injury history")
    player_name = get_player_names(prompt)[0]
    injuries = query_player_injuries(player_name)

    if not injuries:
        return "No Injuries found for the given player."
    
    return injuries

@tool
def model_prediction(prompt: str) -> str:
    """Predict player picked probability"""
    player_name = get_player_names(prompt)[0]
    print(player_name)
    results = war_prediction(player_name)
    if results < 0.5:
        return "Model Prediction : Major league pick probability is low"
    else:
        return "Model Prediction : Major league pick probability is high"

@tool
def advanced_stats_analyser(prompt: str) -> str:
    """Analyzes player performance trends."""
    print("Analyzing player performance")
    player_name = get_player_names(prompt)
    print(player_name)
    search_results = google_search_query(player_name)
    print(search_results)

    return search_results 

@tool
def normal_responder(qns: str) -> str:
    """Answer normal Question/Generic Question (e.g. Hi or who are you?)"""
    print("Using Normal Responder tool now")
    prompt_template = f"""You are a seasoned baseball analyst.
        Your goal is to help answer the user's question: {qns} with comprehensive analysis based on what you have been trained on, or knowledge from Google Search or internal proprietary research.
        You need to return a response that explains how you came up with that answer, backed by evidence that you used in coming up with the answer.
        The user is an MLB enthusiast looking for detailed insights into player performance and future potential.
        """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    llm_output = llm.invoke(PROMPT.format(text=qns))
    return llm_output.content

@tool
def player_comparision(prompt: str) -> str:
    """Compares players based on the prompt."""
    print("player_comparison")
    results = compare_players(prompt)
    return results

# Example usage
if __name__ == "__main__":
    player_name = "Tell me more about Jaden Hill"
    print(model_prediction(player_name))
    # print(normal_responder("Who is the best MLB player currently?"))