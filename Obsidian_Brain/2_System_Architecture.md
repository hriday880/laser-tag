# System Architecture

The system consists of three main components: The Gun (Input), The Phone (Client), and the Router/Laptop (Server).

## 1. The Gun (Trigger Input)
We cannot wire the gun directly to the phone easily via USB because everyone has different phones (USB-C, Lightning, Micro-USB).
**Solution:** A cheap Bluetooth camera shutter remote.
- The remote pairs to the phone.
- When pressed, it sends a "Volume Up" command.
- The custom Laser Tag app listens for the "Volume Up" hardware button press and triggers the "Fire" action.

## 2. The Phone (Client App)
- Strapped to the chest, camera facing outward.
- **Roles:**
  - **Vision:** Continuously scans the camera feed for ArUco markers.
  - **Body Cam:** Saves the video feed locally to the gallery.
  - **Feedback:** Screen turns Red/Blue, flashes, plays sounds, and vibrates to give feedback to the player.
  - **Networking:** Connects to a local WiFi network to report hits and receive damage.

## 3. The Server (Local Network)
You don't want to rely on Mobile Data (latency, spotty indoor reception, data costs).
- **Setup:** Bring a standard home WiFi router to the arena. No internet connection is needed.
- **Host:** A laptop running a lightweight Node.js or Python WebSocket server.
- **Function:** 
  - Keeps track of game state, scores, and health.
  - Receives a message: `Player 1 shot Player 4`.
  - Sends message to Player 4: `You have been hit, lose 10 HP. Disable gun for 3 seconds.`
