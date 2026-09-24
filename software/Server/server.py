import asyncio
import json
import os
import websockets
import uuid

# Config
STARTING_HP = 100
WEAPON_DAMAGE = 20
RESPAWN_TIMER = 10  # seconds

# Game State
players = {}          # player_id -> {socket, name, team, hp, marker_id, status, kills}
teams = {}            # team_name -> [player_ids]
connected_clients = {}  # player_id -> websocket (ALL connections, even before JOIN)

game_settings = {
    "max_players": 8,
    "max_teams": 2,
    "max_per_team": 4
}


async def broadcast_state():
    """Sends game state to ALL connected sockets (players + admin + pre-join)."""
    # Build serializable player state
    players_state = {}
    for pid, p in players.items():
        players_state[pid] = {
            "name": p["name"],
            "team": p["team"],
            "hp": p["hp"],
            "marker_id": p["marker_id"],
            "status": p["status"],
            "kills": p.get("kills", 0)
        }

    team_scores = {}
    for team_name, member_ids in teams.items():
        team_scores[team_name] = sum(
            players[pid].get("kills", 0) for pid in member_ids if pid in players
        )

    payload = json.dumps({
        "type": "STATE_SYNC",
        "settings": game_settings,
        "players": players_state,
        "team_scores": team_scores
    })

    # Send to ALL connected sockets (not just players)
    dead = []
    for cid, sock in list(connected_clients.items()):
        try:
            await sock.send(payload)
        except Exception:
            dead.append(cid)

    for cid in dead:
        cleanup_player(cid)


def cleanup_player(player_id):
    """Remove a player from all state tracking."""
    if player_id in players:
        p = players[player_id]
        team = p.get("team")
        if team and team in teams and player_id in teams[team]:
            teams[team].remove(player_id)
            if not teams[team]:
                del teams[team]
        print(f"[CLEANUP] {p.get('name', '?')} ({player_id[:8]}...) removed.")
        del players[player_id]
    connected_clients.pop(player_id, None)


async def handle_hit_report(shooter_id, target_marker_id):
    shooter = players.get(shooter_id)
    if not shooter:
        return

    if shooter["status"] != "ALIVE":
        return

    if shooter["marker_id"] == target_marker_id:
        return  # Self-shoot

    # Find victim
    victim_id = None
    victim = None
    for pid, p in players.items():
        if p["marker_id"] == target_marker_id and pid != shooter_id:
            victim_id = pid
            victim = p
            break

    if not victim or victim["status"] != "ALIVE":
        return

    # Friendly fire check
    if shooter["team"] and shooter["team"] != "SOLO" and shooter["team"] == victim["team"]:
        return

    # Apply damage
    victim["hp"] -= WEAPON_DAMAGE
    is_fatal = victim["hp"] <= 0

    if is_fatal:
        victim["hp"] = 0
        victim["status"] = "DEAD"
        shooter["kills"] = shooter.get("kills", 0) + 1

    print(f"[HIT] {shooter['name']} -> {victim['name']}. HP: {victim['hp']}"
          + (" [KILL!]" if is_fatal else ""))

    # Notify victim
    try:
        await victim["socket"].send(json.dumps({
            "type": "DAMAGE_RECEIVED",
            "amount": WEAPON_DAMAGE,
            "is_fatal": is_fatal
        }))
    except Exception:
        pass

    # Notify shooter
    try:
        await shooter["socket"].send(json.dumps({
            "type": "HIT_CONFIRMED",
            "is_fatal": is_fatal
        }))
    except Exception:
        pass

    if is_fatal:
        try:
            await victim["socket"].send(json.dumps({
                "type": "DEATH_EVENT",
                "respawn_timer_seconds": RESPAWN_TIMER
            }))
        except Exception:
            pass
        asyncio.create_task(respawn_player(victim_id))

    await broadcast_state()


async def respawn_player(player_id):
    await asyncio.sleep(RESPAWN_TIMER)
    if player_id in players and players[player_id]["status"] == "DEAD":
        players[player_id]["hp"] = STARTING_HP
        players[player_id]["status"] = "ALIVE"
        print(f"[RESPAWN] {players[player_id]['name']} is back!")
        try:
            await players[player_id]["socket"].send(json.dumps({"type": "RESPAWN"}))
        except Exception:
            pass
        await broadcast_state()


