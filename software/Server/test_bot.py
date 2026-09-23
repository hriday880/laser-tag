#!/usr/bin/env python3
"""
# test_bot.py - Laser Tag QA Load Testing Script
# 
# Simulates 8 concurrent WebSocket clients connecting to the Laser Tag server,
# registering as Markers 0 through 7 on opposing teams (TEAM_RED and TEAM_BLUE),
# and continuously sending random HIT_REPORTs for a specified duration (default: 15s)
# to verify server stability and absence of exceptions under high load.
"""

import argparse
import asyncio
import json
import random
import sys
import time
import websockets

DEFAULT_URI = "ws://127.0.0.1:8765"
DEFAULT_CLIENTS = 8
DEFAULT_DURATION = 15.0  # seconds
TEAMS = ["TEAM_RED", "TEAM_BLUE"]


class BotClient:
    def __init__(self, marker_id: int, team: str, uri: str = DEFAULT_URI):
        self.marker_id = marker_id
        self.name = f"Bot-{marker_id}"
        self.team = team
        self.uri = uri
        self.player_id = None
        self.ws = None

        # Telemetry / Statistics
        self.hits_sent = 0
        self.hits_confirmed = 0
        self.damage_received = 0
        self.deaths = 0
        self.respawns = 0
        self.state_syncs = 0
        self.errors = []

        self._running = False
        self._rx_task = None

    async def connect_and_join(self):
        """Connect to WebSocket server and send JOIN message."""
        self.ws = await websockets.connect(self.uri)
        join_msg = {
            "type": "JOIN",
            "player_name": self.name,
            "marker_id": self.marker_id,
            "team": self.team
        }
        await self.ws.send(json.dumps(join_msg))

        # Await JOIN_ACK
        response = await asyncio.wait_for(self.ws.recv(), timeout=5.0)
        data = json.loads(response)
        if data.get("type") == "JOIN_ACK":
            self.player_id = data.get("player_id")
            print(f"  [+] {self.name} joined {self.team} (Marker {self.marker_id}, ID: {self.player_id[:8]}...)")
        elif data.get("type") == "ERROR":
            raise RuntimeError(f"{self.name} join rejected: {data.get('message')}")
        else:
            raise RuntimeError(f"{self.name} unexpected response: {data}")

        # Start continuous message receiver task
        self._running = True
        self._rx_task = asyncio.create_task(self._receive_loop())

    async def _receive_loop(self):
        """Continuously process incoming server messages."""
        try:
            while self._running:
                raw = await self.ws.recv()
                msg = json.loads(raw)
                mtype = msg.get("type")
                if mtype == "STATE_SYNC":
                    self.state_syncs += 1
                elif mtype == "HIT_CONFIRMED":
                    self.hits_confirmed += 1
                elif mtype == "DAMAGE_RECEIVED":
                    self.damage_received += 1
                elif mtype == "DEATH_EVENT":
                    self.deaths += 1
                elif mtype == "RESPAWN":
                    self.respawns += 1
                elif mtype == "ERROR":
                    self.errors.append(msg.get("message", "Unknown error"))
        except asyncio.CancelledError:
            pass
        except websockets.exceptions.ConnectionClosed:
            if self._running:
                self.errors.append("Connection closed unexpectedly by server")
        except Exception as exc:
            if self._running:
                self.errors.append(f"Receiver exception: {exc}")

    async def fire_loop(self, duration: float, stop_event: asyncio.Event, max_target: int):
        """Randomly fire HIT_REPORTs until duration expires or stop_event is set."""
        start_time = time.time()
        while (time.time() - start_time < duration) and not stop_event.is_set():
            target_marker = random.randint(0, max_target - 1)
            hit_msg = {
                "type": "HIT_REPORT",
                "target_marker_id": target_marker,
                "timestamp": time.time()
            }
            try:
                await self.ws.send(json.dumps(hit_msg))
                self.hits_sent += 1
            except websockets.exceptions.ConnectionClosed:
                self.errors.append("Socket closed while sending HIT_REPORT")
                break
            except Exception as exc:
                self.errors.append(f"Send failed: {exc}")
                break

            # Brief random sleep between shots (50ms - 150ms)
            await asyncio.sleep(random.uniform(0.05, 0.15))

    async def stop(self):
        """Gracefully terminate client connection and receiver task."""
        self._running = False
        if self._rx_task:
            self._rx_task.cancel()
            try:
                await self._rx_task
            except asyncio.CancelledError:
                pass
        if self.ws:
            await self.ws.close()


