import json

with open("Software/Server/server.py", "r") as f:
    content = f.read()

# Add game settings if not present
if "game_settings =" not in content:
    content = content.replace("connected_clients = {}  # UUID -> WebSocket\n", "connected_clients = {}  # UUID -> WebSocket\n\ngame_settings = {\n    \"max_players\": 8,\n    \"max_teams\": 2,\n    \"max_per_team\": 4\n}\n")

# Broadcast game settings
if "\"settings\": game_settings" not in content:
    content = content.replace("\"type\": \"STATE_UPDATE\",\n        \"players\":", "\"type\": \"STATE_UPDATE\",\n        \"settings\": game_settings,\n        \"players\":")

# Add ADMIN_UPDATE_SETTINGS
if "ADMIN_UPDATE_SETTINGS" not in content:
    old_join = 'elif msg_type == "JOIN":'
    new_admin_settings = '''elif msg_type == "ADMIN_UPDATE_SETTINGS":
                new_settings = data.get("settings", {})
                if "max_players" in new_settings:
                    game_settings["max_players"] = int(new_settings["max_players"])
                if "max_teams" in new_settings:
                    game_settings["max_teams"] = int(new_settings["max_teams"])
                if "max_per_team" in new_settings:
                    game_settings["max_per_team"] = int(new_settings["max_per_team"])
                print(f"[ADMIN] Updated settings: {game_settings}")
                await broadcast_state()

            elif msg_type == "JOIN":'''
    content = content.replace(old_join, new_admin_settings)

# Enforce limits
if "Limit checks" not in content:
    old_marker_check = '''if marker_id is None:
                    continue'''
    new_marker_check = '''if marker_id is None:
                    continue

                # Limit checks
                active_players = sum(1 for p in players.values() if p["status"] != "ADMIN")
                if active_players >= game_settings["max_players"]:
                    await websocket.send(json.dumps({"type": "ERROR", "message": "Game is full! Max players reached."}))
                    continue
                    
                if team != "SOLO":
                    if team not in teams and len(teams) >= game_settings["max_teams"]:
                        await websocket.send(json.dumps({"type": "ERROR", "message": f"Cannot join {team}. Max {game_settings['max_teams']} teams reached!"}))
                        continue
                    if team in teams and len(teams[team]) >= game_settings["max_per_team"]:
                        await websocket.send(json.dumps({"type": "ERROR", "message": f"{team} is full! Max {game_settings['max_per_team']} players per team."}))
                        continue'''
    content = content.replace(old_marker_check, new_marker_check)

with open("Software/Server/server.py", "w") as f:
    f.write(content)
