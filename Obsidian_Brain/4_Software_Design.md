# Software Design

Building the mobile application is where you will save the money, as software replication is free.

## Tech Stack Recommendation
- **Engine:** Unity3D or React Native. Unity might be easier for integrating OpenCV (Open Source Computer Vision) and game logic.
- **Vision Library:** OpenCV (specifically the `aruco` module).
- **Networking:** UDP sockets or WebSockets.

## The Hit Detection Algorithm (The Magic)
1. **Crosshair Definition:** Define a virtual box in the center of the screen (e.g., center 20% of the image).
2. **Scanning:** As the camera feed runs, OpenCV looks for ArUco markers in the frame.
3. **Trigger Event:** When the Volume Up event (Bluetooth trigger) fires:
   - Check if an ArUco marker is currently detected.
   - Calculate the center X,Y coordinates of the detected marker.
   - Check if those X,Y coordinates fall within our "Crosshair" bounding box.
   - Check the size of the marker (to ensure the target is within range. If the marker is too small, they are too far away).
4. **Hit Confirmation:** If all conditions are met, extract the ID embedded in the ArUco marker (e.g., Marker ID 4 belongs to Player 4) and send the hit to the server.

## Body Cam Implementation
Most modern camera APIs allow you to split the stream: one stream goes to the image analyzer (downscaled for fast processing), and the other high-res stream is encoded to an MP4 file on the device storage.

## Anti-Cheat
- Since the server logs all shots, and phones record the video, players can review the body cam footage after the match to settle disputes!
