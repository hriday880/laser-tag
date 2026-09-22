# Idea 6: Bluetooth RSSI Proximity — Cons

## Critical Problems

### 🔴 RSSI is Wildly Inaccurate for Position/Direction
- Bluetooth RSSI fluctuates by ±10 dBm even when devices are stationary. Moving humans, walls, and body absorption make it worse.
- You cannot reliably determine if a phone is 3m or 8m away using RSSI alone.
- Directional accuracy is essentially non-existent — RSSI tells you "roughly how far" but NOT "which direction."

### 🔴 Radio Goes Through Walls
- Bluetooth signals pass through thin walls, furniture, and barriers.
- A player could "shoot" someone hiding behind a wall because the radio signal reaches through the obstacle.
- **This completely breaks the obstruction requirement.**

### 🔴 Phone Magnetometer is Unreliable Indoors
- The compass/magnetometer in phones is heavily affected by metal structures, electronics, and electromagnetic interference in indoor environments.
- Directional aiming based on the magnetometer will drift and be inaccurate, leading to phantom hits and missed shots.

### 🟡 Android vs iOS BLE Differences
- BLE scanning behavior, intervals, and RSSI reporting vary dramatically between Android versions, manufacturers, and iOS.
- Getting consistent BLE readings across 12 different phones is a nightmare.

### 🟡 Processing Overhead
- Constantly scanning for 11 other BLE beacons while running game logic and UI will drain batteries fast and may cause lag on budget phones.

### 🟢 Minor Issues
- **BLE pairing limits:** Some older phones can only maintain a limited number of BLE connections.
- **Latency:** BLE advertising intervals (100-1000ms) add noticeable delay to hit detection.

## Verdict
**Fundamentally broken.** Radio signals ignore walls, and RSSI is far too inaccurate for a shooter game. You'd essentially be playing a proximity-based game where walls don't matter and hits feel random. Not a viable laser tag experience.

[[Idea6_Concept]] | [[Accuracy_Meter]] | [[Home]]
