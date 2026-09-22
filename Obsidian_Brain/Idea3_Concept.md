# Idea 3: IR LED + Phone Camera

## The Core Concept
Most smartphone cameras can **see Infrared (IR) light**, even though human eyes cannot. Try it: point a TV remote at your phone camera and press a button — you'll see a purple/white flash on screen.

This means we can use **IR LEDs** as the "laser" in our laser tag, and the phone camera as the sensor — and it works **perfectly in the dark!**

## How It Works
1. **The Gun:** Contains a focused IR LED (harvested from a cheap TV remote or bought in bulk). When the trigger is pulled, the IR LED fires a coded burst (like a TV remote signal).
2. **The Vest Phone:** The phone camera faces outward. It continuously monitors for sudden IR light spikes. Since IR is invisible to the human eye but visible to the camera, the dark arena doesn't matter.
3. **Encoding the Shooter:** IR LEDs can be pulsed in patterns (just like a TV remote sends different codes for different buttons). Each gun pulses a unique pattern:
   - Gun 1: Short-Short-Long
   - Gun 2: Short-Long-Short
   - Gun 3: Long-Short-Short
   - etc.
4. **Decoding:** The phone camera reads the pulse pattern and identifies WHICH gun shot it.
5. **Obstruction:** IR light cannot pass through walls or solid objects. Line of sight is naturally enforced.

## Why This is Better Than Idea 2
- **Solves "Who shot whom"** — each gun has a unique IR code.
- **Works in the dark** — IR is invisible to eyes but visible to cameras.
- **No timestamp matching needed** — the camera directly reads the shooter's identity.

## Links
- [[Idea3_Hardware]] — How to build the IR guns cheaply.
- [[Idea3_Cons]] — The problems with this approach.
