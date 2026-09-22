# Idea 8: LED Color Beacon — Cons

## Problems

### 🟡 Color Differentiation Limits
- With only R, G, B LEDs, the number of unique 2-LED combos is limited: RR, RG, RB, GG, GB, BB = 6 combos.
- For 12 players, you need to add a second dimension like **blink pattern** (steady vs slow flash vs fast flash), giving 6 colors × 2-3 patterns = 12-18 unique identities.
- Blink pattern detection adds software complexity (need to observe over multiple frames).

### 🟡 Color Bleed on Cheap Cameras
- Budget phone cameras can struggle to distinguish Red from Orange, or Green from Yellow-Green in certain conditions.
- **Mitigation:** Use only pure R, G, B (highly distinct wavelengths) and keep the arena otherwise dark.

### 🟡 LED Visibility Through Smoke/Haze
- If you use smoke machines for atmosphere, thick smoke scatters LED light, creating a "glow cloud" effect that makes pinpointing the exact LED location harder.
- **Mitigation:** Use moderate haze, not thick fog.

### 🟢 Minor Issues
- **LED orientation:** If a player's beacon is slightly angled away, the light intensity drops. Diffused LEDs help but aren't perfect.
- **Battery replacement:** CR2032 batteries need to be replaced between game sessions. Keep spares.
- **Beacon damage:** Physical gameplay could knock LEDs loose. Hot glue everything generously.

## What This Idea Gets Right
- ✅ Works in the dark (darkness helps, not hurts)
- ✅ Line-of-sight naturally enforced (light blocked by walls)
- ✅ 360° coverage (multiple beacons)
- ✅ Player identification (color + blink pattern)
- ✅ Cheapest hardware of all ideas
- ✅ Simplest software of all ideas
- ✅ Works on all phones (no IR filter issues)

## Verdict
**This is the strongest idea overall for the phone-on-chest paradigm.** The cons are all yellow/green (solvable), with no red dealbreakers. The 12-player color limit is solvable with blink patterns. (Now surpassed by the phone-as-gun Ideas 9-11.)

[[Idea8_Concept]] | [[Accuracy_Meter]] | [[Home]]
