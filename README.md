# Laser Tag 🔫

> **DIY Smartphone Laser Tag** — A full-stack augmented reality laser tag system using ArUco markers, computer vision, and your phone as the gun.

## Overview

This project turns any dark room into a laser tag arena using nothing but smartphones and printed ArUco markers. Players hold their phones like FPS weapons — the camera detects enemy markers through computer vision, and a central Python server manages teams, health, and hit validation over local WiFi.

**Budget:** Under ₹4,000 INR for 8 complete player sets.

## Architecture

```
┌──────────────┐         WebSocket (JSON)         ┌──────────────┐
│  Player Gun  │◄──────────────────────────────────►│  Game Server │
│  (Unity App) │         Local WiFi                │  (Python)    │
│              │                                   │              │
│ ┌──────────┐ │                                   │ ┌──────────┐ │
│ │ Camera   │ │  Trigger → ArUco Detection →      │ │ Team Mgr │ │
│ │ + OpenCV │ │  HIT_REPORT if crosshair is       │ │ HP Track │ │
│ │ ArUco    │ │  inside marker polygon             │ │ Hit Valid│ │
│ └──────────┘ │                                   │ └──────────┘ │
└──────────────┘                                   └──────────────┘
```

## Project Structure

```
Software/
├── Server/
│   ├── server.py          # Python WebSocket game server
│   ├── test_client.py     # Mock client for testing (simulates 2v1 match)
│   └── requirements.txt
│
├── CV_Test/
│   ├── cv_test.py         # Standalone webcam ArUco + crosshair test
│   └── requirements.txt
│
└── Unity_Client/
    └── Scripts/
        ├── ArUcoVision.cs            # OpenCV camera + ArUco detection
        ├── LaserTagGun.cs            # Weapon logic, HUD, HP, ammo
        └── LaserTagNetworkManager.cs # WebSocket client for Unity
```

## Quick Start

### 1. Run the Server
```bash
cd Software/Server
pip3 install -r requirements.txt
python3 server.py
```
You should see:
```
==================================================
  LASER TAG SERVER
  Listening on ws://0.0.0.0:8765
==================================================
```

### 2. Test It (No Phones Needed)
In a separate terminal:
```bash
cd Software/Server
python3 test_client.py
```
This simulates 3 players (2 Red vs 1 Blue) joining and shooting. You'll see hit confirmations, damage events, and friendly fire being blocked.

### 3. Test Computer Vision (Laptop Webcam)
```bash
cd Software/CV_Test
pip3 install -r requirements.txt
python3 cv_test.py
```
Print an ArUco marker (DICT_4X4_50, IDs 0-7) and aim your webcam at it. The crosshair turns red when you're locked on.

### 4. Unity Client
1. Open Unity (2022.3 LTS or later)
2. Import [OpenCV for Unity](https://assetstore.unity.com/packages/tools/integration/opencv-for-unity-21088) from the Asset Store
3. Import [NativeWebSocket](https://github.com/endel/NativeWebSocket) via Unity Package Manager
4. Copy the 3 scripts from `Unity_Client/Scripts/` into your Unity project
5. Set the `serverUrl` in `LaserTagNetworkManager` to your laptop's local IP (e.g., `ws://192.168.1.100:8765`)
6. Build for Android/iOS

## How It Works

1. **Trigger Pull (Volume Button):** Player presses Volume Up/Down on their phone
2. **ArUco Detection:** OpenCV scans the current camera frame for ArUco markers
3. **Crosshair Test:** Point-in-Polygon math checks if the screen center falls inside any detected marker
4. **Hit Report:** If the crosshair is on a marker, the phone sends `{ type: "HIT_REPORT", target_marker_id: X }` to the server
5. **Server Validation:** The server checks the shooter is alive, the target is alive, and they're on different teams
6. **Damage:** Server deducts HP, sends `DAMAGE_RECEIVED` to victim and `HIT_CONFIRMED` to shooter
7. **Death & Respawn:** At 0 HP, the player dies for 10 seconds, then auto-respawns

## Team Modes

The server supports **any team configuration**:
- `TEAM_RED` vs `TEAM_BLUE` (4v4)
- `TEAM_RED` vs `TEAM_BLUE` vs `TEAM_GREEN` (3v3v2)
- 8 unique teams (Free-For-All)
- 1 vs 7 (Juggernaut / Zombie mode)

Teams are created dynamically — just pass the team name in the JOIN message.

## Network Protocol

| Direction | Type | Purpose |
|-----------|------|---------|
| Client → Server | `JOIN` | Register player with name, marker_id, team |
| Client → Server | `HIT_REPORT` | Report a hit (target_marker_id) |
| Server → Client | `JOIN_ACK` | Confirm registration |
| Server → Client | `HIT_CONFIRMED` | Tell shooter the hit landed |
| Server → Client | `DAMAGE_RECEIVED` | Tell victim they took damage |
| Server → Client | `DEATH_EVENT` | Player died, respawn timer starts |
| Server → Client | `RESPAWN` | Player is back alive |
| Server → All | `STATE_SYNC` | Periodic game state broadcast |

## Hardware (Physical Gun Mount)

See the `Obsidian_Brain/` folder for detailed hardware concepts including:
- **Idea 14b:** 3D-printed periscope gun mount (phone lies flat, mirror reflects camera forward)
- **Idea 14c:** ESP32-C3 SuperMini for haptic recoil and muzzle flash LEDs

## License

MIT
