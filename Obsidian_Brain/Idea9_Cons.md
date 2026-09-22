# Idea 9: FPS Paradigm — Cons

## Problems

### 🟡 Phone Handling During Physical Play
- Players are running, dodging, crouching. Holding a phone while doing this risks drops and screen cracks.
- **Mitigation:** Require phone cases. Use a wrist strap. The waterproof pouch from other ideas can work as a grip protector.

### 🟡 Blink Code Decode Time
- At 5Hz blink rate with 4-bit codes, decoding takes ~0.8 seconds. During this time, the player must keep the crosshair roughly on the target.
- **Mitigation:** Start detecting the moment LEDs enter the frame (not just at trigger pull). Cache partially-decoded patterns. When trigger fires, use the most recently decoded ID. This reduces perceived lag to near-zero.

### 🟡 Battery Life
- Running the camera + screen + network + game logic continuously will drain the phone battery.
- A typical phone lasts ~2 hours of continuous camera use.
- **Mitigation:** Each game round is 5-15 minutes. Between rounds, phones charge or rest. 2 hours covers many rounds.

### 🟡 555 Timer Circuit Complexity
- Building 12 unique blink-code circuits with 555 timers requires some electronics knowledge.
- **Mitigation:** Use the simplest approach — just 2 LEDs of different colors (no blinking needed). With R, G, B in 2 positions you get enough combos for 12 players. Or use a ₹15 ATtiny85 programmed with a unique blink pattern via USB.

### 🟢 Minor Issues
- **Screen visibility in dark:** The bright phone screen might give away the player's position. **Mitigation:** Reduce screen brightness to minimum, use dark UI themes with dim red HUD elements.
- **One-handed aiming:** Holding a phone steady with one hand while running is harder than a two-handed gun grip. **Mitigation:** Use both hands, or 3D-print/cardboard a simple phone grip.

## What This Idea Gets Right
- ✅ Works perfectly in the dark
- ✅ Line-of-sight enforced by camera
- ✅ **360° coverage** (beacons on all sides)
- ✅ **Back shots work** (shooter detects target, not the reverse)
- ✅ Player identification via blink codes
- ✅ Natural aiming (point the phone)
- ✅ Full HUD on screen (health, ammo, crosshair)
- ✅ Body cam / kill cam built in
- ✅ **Cheapest build of ALL ideas** (₹1,416–2,136 for 12 sets)
- ✅ Works on ALL phones (just needs a camera)
- ✅ Completely safe

## Verdict
**No red dealbreakers.** All cons are solvable yellow/green issues. This is the strongest overall idea by a significant margin.

[[Idea9_Concept]] | [[Home]]
