import asyncio
import websockets
import json

async def mock_player(name, marker_id, team, target_marker_to_shoot, join_delay=0, shoot_delay=2):
    """Simulate a player joining and shooting."""
    uri = "ws://localhost:8765"

    # Stagger joins to prevent race conditions
    await asyncio.sleep(join_delay)

    async with websockets.connect(uri) as websocket:
        # 1. Join Game
        join_msg = {
            "type": "JOIN",
            "player_name": name,
            "marker_id": marker_id,
            "team": team
        }
        await websocket.send(json.dumps(join_msg))

        # Wait for JOIN_ACK
        ack = await asyncio.wait_for(websocket.recv(), timeout=5)
        ack_data = json.loads(ack)
        if ack_data.get("type") == "JOIN_ACK":
            print(f"[{name}] Joined successfully!")
        elif ack_data.get("type") == "ERROR":
            print(f"[{name}] ERROR: {ack_data.get('message')}")
            return

        # Drain the initial STATE_SYNC
        try:
            await asyncio.wait_for(websocket.recv(), timeout=2)
        except asyncio.TimeoutError:
            pass

        # 2. Wait a bit, then shoot!
        await asyncio.sleep(shoot_delay)
        print(f"[{name}] Shooting at marker {target_marker_to_shoot}...")
        shoot_msg = {
            "type": "HIT_REPORT",
            "target_marker_id": target_marker_to_shoot,
            "timestamp": 123456789.0
        }
        await websocket.send(json.dumps(shoot_msg))

        # 3. Listen for responses (with timeout to prevent hanging)
        for _ in range(5):
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=3)
                data = json.loads(response)
                if data["type"] != "STATE_SYNC":
                    print(f"[{name} RECEIVED] {json.dumps(data, indent=2)}")
            except asyncio.TimeoutError:
                break  # No more messages, stop listening


async def main():
    print("=" * 50)
    print("  LASER TAG TEST CLIENT")
    print("  Make sure server.py is running first!")
    print("=" * 50)
    print()

    # Simulate a 2v1 situation
    # Player 1 (Red, Marker 1) shoots Player 3 (Blue, Marker 3) -> Valid hit
    # Player 3 (Blue, Marker 3) shoots Player 2 (Red, Marker 2) -> Valid hit
    # Player 2 (Red, Marker 2) shoots Player 1 (Red, Marker 1) -> Friendly fire! Ignored.

    p1 = mock_player("Alpha",   marker_id=1, team="TEAM_RED",  target_marker_to_shoot=3, join_delay=0,   shoot_delay=2)
    p2 = mock_player("Charlie", marker_id=2, team="TEAM_RED",  target_marker_to_shoot=1, join_delay=0.5, shoot_delay=2)
    p3 = mock_player("Bravo",   marker_id=3, team="TEAM_BLUE", target_marker_to_shoot=2, join_delay=1.0, shoot_delay=2)

    await asyncio.gather(p1, p2, p3)
    print()
    print("Test complete!")


if __name__ == "__main__":
    asyncio.run(main())
