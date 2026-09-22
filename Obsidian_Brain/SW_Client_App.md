# 🟩 The Client App (The Gun)

> [!abstract] Overview
> The mobile app running on the player's phone. It acts as the viewport (Scope), the sensor (Vision), and the communicator (Network).

## The Core Loop (60 FPS)
The app runs a continuous render loop. 

1. **Render Camera Background:** The raw camera feed is drawn to the screen.
2. **Overlay HUD:** Draw the crosshair, health bar, ammo count, and team color borders.
3. **Scan (Background Thread):** Pass every $n^{th}$ frame (e.g., 15 fps to save battery) to the OpenCV processor to find ArUco markers.
4. **Trigger Listener:** Wait for a hardware volume-button press or a screen tap.

## How the Trigger Works

```python
# Pseudo-code for trigger logic
def on_trigger_pulled():
    if current_ammo > 0 and not is_reloading and not is_dead:
        current_ammo -= 1
        play_sound("shoot.wav")
        trigger_haptic("light_kick")
        
        # Check vision system AT THIS EXACT MILLISECOND
        target_marker_id = CV_Engine.get_marker_in_crosshair()
        
        if target_marker_id is not None:
            # We hit a marker! Tell the server.
            Network.send("HIT_REPORT", {
                "shooter_id": my_player_id,
                "target_marker": target_marker_id
            })
        else:
            # Missed.
            pass
```

## The HUD (Heads Up Display)
- **Crosshair:** A dynamic UI element in the exact center of the screen. Expands when moving, turns <span style="color: red">Red</span> briefly when a hit is confirmed by the server (Hitmarker!).
- **Damage Indicator:** When receiving a `DAMAGE` packet from the server, a bloody/red vignette flashes around the edges of the screen, and the phone vibrates heavily.
- **Ammo/Reload:** If ammo hits 0, player must swipe down or press a specific button to reload (triggers a 2-second cooldown).

## Hardware Integration
- **Volume Button Hook:** On Android/iOS, apps can override the volume up/down buttons. We bind Volume Up to `FIRE`.
- **OTG Serial (Optional):** If using the ESP32 trigger (Idea 14c), the app reads serial data from the USB port.

---
*Parent: [[Software_Master_Node]]*
