import json

with open("Software/Server/server.py", "r") as f:
    content = f.read()

# Add game settings at the top
if "game_settings =" not in content:
    content = content.replace("RESPAWN_TIMER = 10  # seconds", "RESPAWN_TIMER = 10  # seconds\n\ngame_settings = {\n    \"max_players\": 8,\n    \"max_teams\": 2,\n    \"max_per_team\": 4\n}\n")

# Update broadcast state
if "\"settings\": game_settings" not in content:
    old_payload = '''    state_payload = {
        "type": "STATE_SYNC",
        "players": players_state,
        "team_scores": team_scores
    }'''
    new_payload = '''    state_payload = {
        "type": "STATE_SYNC",
        "settings": game_settings,
        "players": players_state,
        "team_scores": team_scores
    }'''
    content = content.replace(old_payload, new_payload)

with open("Software/Server/server.py", "w") as f:
    f.write(content)

with open("Software/WebClient/admin.html", "r") as f:
    html = f.read()

# Update admin.html to listen for STATE_SYNC instead of STATE_UPDATE
html = html.replace("data.type === \"STATE_UPDATE\"", "data.type === \"STATE_SYNC\"")

with open("Software/WebClient/admin.html", "w") as f:
    f.write(html)
