# Idea 10: Ghost Mode (Retroreflective) — Cons

## Problems

### 🔴 Shape Recognition is Hard CV
- Classifying tape shapes (X, triangle, bars) from a shaky camera feed in real-time requires a trained ML model or complex contour analysis.
- This is **harder** than the simple color blob detection in Idea 9. You need shape recognition, not just "find a bright spot."
- **Partial Mitigation:** Instead of shapes, use different COLORS of retroreflective tape (red, green, silver, yellow exist). But color variety in retroreflective tape is limited — typically only silver/white, red, and yellow are widely available cheaply.

### 🟡 Flashlight Gives Away Position
- Your phone flashlight is ALWAYS on. In a dark arena, you are a walking beacon. Everyone can see where you are.
- **This changes the game dynamic significantly.** It's no longer stealth — it's a constant spotlight on the shooter.
- **Could be a feature, not a bug:** Creates an interesting "hunter becomes the hunted" mechanic. You must expose yourself to aim.

### 🟡 Flashlight Illumination Range
- Phone flashlights are powerful at close range but dim significantly beyond 5-8 meters.
- Retroreflective tape needs to be illuminated to be detected. At long range, the reflection may be too dim.
- **Mitigation:** This naturally creates a "range" mechanic — you can only shoot targets within your flashlight's range.

### 🟡 Limited Player ID Combinations
- With only 2-3 colors of reflective tape available, and simple shapes, getting 12 unique identifiers is challenging.
- **Mitigation:** Combine color + position (e.g., red stripe on chest + silver stripe on shoulders = Player 7).

### 🟢 Minor Issues
- **Tape peeling:** Retroreflective tape's adhesive may weaken with sweat. Use safety pins or sewing as backup.
- **Angle sensitivity:** Retroreflection works best when the light source and camera are very close together (they are on a phone, so this is fine) and the tape is roughly perpendicular to the viewer.

## Verdict
**The shape/player identification problem is a significant weakness.** If you can solve the ID problem (limited color combinations or a lightweight ML model), this is the cheapest possible build. But Idea 9's blink-code LEDs are a more reliable identification mechanism.

[[Idea10_Concept]] | [[Home]]