async def client_handler(websocket):
    player_id = str(uuid.uuid4())
    connected_clients[player_id] = websocket
    print(f"[CONNECT] {player_id[:8]}...")

    # Immediately send current settings so the phone can populate team dropdown
    try:
        await websocket.send(json.dumps({
            "type": "SETTINGS_UPDATE",
            "settings": game_settings
        }))
    except Exception:
        connected_clients.pop(player_id, None)
        return

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except (json.JSONDecodeError, TypeError):
                continue

            msg_type = data.get("type")

            if msg_type == "ADMIN_JOIN":
                players[player_id] = {
                    "socket": websocket,
                    "name": "ADMIN",
                    "team": None,
                    "hp": 0,
                    "kills": 0,
                    "status": "ADMIN",
                    "marker_id": -1
                }
                print("[ADMIN] Dashboard connected.")
                await broadcast_state()

            elif msg_type == "ADMIN_RESET":
                print("[ADMIN] Resetting game...")
                for p in players.values():
                    if p["status"] != "ADMIN":
                        p["hp"] = STARTING_HP
                        p["status"] = "ALIVE"
                        p["kills"] = 0
                await broadcast_state()

            elif msg_type == "ADMIN_UPDATE_SETTINGS":
                s = data.get("settings", {})
                if "max_players" in s:
                    game_settings["max_players"] = max(1, int(s["max_players"]))
                if "max_teams" in s:
                    game_settings["max_teams"] = max(1, int(s["max_teams"]))
                if "max_per_team" in s:
                    game_settings["max_per_team"] = max(1, int(s["max_per_team"]))
                print(f"[ADMIN] Settings: {game_settings}")
                await broadcast_state()

            elif msg_type == "JOIN":
                name = data.get("player_name", "Unknown")
                marker_id = data.get("marker_id")
                team = data.get("team", "TEAM_RED")

                if marker_id is None:
                    await websocket.send(json.dumps({
                        "type": "ERROR",
                        "message": "marker_id is required"
                    }))
                    continue

                # If this player_id already exists (reconnection), clean old entry first
                if player_id in players:
                    cleanup_player(player_id)
                    connected_clients[player_id] = websocket

                # Check duplicate marker (different player using same marker)
                dup = False
                for pid, p in players.items():
                    if p["marker_id"] == marker_id and pid != player_id:
                        dup = True
                        await websocket.send(json.dumps({
                            "type": "ERROR",
                            "message": f"Marker {marker_id} is already in use by {p['name']}"
                        }))
                        break

                if dup:
                    continue

                # Enforce limits
                active = sum(1 for p in players.values() if p["status"] != "ADMIN")
                if active >= game_settings["max_players"]:
                    await websocket.send(json.dumps({
                        "type": "ERROR",
                        "message": f"Game full! Max {game_settings['max_players']} players."
                    }))
                    continue

                if team and team != "SOLO":
                    if team not in teams and len(teams) >= game_settings["max_teams"]:
                        await websocket.send(json.dumps({
                            "type": "ERROR",
                            "message": f"Max {game_settings['max_teams']} teams reached!"
                        }))
                        continue
                    if team in teams and len(teams[team]) >= game_settings["max_per_team"]:
                        await websocket.send(json.dumps({
                            "type": "ERROR",
                            "message": f"{team} full! Max {game_settings['max_per_team']} per team."
                        }))
                        continue

                # Register
                players[player_id] = {
                    "socket": websocket,
                    "name": name,
                    "marker_id": marker_id,
                    "team": team,
                    "hp": STARTING_HP,
                    "status": "ALIVE",
                    "kills": 0
                }
                if team and team != "SOLO":
                    if team not in teams:
                        teams[team] = []
                    teams[team].append(player_id)

                print(f"[JOIN] {name} -> {team} (Marker {marker_id})")
                await websocket.send(json.dumps({
                    "type": "JOIN_ACK",
                    "player_id": player_id,
                    "message": f"Welcome {name}!"
                }))
                await broadcast_state()

            elif msg_type == "HIT_REPORT":
                target = data.get("target_marker_id")
                if target is not None:
                    await handle_hit_report(player_id, target)

    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"[ERROR] {player_id[:8]}: {e}")
    finally:
        cleanup_player(player_id)
        await broadcast_state()


async def main():
    port = int(os.environ.get("PORT", 8765))
    print("=" * 50)
    print("  LASER TAG SERVER")
    print(f"  Listening on ws://0.0.0.0:{port}")
    print("=" * 50)
    async with websockets.serve(
        client_handler,
        "0.0.0.0",
        port,
        ping_interval=20,
        ping_timeout=20,
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
