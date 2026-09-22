# 🟧 Network Protocol (JSON Schemas)

> [!info] TCP/WebSockets
> We use WebSockets because they allow bi-directional, persistent, low-latency connections over local WiFi.

## 1. Client -> Server Payloads

**Join Game:**
```json
{
  "type": "JOIN",
  "player_name": "Ghost",
  "marker_id": 5
}
```

**Report a Hit (Fired when crosshair intersects marker):**
```json
{
  "type": "HIT_REPORT",
  "target_marker_id": 2,
  "timestamp": 1695420000.123 
}
```
*(Note: We don't send "misses" to the server to save bandwidth).*

## 2. Server -> Client Payloads

**Game State Update (Broadcast every 1s, or on changes):**
```json
{
  "type": "STATE_SYNC",
  "time_remaining": 300,
  "team_scores": {"TEAM_RED": 40, "TEAM_BLUE": 10},
  "my_hp": 80
}
```

**Take Damage (Sent only to the victim):**
```json
{
  "type": "DAMAGE_RECEIVED",
  "amount": 20,
  "shooter_name": "SniperBoy99",
  "is_fatal": false
}
```

**Hit Confirmation (Sent only to the shooter):**
```json
{
  "type": "HIT_CONFIRMED",
  "target_name": "NoobMaster",
  "points_awarded": 10
}
```

**Kill Command (When HP hits 0):**
```json
{
  "type": "DEATH_EVENT",
  "respawn_timer_seconds": 10
}
```

---
*Parent: [[Software_Master_Node]]*
