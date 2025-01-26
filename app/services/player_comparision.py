from langchain_core.tools import tool
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from google.cloud import bigquery

# Initialize a BigQuery client
client = bigquery.Client()

# Function to get data from BigQuery
def get_data_from_bigquery(query, params=None):
    if params:
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        query_job = client.query(query, job_config=job_config)
    else:
        query_job = client.query(query)
    return query_job.to_dataframe()


def compare_players(prompt: str) -> str:
    """Compares a minor league player with major league players based on given statistics."""
    print("Comparing players")
    
    minor_player_name_list = prompt
    
    # Ensure 'minor_player_name' is a string
    if isinstance(minor_player_name_list, list):
        if len(minor_player_name_list) > 0:
            minor_player_name = minor_player_name_list[0]
        else:
            return "No player name found in the input."
    else:
        minor_player_name = minor_player_name_list

    # Queries to fetch data
    minor_query = """
    SELECT *, Relinquished as Name  
    FROM `hackathon-448821.mlb.milb_testing_data`
    """
    
    major_query = """
    SELECT Name, Age as currentAge, ERA, WHIP, SO, BK
    FROM `hackathon-448821.mlb.mlb_comparison_stats_2024`
    WHERE Name != @minor_player_name
    """
    
    # Parameters for the query
    query_params = [
        bigquery.ScalarQueryParameter("minor_player_name", "STRING", minor_player_name)
    ]

    # Load data
    minor_df = get_data_from_bigquery(minor_query)
    major_df = get_data_from_bigquery(major_query, query_params)

    # Ensure 'Name' column is a string
    minor_df['Name'] = minor_df['Name'].astype(str)

    # Debugging: print out some data
    print(minor_df.head())
    print("Looking for minor player:", minor_player_name)
    
    # Normalize function with error handling for non-numeric data
    def normalize(df, columns):
        df_normalized = df.copy()
        for col in columns:
            df_normalized[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, set errors to NaN
        df_normalized[columns] = (df_normalized[columns] - df_normalized[columns].min()) / (df_normalized[columns].max() - df_normalized[columns].min())
        return df_normalized

    # Columns to normalize
    columns_to_normalize = ['currentAge', 'ERA', 'WHIP', 'SO', 'BK']

    # Normalize the relevant columns
    minor_normalized = normalize(minor_df, columns_to_normalize)
    major_normalized = normalize(major_df, columns_to_normalize)

    # Function to calculate cosine similarity
    def calculate_similarity(minor_player, major_df):
        # Ensure minor_player is a 1D array
        minor_player_values = minor_player[columns_to_normalize].values.reshape(1, -1)
        
        # Calculate cosine similarities
        similarities = cosine_similarity(major_df[columns_to_normalize].values, minor_player_values)
        
        return similarities.flatten()

    # Find the closest major player for a given minor player name
    def find_best_match(minor_player_name):
        # Ensure minor_player_name is a string
        minor_player_name = str(minor_player_name)

        # Filter the minor player's DataFrame
        minor_player_df = minor_normalized[minor_normalized['Name'] == minor_player_name]
        
        # Check if the DataFrame is empty
        if minor_player_df.empty:
            return f"Minor player '{minor_player_name}' not found in the dataset."
        
        minor_player = minor_player_df.iloc[0]
        
        # Calculate similarities
        similarities = calculate_similarity(minor_player, major_normalized)
        
        # Find the closest major player
        closest_major_idx = similarities.argmax()  # Using argmax to find the index
        closest_major_player = major_df.loc[closest_major_idx, 'Name']
        
        # Retrieve all metrics for the closest player
        closest_player_metrics = major_df.loc[closest_major_idx, columns_to_normalize].to_dict()
        
        # Retrieve all metrics for the minor player
        minor_player_metrics = minor_df.loc[minor_df['Name'] == minor_player_name, columns_to_normalize].iloc[0].to_dict()
        
        return {
            "minor_player": minor_player_name,
            "minor_player_metrics": minor_player_metrics,
            "closest_major_player": closest_major_player,
            "similarity_score": similarities[closest_major_idx],
            "closest_major_player_metrics": closest_player_metrics
        }
 
    # Perform the comparison
    result = find_best_match(minor_player_name)
    return result

