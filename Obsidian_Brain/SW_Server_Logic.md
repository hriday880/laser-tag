# 🟪 Server Logic & Team Management

> [!abstract] Overview
> A lightweight Python WebSocket server. It runs on a laptop connected to the arena's local WiFi router. No internet required.

## Player / Marker Mapping
The server must map **Players** (Socket connections) to **Markers** (Physical ArUco prints) to **Teams**.

```json
// Server's internal state
{
  "gameState": "PLAYING",
  "teams": {
    "TEAM_RED": ["player_uuid_1", "player_uuid_2", ...],
    "TEAM_BLUE": ["player_uuid_3", "player_uuid_4", ...]
  },
  "players": {
    "player_uuid_1": {
      "name": "Alpha",
      "marker_id": 0,
      "team": "TEAM_RED",
      "hp": 100,
      "status": "ALIVE"
    }
  }
}
```

## Asymmetrical Teams (8v4, 6v6, etc.)
Because teams are just string arrays in the server, **any configuration is possible**.
- 8 of 1s, 4 of 2s (8v4 Juggernaut mode)
- 3v3v3v3 (Squads)
- 1v11 (Zombie / Boss mode)

## Hit Resolution Logic

When the server receives a `HIT_REPORT` from `player_uuid_1` claiming they shot `marker_id: 3`:

1. **Find Target:** Server iterates through the `players` dict to find who owns `marker_id: 3`. (Let's say it's `player_uuid_4`).
2. **Check Status:** Is `player_uuid_1` ALIVE? (Dead men can't shoot). Is `player_uuid_4` ALIVE? (Can't kill a dead man).
3. **Friendly Fire Check:** Are they on the same team?
   - If `TEAM_RED` == `TEAM_RED` -> Ignore (or apply penalty).
4. **Apply Damage:** 
   - `player_uuid_4.hp -= 20`
5. **Broadcast:**
   - Send `DAMAGE_RECEIVED` to `player_uuid_4` (makes their phone vibrate and flash red).
   - Send `HIT_CONFIRMED` to `player_uuid_1` (gives them points, plays hitmarker sound).
   - If HP <= 0, send `DEATH_EVENT`.

## Tick Rate
The server doesn't need a high physics tick rate because movement isn't tracked on the server. It is purely event-driven. This allows it to run on a potato laptop without lag.

---
*Parent: [[Software_Master_Node]]*
