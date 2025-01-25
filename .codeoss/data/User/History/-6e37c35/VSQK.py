from langchain_core.tools import tool
#from search_stats import query_player_stats
#from search_google import google_search_query
#from search_injuries import query_player_injuries
#from model_predictions import war_prediction
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

# Existing tools...

@tool
def compare_players(prompt: str) -> str:
    """Compares a minor league player with major league players based on given statistics."""
    print("Comparing players")
    
    # Extract player name from the prompt
    minor_player_name = get_player_names(prompt)
    
    # Queries to fetch data
    minor_query = f"SELECT *, Relinquished as Name, ` SO` as SO, ` BK` as BK FROM `theta-shuttle-446821-i9.mlb.milb_testing_data`"
    major_query = f"SELECT Name, Age as currentAge, ERA, WHIP, SO, BK FROM `theta-shuttle-446821-i9.mlb.mlb_comparison_stats_2024` WHERE Name != '{minor_player_name}'"

    # Load data
    minor_df = get_data_from_bigquery(minor_query)
    major_df = get_data_from_bigquery(major_query)

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
        
        return f"The closest major player to {minor_player_name} is {closest_major_player} with a similarity score of {similarities[closest_major_idx]:.4f}."

    # Perform the comparison
    result = find_best_match(minor_player_name)
    return result

# Example usage in main
if __name__ == "__main__":
    player_name = "Paul Skenes"
    print(compare_players(player_name))
    # print(normal_responder("Who is the best MLB player currently?"))