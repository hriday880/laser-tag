# Idea 7: Laser Pointer + Phone Screen Detection

## The Core Concept
The simplest possible approach. The gun is literally just a **laser pointer**. The "sensor" is the phone's **screen/front camera**.

## How It Works
1. **The Gun:** A cheap laser pointer (red or green) mounted inside a toy gun shell. Trigger activates the laser.
2. **The Target:** The phone is strapped to the chest with the **screen facing outward**. The phone's front-facing camera or ambient light sensor monitors for a laser dot landing on or near the screen.
3. **Hit Detection:**
   - **Method A (Front Camera):** The front camera watches for a sudden, intensely bright point of light (the laser dot). If detected, it's a hit.
   - **Method B (Screen Touch):** Some research shows that certain lasers can trigger capacitive touchscreen events (though this is unreliable).
   - **Method C (Light Sensor):** The ambient light sensor detects a spike in brightness when a laser shines directly on it.
4. **Obstruction:** Lasers are perfectly line-of-sight. Walls block them completely.

## Why Consider This?
- **Perfect line-of-sight** — lasers are the gold standard for directional accuracy.
- **Extremely cheap** — laser pointers cost 20-30 INR.
- **Works in the dark** — laser dots are MORE visible in darkness.
- **Looks cool** — visible laser beams in a smoky/hazy dark arena look like actual sci-fi weapons.

## Links
- [[Idea7_Cons]] — The problems with this approach.
