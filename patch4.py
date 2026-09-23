import json

with open("Software/Server/server.py", "r") as f:
    content = f.read()

old_code = '''async def client_handler(websocket):
    player_id = str(uuid.uuid4())
    print(f"[CONNECT] New connection: {player_id[:8]}...")

    try:
        async for message in websocket:'''
        
new_code = '''async def client_handler(websocket):
    player_id = str(uuid.uuid4())
    print(f"[CONNECT] New connection: {player_id[:8]}...")
    
    try:
        await websocket.send(json.dumps({
            "type": "SETTINGS_UPDATE",
            "settings": game_settings
        }))
    except Exception:
        pass

    try:
        async for message in websocket:'''

content = content.replace(old_code, new_code)

with open("Software/Server/server.py", "w") as f:
    f.write(content)
