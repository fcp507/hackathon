from google.cloud import bigquery
import logging
from google.cloud import bigquery_storage

import pandas as pd

# Initialize a BigQuery client
bqstorageclient = bigquery_storage.BigQueryReadClient()
client = bigquery.Client(project="hackathon-448821")


def fetch_distinct_names():
    query = """
    SELECT DISTINCT name
    FROM `hackathon-448821.mlb.pitching_stats_2024`
    WHERE name IS NOT Null
    ORDER BY name
    """
    
    try:
        query_job = client.query(query)
        results = query_job.result()
    except Exception as e:
        logging.error(f"An error occurred during the query: {e}")
        return []

    names = [row.name for row in results]
    #logging.info(f"Fetched names: {names}")
    return names

def fetch_player_stats(name):
    # Use parameterized queries to prevent SQL injection
    query = """
    SELECT PlayerId, Sport_id, 
        currentAge,
        height,
        weight,
        draftYear,
        strikeZoneTop,
        strikeZoneBottom,
        W,
        L,
        G,
        GS,
        GF,
        CG,
        QS,
        SHO,
        SVO,
        SV,
        HLD,
        BS,
        IP_str,
        IP,
        BF,
        AB,
        R,
        H,
        `2B` as Double_B,
        `3B` as Triple_B,
        R2,
        ER,
        HR,
        TB,
        BB,
        IBB,
        SO,
        HBP,
        BK,
        GiDP,
        GiDP_opp,
        CI,
        IR,
        IRS,
        BqR,
        BqRS,
        RS,
        SF,
        SB,
        CS,
        PK,
        FH,
        PH,
        LH,
        FO,
        GO,
        AO,
        pop_outs,
        line_outs,
        PI,
        total_swings,
        swing_and_misses,
        balls_in_play,
        PI_strikes,
        PI_balls,
        WP,
        `W%` W_perc, -- Changed SO% to W_perc to avoid issues with special characters
        ERA,
        RA9,
        WHIP,
        H_9,
        HR_9,
        BB_9,
        SO_9,
        BABiP,
        SO_BB,
        BA,
        OBP,
        SLG,
        `SO%` SO_perc, -- Changed SO% to SO_perc to avoid issues with special characters
        BB_SO,
        PI_PA,
        HR_PA,
        BB_PA,
        PI_IP,
        Injury_Count,
        Total_DL_Length,
        Average_DL_Length 
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



def fetch_player_injuries(name):
    # Use parameterized queries to prevent SQL injection
    query = """
    SELECT  Relinquished, Injury_Count,
            Total_DL_Length,
            Average_DL_Length 
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

    injuries = [dict(row) for row in results]
    logging.info(f"Fetched stats for {name}: {stats}")
    return injuries


def war_prediction(player_name):
    # Define the SQL query with placeholders for the input parameters
    query = f"""
    SELECT * FROM ML.PREDICT(
        MODEL `mlb.prospect_prediction` ,
        (select `SO%` as SO_Percent,
    `W%` as W_Percent,
    `2B` as Double_B,
    `3B` as Triple_B,
    IFNULL(Injury_Count, 0) AS InjuryCount,
    IFNULL(Total_DL_Length, 0) AS Tot_DL_Length,
    IFNULL(Average_DL_Length, 0) AS Avg_DL_Length,
    * except(PlayerId, Relinquished, birthDate, draftYear, `2B`, `3B`, `SO%`, `W%`, Injury_Count, Total_DL_Length, Average_DL_Length) 
    from `hackathon-448821.mlb.milb_testing_data` where Relinquished =  '{player_name}' )
    )
    """
    # Execute the query
    query_job = client.query(query)
    
    # Convert the result to a pandas DataFrame
    df = query_job.to_dataframe(bqstorage_client=bqstorageclient)
    print(f"Query result:\n{df}")
    # Return the probability of prediction 1
    if not df.empty:
        # Assuming the column containing the prediction probabilities is named 'predicted_Flg_probs'
        if 'predicted_Flg_probs' in df.columns:
            predicted_probs = df['predicted_Flg_probs'].iloc[0]
            for prob in predicted_probs:
                if prob['label'] == 1:
                    return f"{prob['prob']:.2f}"
            raise KeyError("Probability for label '1' not found in the prediction results.")
        else:
            raise KeyError("Column 'predicted_Flg_probs' not found in the prediction results.")
    else:
        return None