with open("Software/WebClient/index.html", "r") as f:
    html = f.read()

# Replace window.onload
old_onload = '''        window.onload = () => {
            scanBtn.innerText = "START CAMERA & SCAN VEST";
            scanBtn.disabled = false;
        };'''

new_onload = '''        let ws = null;
        let hasJoined = false;

        window.onload = () => {
            scanBtn.innerText = "START CAMERA & SCAN VEST";
            scanBtn.disabled = false;
            
            ws = new WebSocket(`wss://laser-tag-laser-tag-server.onrender.com`);
            
            ws.onmessage = (e) => {
                const msg = JSON.parse(e.data);
                
                if (msg.type === "SETTINGS_UPDATE" || msg.type === "STATE_SYNC") {
                    if (msg.settings && !hasJoined) {
                        const select = document.getElementById('teamSelect');
                        // Keep current selection if possible
                        const currentVal = select.value;
                        select.innerHTML = '<option value="SOLO">No Team (Solo)</option>';
                        const teamNames = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Cyan", "Pink"];
                        for(let i=0; i<msg.settings.max_teams && i<teamNames.length; i++) {
                            const opt = document.createElement('option');
                            opt.value = `TEAM_${teamNames[i].toUpperCase()}`;
                            opt.innerText = `Team ${teamNames[i]}`;
                            select.appendChild(opt);
                        }
                        if(Array.from(select.options).some(o => o.value === currentVal)) {
                            select.value = currentVal;
                        }
                    }
                } else if (msg.type === "ERROR") {
                    alert("SERVER ERROR: " + msg.message + "\\n\\nPlease pick a different vest or team.");
                    hud.style.display = 'none';
                    setupScreen.style.display = 'flex';
                    hasJoined = false;
                } else if (msg.type === "JOIN_ACK") {
                    console.log("Successfully joined server!");
                    hasJoined = true;
                } else if (msg.type === "DAMAGE_RECEIVED") {
                    takeDamage(msg.amount, msg.is_fatal);
                } else if (msg.type === "HIT_CONFIRMED") {
                    flashHitmarker();
                } else if (msg.type === "DEATH_EVENT") {
                    die(msg.respawn_timer_seconds);
                } else if (msg.type === "RESPAWN") {
                    respawn();
                }
            };
        };'''
html = html.replace(old_onload, new_onload)

# Replace connectWebSocket function
old_connect = '''        function connectWebSocket() {
            const serverIp = window.location.hostname || "localhost";
            ws = new WebSocket(`wss://laser-tag-laser-tag-server.onrender.com`);
            
            ws.onopen = () => {
                ws.send(JSON.stringify({
                    type: "JOIN",
                    player_name: document.getElementById('playerName').value,
                    marker_id: myMarkerId,
                    team: document.getElementById('teamSelect').value
                }));
            };
            
            ws.onmessage = (e) => {
                const msg = JSON.parse(e.data);
                if (msg.type === "ERROR") {
                    alert("SERVER ERROR: " + msg.message + "\\n\\nPlease pick a different vest or team.");
                    // Kick back to setup screen
                    hud.style.display = 'none';
                    setupScreen.style.display = 'flex';
                    if (videoTrack) {
                        videoTrack.stop(); // Stop camera
                    }
                    ws.close();
                } else if (msg.type === "JOIN_ACK") {
                    console.log("Successfully joined server!");
                    // We could set myPlayerId here if needed
                } else if (msg.type === "DAMAGE_RECEIVED") {
                    takeDamage(msg.amount, msg.is_fatal);
                } else if (msg.type === "HIT_CONFIRMED") {
                    flashHitmarker();
                } else if (msg.type === "DEATH_EVENT") {
                    die(msg.respawn_timer_seconds);
                } else if (msg.type === "RESPAWN") {
                    respawn();
                }
            };
        }'''

new_connect = '''        function connectWebSocket() {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: "JOIN",
                    player_name: document.getElementById('playerName').value,
                    marker_id: myMarkerId,
                    team: document.getElementById('teamSelect').value
                }));
            } else {
                alert("Server not connected! Refresh the page.");
                setupScreen.style.display = 'flex';
                hud.style.display = 'none';
            }
        }'''

html = html.replace(old_connect, new_connect)

with open("Software/WebClient/index.html", "w") as f:
    f.write(html)
