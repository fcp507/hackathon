from google.cloud import bigquery
from vertexai.generative_models import GenerativeModel
from config import PROJECT_ID, BIGQUERY_DATASET_ID
from utils.prompt import injuries_prompt
from utils.help_function import get_player_names

# Initialize the Gemini Thinking model
sql_generator_model = GenerativeModel(
    'gemini-1.5-pro',
    generation_config={"temperature": 0, "max_output_tokens": 2048}
)

# Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)

def query_player_injuries(prompt):
    """
    Queries BigQuery for player injury history based on a given prompt.

    Args:
        prompt (str): The user's question regarding player injuries.

    Returns:
        str: A natural language response based on the query results.
    """
    user_question = prompt
    revised_prompt = (
        f"Use these System Instructions: {injuries_prompt} "
        f"to answer the provided Question about {user_question}"
    )
    
    print(revised_prompt)
    
    generated_query = sql_generator_model.generate_content(revised_prompt)
    print(generated_query.text)
    
    job_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)  # Adjust as needed
    
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
    
    # Convert API response to a string representation
    api_response = str([dict(row) for row in api_response])
    api_response = api_response.replace("\\", "").replace("\n", "")
    
    print(api_response)
    
    return_prompt = (
        f"""Please provide a detailed summary and analysis of minor mlb player '{user_question}' injury history and discuss how these injuries might impact his future performance and career prospects. 
        Highlight key aspects such as the type and frequency of injuries based on '{api_response}'"""
    )
    
    response = sql_generator_model.generate_content(return_prompt)
    print(response.text)
    
    return response.text

# Example usage
if __name__ == "__main__":
    user_question = "Thomas White"
    response = query_player_injuries(user_question)
    print(response)