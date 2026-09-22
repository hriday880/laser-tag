# Idea 4: Sound-Based — Cons

## Critical Problems

### 🔴 Sound Goes Through Walls
- This is the **fatal flaw**. Sound waves travel around corners and through thin barriers.
- A player hiding behind a wall can still be "hit" because the ultrasonic ping reaches their mic through or around the obstacle.
- **This completely breaks the obstruction requirement.**

### 🔴 No Directional Aiming
- Sound from a piezo buzzer radiates in all directions (omnidirectional).
- If you fire, EVERY phone in the room hears it, not just the one you're aiming at.
- There's no concept of "aiming" — pulling the trigger hits everyone in range simultaneously.

### 🔴 12-Player Frequency Crowding
- Phone microphones can reliably capture up to ~20-22 kHz (some only 16 kHz).
- Fitting 12 unique frequencies in the 18-22 kHz band means each frequency is only 333Hz apart.
- In a noisy, echo-filled arena, the FFT will struggle to distinguish Gun 7 (20.0 kHz) from Gun 8 (20.3 kHz), especially with reverb and reflections.

### 🟡 Microphone Quality Varies Wildly
- Budget phones have terrible microphones that may not even pick up frequencies above 16 kHz.
- Some phones apply noise cancellation that actively filters out ultrasonic frequencies.

### 🟡 Echoes and Reverb
- Indoor arenas have hard walls that reflect sound, creating echoes.
- A single shot could register as multiple hits due to reflected sound waves bouncing around.

### 🟢 Minor Issues
- **Player discomfort:** Some people (especially younger players) can hear up to 20kHz. The "silent" buzzer might be audible and annoying.
- **Ambient noise:** Music, shouting, footsteps could interfere with detection.

## Verdict
**Fundamentally broken.** Sound cannot provide line-of-sight enforcement. The lack of directionality makes "aiming" meaningless. Creative concept but physically impossible to make work for a shooter game.

[[Idea4_Concept]] | [[Accuracy_Meter]] | [[Home]]
