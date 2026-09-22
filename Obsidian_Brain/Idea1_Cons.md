# Idea 1: ArUco Marker + Computer Vision — Cons

## Critical Problems

### 🔴 Doesn't Work in the Dark
- This is the **dealbreaker**. ArUco markers need decent, even lighting to be reliably detected by OpenCV.
- A dark arena makes this approach fundamentally broken unless you flood the arena with light (which defeats the laser tag atmosphere).

### 🟡 Motion Blur
- Players sprinting will cause significant motion blur on the camera feed.
- ArUco markers need sharp, clean edges to be decoded. A blurry frame = missed detection = frustrating gameplay.

### 🟡 Processing Power
- Running OpenCV ArUco detection in real-time at 30fps requires a reasonably powerful phone.
- Budget/older Android phones (which many players in a group of 12 might have) could struggle, causing lag between trigger pull and hit detection.

### 🟡 Detection Range
- For a 15cm marker to be reliably detected, the target needs to be within ~5-8 meters. Beyond that, the marker becomes too small in the camera frame.
- This limits arena size or forces you to print comically large markers.

### 🟢 Minor Issues
- **Marker Damage:** Paper markers can tear, get sweaty, or curl, making them unreadable.
- **Camera FOV:** The phone's camera has a fixed field of view. If the target is slightly off to the side, the camera won't see the marker even if the player's eyes can.
- **Phone Orientation:** If the phone shifts slightly in the chest pouch, the camera might point at the floor or ceiling.

## Verdict
**Not viable for a dark arena.** Good concept for a well-lit outdoor or brightly-lit indoor space only.

[[1_Feasibility_Analysis]] | [[Accuracy_Meter]] | [[Home]]
