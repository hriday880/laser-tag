import asyncio
import json
import websockets
import uuid
import time

# Game State
players = {}
teams = {}  # Dynamic: auto-created when a player joins with a new team name

# Config
STARTING_HP = 100
WEAPON_DAMAGE = 20
RESPAWN_TIMER = 10  # seconds

async def broadcast_state():
    """Sends the current game state to all connected players."""
    if not players:
        return

    # Build per-player state (excluding socket objects which aren't serializable)
    players_state = {}
    for pid, p in players.items():
        players_state[pid] = {
            "name": p["name"],
            "team": p["team"],
            "hp": p["hp"],
            "marker_id": p["marker_id"],
            "status": p["status"]
        }

    # Build team scores
    team_scores = {}
    for team_name in teams:
        team_scores[team_name] = sum(
            players[pid].get("kills", 0) for pid in teams[team_name] if pid in players
        )

    state_payload = {
        "type": "STATE_SYNC",
        "players": players_state,
        "team_scores": team_scores
    }

    encoded = json.dumps(state_payload)
    dead_sockets = []
    # Snapshot the dict to avoid RuntimeError if cleanup modifies it
    for pid, p in list(players.items()):
        try:
            await p["socket"].send(encoded)
        except websockets.exceptions.ConnectionClosed:
            dead_sockets.append(pid)
        except Exception:
            dead_sockets.append(pid)

    # Cleanup any dead sockets discovered during broadcast
    for pid in dead_sockets:
        cleanup_player(pid)


def cleanup_player(player_id):
    """Remove a player from all state tracking."""
    if player_id in players:
        team = players[player_id]["team"]
        if team in teams and player_id in teams[team]:
            teams[team].remove(player_id)
            if not teams[team]:
                del teams[team]  # Remove empty teams
        name = players[player_id]["name"]
        del players[player_id]
        print(f"[CLEANUP] {name} ({player_id[:8]}...) removed.")


async def handle_hit_report(shooter_id, target_marker_id):
    shooter = players.get(shooter_id)
    if not shooter:
        return
    if shooter["status"] == "DEAD":
        return  # Dead players can't shoot

    # Self-shoot protection: ignore if shooter's own marker
    if shooter["marker_id"] == target_marker_id:
        return

    # Find who owns the target marker
    victim_id = None
    victim = None
    for pid, p in players.items():
        if p["marker_id"] == target_marker_id and pid != shooter_id:
            victim_id = pid
            victim = p
            break

    if not victim:
        return  # No player found with that marker (stale frame / missed)
    if victim["status"] == "DEAD":
        return  # Can't kill a dead player

    # Friendly Fire Check
    if shooter["team"] == victim["team"]:
        print(f"[FF] {shooter['name']} tried to shoot teammate {victim['name']}. Ignored.")
        return

    # Apply Damage
    victim["hp"] -= WEAPON_DAMAGE
    is_fatal = victim["hp"] <= 0

    if is_fatal:
        victim["hp"] = 0
        victim["status"] = "DEAD"
        shooter["kills"] = shooter.get("kills", 0) + 1

    print(f"[HIT] {shooter['name']} -> {victim['name']}. HP: {victim['hp']}"
          + (" [KILL!]" if is_fatal else ""))

    # Notify Victim
    try:
        await victim["socket"].send(json.dumps({
            "type": "DAMAGE_RECEIVED",
            "amount": WEAPON_DAMAGE,
            "shooter_name": shooter["name"],
            "is_fatal": is_fatal
        }))
    except Exception:
        pass

    # Notify Shooter
    try:
        await shooter["socket"].send(json.dumps({
            "type": "HIT_CONFIRMED",
            "target_name": victim["name"],
            "is_fatal": is_fatal
        }))
    except Exception:
        pass

    # If fatal, schedule respawn
    if is_fatal:
        try:
            await victim["socket"].send(json.dumps({
                "type": "DEATH_EVENT",
                "respawn_timer_seconds": RESPAWN_TIMER
            }))
        except Exception:
            pass
        asyncio.create_task(respawn_player(victim_id))

    # Broadcast updated state to everyone
    await broadcast_state()


async def respawn_player(player_id):
    """Respawn a dead player after the respawn timer."""
    await asyncio.sleep(RESPAWN_TIMER)
    if player_id in players and players[player_id]["status"] == "DEAD":
        players[player_id]["hp"] = STARTING_HP
        players[player_id]["status"] = "ALIVE"
        print(f"[RESPAWN] {players[player_id]['name']} is back!")
        try:
            await players[player_id]["socket"].send(json.dumps({
                "type": "RESPAWN"
            }))
        except Exception:
            pass
        await broadcast_state()


async def client_handler(websocket):
    player_id = str(uuid.uuid4())
    print(f"[CONNECT] New connection: {player_id[:8]}...")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                continue  # Ignore malformed JSON

            msg_type = data.get("type")

            if msg_type == "JOIN":
                name = data.get("player_name", "Unknown")
                marker_id = data.get("marker_id")
                team = data.get("team", "TEAM_RED")

                # Validate marker_id
                if marker_id is None:
                    await websocket.send(json.dumps({
                        "type": "ERROR",
                        "message": "marker_id is required"
                    }))
                    continue

                # Check for duplicate marker IDs
                for pid, p in players.items():
                    if p["marker_id"] == marker_id:
                        await websocket.send(json.dumps({
                            "type": "ERROR",
                            "message": f"Marker {marker_id} is already in use by {p['name']}"
                        }))
                        break
                else:
                    # No duplicate found, register the player
                    players[player_id] = {
                        "socket": websocket,
                        "name": name,
                        "marker_id": marker_id,
                        "team": team,
                        "hp": STARTING_HP,
                        "status": "ALIVE",
                        "kills": 0
                    }
                    # Auto-create team if it doesn't exist
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
                target_marker = data.get("target_marker_id")
                if target_marker is not None:
                    await handle_hit_report(player_id, target_marker)

    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"[ERROR] Unexpected error for {player_id[:8]}: {e}")
    finally:
        cleanup_player(player_id)
        await broadcast_state()


async def main():
    print("=" * 50)
    print("  LASER TAG SERVER")
    print("  Listening on ws://0.0.0.0:8765")
    print("=" * 50)
    async with websockets.serve(client_handler, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
