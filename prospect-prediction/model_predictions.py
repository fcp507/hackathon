from google.cloud import bigquery
import pandas as pd

# Initialize a BigQuery client
client = bigquery.Client()


def war_prediction(player_name):
    # Define the SQL query with placeholders for the input parameters
    query = f"""
    SELECT * FROM ML.PREDICT(
        MODEL `mlb.prospect_prediction` ,
        (select   `SO%` as SO_Percent,
    `W%` as W_Percent,
    `2B` as Double_B,
    `3B` as Triple_B,
    IFNULL(Injury_Count, 0) AS InjuryCount,
    IFNULL(Total_DL_Length, 0) AS Tot_DL_Length,
    IFNULL(Average_DL_Length, 0) AS Avg_DL_Length,
    * except(PlayerId, Relinquished, birthDate, draftYear, `2B`, `3B`, `SO%`, `W%`, Injury_Count, Total_DL_Length, Average_DL_Length) 
    from `mlb.milb_testing_data` where Relinquished =  '{player_name}' )
    )
    """
    
    # Execute the query
    query_job = client.query(query)
    
    # Convert the result to a pandas DataFrame
    df = query_job.to_dataframe()
    
    # Return the probability of prediction 1
    if not df.empty:
        # Assuming the column containing the prediction probabilities is named 'predicted_Flg_probs'
        if 'predicted_Flg_probs' in df.columns:
            predicted_probs = df['predicted_Flg_probs'].iloc[0]
            for prob in predicted_probs:
                if prob['label'] == 1:
                    return prob['prob']
            raise KeyError("Probability for label '1' not found in the prediction results.")
        else:
            raise KeyError("Column 'predicted_Flg_probs' not found in the prediction results.")
    else:
        return None


player_name = "Jackson Jobe"
mode_result = war_prediction(player_name)
print(f"The mode(s) of the dataset is/are: {mode_result}")
