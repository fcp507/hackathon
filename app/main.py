from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from services.bigquery_client import fetch_distinct_names, fetch_player_stats
from services.player_comparision import compare_players
from urllib.parse import unquote

import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/v1/players", methods=["GET"])
def get_data():
    try:
        names = fetch_distinct_names()
        return jsonify(names=names)
    except Exception as e:
        logging.error(f"Error fetching player names: {e}")
        return jsonify(error=str(e)), 500

@app.route("/api/v1/player-stats/<player_name>", methods=["GET"])
def get_player_stats(player_name):
    if not player_name:
        return jsonify(error="Player name is required"), 400

    try:
        # Decode the player name using urllib.parse.unquote
        player_name = unquote(player_name)

        stats = fetch_player_stats(player_name)
        if stats:
            # Assuming stats is a list of dictionaries
            for stat in stats:
                player_id = stat.get('PlayerId')
                if player_id:
                    player_current_headshot_url = f'https://securea.mlb.com/mlb/images/players/head_shot/{player_id}.jpg'
                    stat['headshot_url'] = player_current_headshot_url
                else:
                    logging.warning(f"No PlayerId found for player {player_name}")

            return jsonify(stats=stats)
        else:
            return jsonify(error="No stats found for player"), 404
    except Exception as e:
        logging.error(f"Error fetching stats for player {player_name}: {e}")
        return jsonify(error=str(e)), 500


@app.route("/api/v1/compare-players/<playername>", methods=["GET"])
def compare_players_api(playername):
    if not playername:
        return jsonify(error="Player name is required"), 400

    try:
        # Decode player name
        playername = unquote(playername)
        playername = playername.replace('%20', ' ')  # Replace URL-encoded spaces with actual spaces
        print(f"Comparing player: {playername}")  # Debugging log
        result = compare_players(playername)
        return jsonify(result=result)
    except Exception as e:
        logging.error(f"Error comparing players: {e}")
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)