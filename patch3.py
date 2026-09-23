with open("Software/Server/server.py", "r") as f:
    content = f.read()

content = content.replace('''            if msg_type == "ADMIN_JOIN":
                players[player_id] = {
                    "name": "ADMIN",
                    "team": None,
                    "hp": 0,
                    "kills": 0,
                    "status": "ADMIN",
                    "marker_id": -1
                }''', '''            if msg_type == "ADMIN_JOIN":
                players[player_id] = {
                    "socket": websocket,
                    "name": "ADMIN",
                    "team": None,
                    "hp": 0,
                    "kills": 0,
                    "status": "ADMIN",
                    "marker_id": -1
                }''')

with open("Software/Server/server.py", "w") as f:
    f.write(content)
