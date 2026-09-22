# Idea 2: Time-Synced Light Strike (Dark Arena)

Since the arena will be dark, computer vision and markers won't work well. However, darkness is actually an *advantage* if we switch from reading patterns to reading **light bursts**.

## The Core Concept
Instead of scanning for QR codes, we use **focused flashes of light** and **server-side time matching**.

1. **The Weapon:** A toy gun equipped with a highly focused LED (like a zoomable flashlight or a diffused laser pointer).
2. **The Sensor:** The player's smartphone, strapped to their chest with the camera facing outward.
3. **The Logic:**
   - When Player A pulls the trigger, their gun emits a split-second flash of focused light.
   - At the exact same millisecond, Player A's phone tells the central server: *"I just fired my weapon."*
   - The light beam hits Player B in the dark.
   - Player B's chest-mounted phone camera detects a sudden, massive spike in brightness.
   - Player B's phone tells the server: *"I was just hit by a flash of light."*
   - The Server matches the timestamps. If Player A fired at the exact moment Player B saw a flash, **Player A hit Player B!**

## Why this works perfectly in the dark
- **No Motion Blur Issues:** We aren't reading complex patterns, just overall brightness.
- **Low Compute Power:** Calculating the average brightness of a camera frame is incredibly lightweight compared to running OpenCV.
- **Obstruction Solved:** Light cannot pass through walls. If you are behind a barrier, your phone is in the shadow and won't detect the flash.

## Links
- [[Idea2_Cons]] — Problems with this approach
- [[Idea2_Architecture]] | [[Idea2_Hardware]] | [[Idea2_Budget]]
- [[Home]] | [[Accuracy_Meter]]
