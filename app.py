from flask import Flask, jsonify, request
from flask_cors import CORS
from pro_football_reference_web_scraper import team_game_log as t

app = Flask(__name__)
CORS(app)  # This enables cross-origin requests so that your GitHub Pages front end can access the backend

@app.route('/api/nfl_matchups', methods=['GET'])
def get_nfl_matchups():
    year = request.args.get('year', type=int)
    week = request.args.get('week', type=int)
    
    if not year or not week:
        return jsonify({"error": "Year and Week are required"}), 400

    # Example: Fetching data for a specific team, modify as needed
    team_name = "Kansas City Chiefs"
    try:
        game_log = t.get_team_game_log(team=team_name, season=year)
        
        # Log the DataFrame columns to verify structure
        app.logger.debug(f"Columns in game_log DataFrame: {game_log.columns}")
        
        # Update to match correct column names
        if 'Week' in game_log.columns:
            game_log_filtered = game_log[game_log['Week'] == week]
        elif 'week' in game_log.columns:
            game_log_filtered = game_log[game_log['week'] == week]
        else:
            return jsonify({"error": "Week column not found in game log data"}), 404

        games = game_log_filtered.to_dict(orient='records')
        return jsonify(games)
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
