import os

with open("Software/Server/server.py", "r") as f:
    content = f.read()

# Add ADMIN_JOIN to server.py
if "ADMIN_JOIN" not in content:
    old_join = 'if msg_type == "JOIN":'
    new_admin = '''if msg_type == "ADMIN_JOIN":
                players[player_id] = {
                    "name": "ADMIN",
                    "team": None,
                    "hp": 0,
                    "kills": 0,
                    "status": "ADMIN",
                    "marker_id": -1
                }
                print("[ADMIN] Dashboard Connected.")
                await broadcast_state()
            
            elif msg_type == "ADMIN_RESET":
                print("[ADMIN] Resetting game state...")
                for p in players.values():
                    if p["status"] != "ADMIN":
                        p["hp"] = STARTING_HP
                        p["status"] = "ALIVE"
                        p["kills"] = 0
                await broadcast_state()

            elif msg_type == "JOIN":'''
    content = content.replace(old_join, new_admin)
    with open("Software/Server/server.py", "w") as f:
        f.write(content)

with open("Software/WebClient/index.html", "r") as f:
    html = f.read()

# Web Audio API for 5000% volume
if "audioCtx" not in html:
    old_audio = "const reloadSound = new Audio('reload.mp3');"
    new_audio = """const reloadSound = new Audio('reload.mp3');
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const reloadSource = audioCtx.createMediaElementSource(reloadSound);
        const gainNode = audioCtx.createGain();
        gainNode.gain.value = 50.0; // 5000% volume
        reloadSource.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        // Resume AudioContext on first tap
        document.body.addEventListener('touchstart', () => { if (audioCtx.state === 'suspended') audioCtx.resume(); }, {once: true});
        document.body.addEventListener('mousedown', () => { if (audioCtx.state === 'suspended') audioCtx.resume(); }, {once: true});"""
    html = html.replace(old_audio, new_audio)

# Cloud WebSocket URL
if "laser-tag-server.onrender.com" not in html:
    old_ws = 'ws = new WebSocket(`ws://${serverIp}:8765`);'
    new_ws = 'ws = new WebSocket(`wss://laser-tag-server.onrender.com`);'
    html = html.replace(old_ws, new_ws)

with open("Software/WebClient/index.html", "w") as f:
    f.write(html)
