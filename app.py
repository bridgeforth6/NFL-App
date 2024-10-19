from flask import Flask, jsonify, request
from flask_cors import CORS
from pro_football_reference_web_scraper import player_game_log as p
from pro_football_reference_web_scraper import team_game_log as t

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests so that your GitHub Pages front end can access the backend

# Endpoint to get player stats
@app.route('/api/player_game_log', methods=['GET'])
def get_player_game_log():
    player = request.args.get('player')
    position = request.args.get('position')
    season = request.args.get('season', type=int)

    if not player or not position or not season:
        return jsonify({"error": "Player, position, and season are required"}), 400

    try:
        # Get player game log using the scraper package
        game_log = p.get_player_game_log(player=player, position=position, season=season)
        game_log_dict = game_log.to_dict(orient='records')
        return jsonify(game_log_dict)
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Endpoint to get team stats
@app.route('/api/team_game_log', methods=['GET'])
def get_team_game_log():
    team = request.args.get('team')
    season = request.args.get('season', type=int)

    if not team or not season:
        return jsonify({"error": "Team and season are required"}), 400

    try:
        # Get team game log using the scraper package
        game_log = t.get_team_game_log(team=team, season=season)
        game_log_dict = game_log.to_dict(orient='records')
        return jsonify(game_log_dict)
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
