from google.cloud import bigquery

from google.cloud import bigquery
import logging

def fetch_distinct_names():
    client = bigquery.Client(project="hackathon-448821")
    query = """
    SELECT DISTINCT name
    FROM `hackathon-448821.mlb.pitching_stats_2024`
    WHERE name IS NOT NULL
    ORDER BY name
    """
    
    try:
        query_job = client.query(query)
        results = query_job.result()
    except Exception as e:
        logging.error(f"An error occurred during the query: {e}")
        return []

    names = [row.name for row in results]
    logging.info(f"Fetched names: {names}")
    return names

def fetch_player_stats(name):
    client = bigquery.Client(project="hackathon-448821")
    # Use parameterized queries to prevent SQL injection
    query = """
    SELECT *
    FROM `hackathon-448821.mlb.milb_testing_data`
    WHERE Relinquished = @name
    """
    
    try:
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("name", "STRING", name)
            ]
        )
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
    except Exception as e:
        logging.error(f"An error occurred during the query: {e}")
        return []

    stats = [dict(row) for row in results]
    logging.info(f"Fetched stats for {name}: {stats}")
    return stats