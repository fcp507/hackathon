from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from config import PROJECT_ID, GOOGLE_MODEL_ID, GOOGLE_API_KEY
from utils.prompt import sys_instruction
from utils.help_function import get_player_names
from typing import List
import json
import re
import io

# Variables
# Client initialization
client = genai.Client(api_key=GOOGLE_API_KEY)

# Configuration for generating content
config = GenerateContentConfig(system_instruction=sys_instruction, tools=[Tool(google_search=GoogleSearch())], temperature=0)

def clean_html(raw_html):
    """Function to remove HTML tags from text."""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def google_search_query(player_name: str):
    print("google_search_query", player_name)
    prompt = f"Generate a scouting report for the minor league player {player_name}."

    try:
        # If user selects web search, redefine the tool and generate response with web search
        google_search_tool = Tool(google_search=GoogleSearch())
        response_stream = client.models.generate_content_stream(
            model=GOOGLE_MODEL_ID,
            contents=[prompt],
            config=GenerateContentConfig(
                system_instruction=sys_instruction,
                tools=[google_search_tool],
                temperature=0
            ),
        )

        report = io.StringIO()
        for chunk in response_stream:
            candidate = chunk.candidates[0]
            for part in candidate.content.parts:
                if part.text:
                    cleaned_text = clean_html(part.text)
                    report.write(cleaned_text)
                else:
                    print(json.dumps(part.model_dump(exclude_none=True), indent=2))

        scouting_report = report.getvalue().strip()
        if not scouting_report:
            print("No content was generated in the scouting report.")
        return scouting_report

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    player_name = "Jackson Jobe"
    scouting_report = google_search_query(player_name)
    if scouting_report:
        print("Scouting Report:")
        print(scouting_report)
    else:
        print("Failed to generate scouting report.")