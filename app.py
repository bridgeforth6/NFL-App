from flask import Flask, jsonify, request
from flask_cors import CORS
from pro_football_reference_web_scraper import team_game_log as t

app = Flask(__name__)
CORS(app)

@app.route('/api/nfl_matchups', methods=['GET'])
def get_nfl_matchups():
    year = request.args.get('year', type=int)
    week = request.args.get('week', type=int)
    
    if not year or not week:
        return jsonify({"error": "Year and Week are required"}), 400

    # Example: Only fetching for one team, modify as needed
    team_name = "Kansas City Chiefs"
    game_log = t.get_team_game_log(team=team_name, season=year)
    game_log_filtered = game_log[game_log['Week'] == week]
    games = game_log_filtered.to_dict(orient='records')
    return jsonify(games)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
