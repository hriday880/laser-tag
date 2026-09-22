# Architecture (Light Strike)

## 1. The Server (The Matchmaker)
A simple local laptop running a lightweight Node.js server (UDP or WebSockets) connected to a standard WiFi router.
- **Time Syncing:** All phones sync their internal clocks with the server at the start of the game (NTP - Network Time Protocol) to ensure millisecond accuracy.
- **The Matcher:** 
  - Receives `FIRE_EVENT(Player_ID, Timestamp)`
  - Receives `LIGHT_DETECTED_EVENT(Player_ID, Timestamp)`
  - If the timestamps are within ~100 milliseconds of each other, it registers a hit, deducts health from the target, and awards points to the shooter.

## 2. The Phone (The Target Sensor)
- Worn on the chest.
- Constantly loops through camera frames.
- Analyzes the frame for a sudden jump in *Luma* (brightness).
- To prevent ambient light from triggering it, the app can look for a specific color flash. For example, if you put a Red gel filter over the gun's flashlight, the phone only looks for a sudden spike in *Red light*.

## 3. The Gun (The Emitter & Trigger)
The gun needs to do two things simultaneously when the trigger is pulled:
1. Turn on the flashlight for 100ms.
2. Send a Bluetooth signal to the shooter's phone to log the `FIRE_EVENT`.
