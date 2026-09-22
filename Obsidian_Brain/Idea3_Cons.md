# Idea 3: IR LED + Phone Camera — Cons

## Critical Problems

### 🔴 Back Shot Problem (Still Exists!)
- The phone camera only faces **one direction** (forward from the chest).
- A shot to the back, sides, or legs won't be detected.
- **Workaround:** Add cheap reflective panels or small mirrors on shoulders/back to bounce IR toward the front camera. Hacky and unreliable.

### 🔴 IR Filter on Newer Phones
- Many modern flagship phones (iPhone 12+, Samsung S21+) have **IR-cut filters** on the camera to improve photo quality. These block IR light entirely.
- Older / budget phones are more likely to see IR, but you can't guarantee all 12 players have compatible phones.
- **Test required:** Every player's phone must be tested beforehand with a TV remote to confirm IR visibility.

### 🟡 Decoding Pulse Patterns via Camera
- Phone cameras typically capture at 30fps. Decoding a rapid pulse pattern (like a TV remote signal) from 30fps video is extremely difficult — the pulses happen at ~38kHz, way faster than 30fps can capture.
- **Workaround:** Use much slower pulse patterns (e.g., 200ms per pulse). But this means a "shot" takes ~1 second to transmit, making the game feel sluggish.

### 🟡 Requires Electronics Knowledge
- Wiring 555 timers or programming ATtiny85 microcontrollers requires soldering skills and basic electronics knowledge.
- This is the most technically complex gun build of all the ideas.

### 🟢 Minor Issues
- **IR LED Range:** Cheap IR LEDs have limited range (~3-5m without a lens). Need a focusing mechanism.
- **Ambient IR:** Sunlight contains IR. If any sunlight leaks into the arena, it could cause false positives.

## Verdict
**The IR filter issue on modern phones is a serious compatibility risk.** The pulse decoding problem at 30fps makes identifying individual shooters very challenging. Promising concept but technically complex.

[[Idea3_Concept]] | [[Accuracy_Meter]] | [[Home]]
