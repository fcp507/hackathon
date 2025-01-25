from google.cloud import bigquery
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
from config import PROJECT_ID, BIGQUERY_DATASET_ID

from utils.prompt import injuries_prompt
from utils.help_function import get_player_names

# Initialize the Gemini Thinking model

sqlGeneratorModel = GenerativeModel('gemini-1.5-pro',generation_config={"temperature": 0, "max_output_tokens": 2048},)

# Initialize BigQuery client

client = bigquery.Client(project=PROJECT_ID)

def query_player_injuries(prompt):
    user_question = prompt
    revised_prompt = "Use these System Instructions: " + injuries_prompt + " to answer the provided Question: " + user_question
    print(revised_prompt)
    generated_query = sqlGeneratorModel.generate_content(revised_prompt)
    print(generated_query.text)
    job_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10) # Adjust maximum bytes billed as needed

    cleaned_query = (
    generated_query.text
    .replace("\\n", " ")
    .replace("\n", "")
    .replace("\\", "")
    .replace("```sql", "")
    )
    print(cleaned_query)

    query_job = client.query(cleaned_query, job_config=job_config)

    api_response = query_job.result()

    api_response = str([dict(row) for row in api_response])

    api_response = api_response.replace("\\", "").replace("\n", "")

    print(api_response)

    return_prompt = f"""Generate a natural language response based on the original question: '{user_question}' and the returned results: '{api_response}'"""

    response = sqlGeneratorModel.generate_content(return_prompt)

    print(response.text)

    return response.text

# # Example usage

# if __name__ == "__main__":

# user_question = "What are the injury history for player Thomas White?"

# response = query_player_injuriess(user_question)

# print(response)

