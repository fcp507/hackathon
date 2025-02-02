import re
import json
from langchain.prompts import PromptTemplate
from langchain_google_vertexai import ChatVertexAI
from langchain.schema import AIMessage

LLM_MODEL = 'gemini-1.5-flash'
llm = ChatVertexAI(model_name=LLM_MODEL, temperature=0)

def get_player_names(prompt: str) -> list:
    """Uses LLM to extract player names from the given text."""
 
    prompt_template = """
    Extract the player names from the given text. If no player names are found, return an empty list in valid JSON format.
 
    Example 1:
    Text: "Tell me about LeBron James and Kevin Durant."
    Players: ["LeBron James", "Kevin Durant"]
 
    Example 2:
    Text: "What about Lionel Messi, Cristiano Ronaldo, and Neymar?"
    Players: ["Lionel Messi", "Cristiano Ronaldo", "Neymar"]
 
    Example 3:
    Text: "I want to know about Roger Federer and Serena Williams."
    Players: ["Roger Federer", "Serena Williams"]
 
    Example 4:
    Text: "No players mentioned."
    Players: []
 
    Return ONLY the valid JSON string representing the list of player names. Do not include any other text or formatting like code blocks.
 
    Text: "{text}"
    Players:
    """
 
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    llm_output = llm.invoke(PROMPT.format(text=prompt))
 
    try:
        if isinstance(llm_output, AIMessage):
            llm_text = llm_output.content
        else:
            llm_text = str(llm_output)
 
        # More robust JSON extraction using regex
        match = re.search(r"\[.*\]", llm_text, re.DOTALL)  # Find JSON array using regex
        if match:
            json_string = match.group(0)
            players = json.loads(json_string)
            if isinstance(players, list):
                return [player for player in players]
            else:
                print(f"LLM did not return a list: {llm_text}")
                return []
        else:
            print(f"No JSON found in LLM output: {llm_text}")
            return []
 
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}. Full LLM Output: {llm_text}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# Example usage
prompt = "Tell me about Michael Jordan and Kobe Bryant."
player_names = get_player_names(prompt)
print(player_names)