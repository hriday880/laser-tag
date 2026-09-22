# Idea 8: LED Color Beacon + Phone Camera (Dark Arena Optimized)

## The Core Concept
**The best hybrid for a dark arena.** Instead of reading complex printed markers (which need light), each player wears a small, cheap, **always-on colored LED beacon** on their chest/back. The phone camera sees these bright colored dots in the dark and identifies targets.

## How It Works
1. **The Beacon:** Each player wears 2-3 small colored LEDs (front, back, and optionally shoulders). Each player gets a unique color combination:
   - Player 1: Red-Red
   - Player 2: Red-Green
   - Player 3: Green-Green
   - Player 4: Blue-Red
   - Player 5: Blue-Green
   - Player 6: Blue-Blue
   - (With RGB LEDs, combinations scale to 12+ easily)
2. **The Phone Camera:** Faces outward from the chest. In a dark room, bright LED dots are the ONLY things visible in the camera feed — making detection trivially easy compared to a lit environment.
3. **Firing:** When the trigger is pulled, the phone checks the current camera frame:
   - Are there any colored LED dots in the crosshair (center of frame)?
   - What color combination is it? → Identifies the target player.
   - How large are the dots? → Estimates distance (range check).
4. **Obstruction:** LEDs are light sources. They obey line of sight — walls block them completely.

## Why This Might Be the Best Idea
- **Darkness is an ADVANTAGE** — colored LEDs are trivially easy to detect in a dark frame. No complex CV needed, just color blob detection.
- **Solves "who shot whom"** — unique color combos identify each player.
- **360° coverage** — LEDs on front AND back mean you can be shot from any angle (the SHOOTER's phone camera sees YOUR beacon).
- **Ultra-cheap hardware** — LEDs cost 2-5 INR each.
- **Low processing power** — Color detection is 100x simpler than ArUco decoding.
- **Works on ALL phones** — no IR filter issues, no special mic requirements.

## Links
- [[Idea8_Hardware]] — How to build the beacons.
- [[Idea8_Cons]] — The problems with this approach.