async def run_load_test(uri: str, num_clients: int, duration: float):
    print("=" * 60)
    print("        LASER TAG QA BOT - LOAD TEST RUNNER")
    print(f" Target URI: {uri}")
    print(f" Clients:    {num_clients} (Markers 0 to {num_clients - 1})")
    print(f" Duration:   {duration} seconds")
    print("=" * 60)

    # 1. Initialize Bot instances
    bots = []
    for marker_id in range(num_clients):
        team = TEAMS[marker_id % len(TEAMS)]
        bots.append(BotClient(marker_id, team, uri=uri))

    # 2. Connect and JOIN all bots
    print(f"\n[PHASE 1] Connecting {num_clients} bots and joining game...")
    try:
        await asyncio.gather(*(bot.connect_and_join() for bot in bots))
    except Exception as exc:
        print(f"[!] Failed to connect/join bots: {exc}")
        for bot in bots:
            await bot.stop()
        return False

    print(f"[+] All {num_clients} bots successfully joined!")

    # 3. Concurrent Firing Phase
    print(f"\n[PHASE 2] Firing random HIT_REPORTs for {duration} seconds...")
    stop_event = asyncio.Event()
    start_time = time.time()

    fire_tasks = [
        asyncio.create_task(bot.fire_loop(duration, stop_event, num_clients))
        for bot in bots
    ]

    await asyncio.gather(*fire_tasks)
    elapsed = time.time() - start_time
    print(f"[+] Firing completed in {elapsed:.2f} seconds.")

    # 4. Grace period for final broadcasts
    print("\n[PHASE 3] Allowing 0.5s grace period for in-flight broadcasts...")
    await asyncio.sleep(0.5)

    # 5. Stop and disconnect all bots
    for bot in bots:
        await bot.stop()

    # 6. Aggregate and Display Results
    total_sent = sum(b.hits_sent for b in bots)
    total_confirmed = sum(b.hits_confirmed for b in bots)
    total_damage = sum(b.damage_received for b in bots)
    total_deaths = sum(b.deaths for b in bots)
    total_respawns = sum(b.respawns for b in bots)
    total_syncs = sum(b.state_syncs for b in bots)
    all_errors = [(b.name, err) for b in bots for err in b.errors]

    print("\n" + "=" * 60)
    print("                 LOAD TEST SUMMARY")
    print("=" * 60)
    print(f" Test Duration:               {elapsed:.2f} s")
    print(f" Total HIT_REPORTs Sent:      {total_sent} (~{total_sent/elapsed:.1f} shots/sec)")
    print(f" Total Hits Confirmed:        {total_confirmed}")
    print(f" Total Damage Events Received:{total_damage}")
    print(f" Total Death Events:          {total_deaths}")
    print(f" Total Respawns:              {total_respawns}")
    print(f" Total STATE_SYNCs Received:  {total_syncs}")
    print("-" * 60)
    print(f" Individual Bot Breakdown:")
    for b in bots:
        print(f"  - {b.name} ({b.team}, Marker {b.marker_id}): "
              f"Sent={b.hits_sent}, Hits={b.hits_confirmed}, DmgRcvd={b.damage_received}, "
              f"Deaths={b.deaths}, Syncs={b.state_syncs}, Errors={len(b.errors)}")

    print("-" * 60)
    if all_errors:
        print(f"[FAIL] {len(all_errors)} errors encountered during test:")
        for name, err in all_errors:
            print(f"  - [{name}] {err}")
        return False
    else:
        print("[SUCCESS] Test completed with ZERO client errors or exceptions!")
        return True


def main():
    parser = argparse.ArgumentParser(description="Laser Tag Server QA Load Test Bot")
    parser.add_argument("--uri", default=DEFAULT_URI, help=f"WebSocket URI (default: {DEFAULT_URI})")
    parser.add_argument("--clients", type=int, default=DEFAULT_CLIENTS, help=f"Number of clients (default: {DEFAULT_CLIENTS})")
    parser.add_argument("--duration", type=float, default=DEFAULT_DURATION, help=f"Duration in seconds (default: {DEFAULT_DURATION})")
    args = parser.parse_args()

    success = asyncio.run(run_load_test(args.uri, args.clients, args.duration))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
