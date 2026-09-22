# Idea 2: Time-Synced Light Strike — Cons

## Critical Problems

### 🔴 Back Shots are Impossible (or Require 2 Phones)
- The phone is on the **chest**. If someone shoots you from behind, your chest-mounted camera won't see the flash.
- **Workaround:** Strap a second phone to the back. But that requires players to bring TWO phones, which is unrealistic for 12 people.

### 🔴 Multi-Player Confusion (Who Shot Whom?)
- If 3 players fire at the same time, and Player B's phone detects a flash, the server has **no way to know which of the 3 shooters actually hit Player B**.
- The timestamp matching only tells you *someone* fired and *someone* got hit at the same time. It doesn't prove a direct line between shooter and target.
- In a 12-player game, simultaneous shots will be extremely common.

### 🔴 False Positives from Ambient Light
- Other guns flashing nearby, reflections off walls, or even phone screens can trigger false "I was hit" events.
- The colored gel filter helps, but cheap phone cameras aren't great at distinguishing specific color spikes in a noisy dark environment.

### 🟡 Time Sync Precision
- WiFi-based NTP synchronization between 12 phones of different makes, OS versions, and WiFi chips will have jitter of 10-50ms.
- In a fast-paced game, 50ms of clock drift can cause missed hits or ghost hits.

### 🟡 Friendly Fire
- The system has **zero directional awareness**. If a teammate fires their flash near you, your phone detects it and you take damage from your own team.

### 🟢 Minor Issues
- **LED Battery Drain:** Constant bright flashes will drain the flashlight's small battery quickly during a long game.
- **Flash Blinding:** Bright flashes in a dark room could be disorienting or annoying for players.

## Verdict
**The "who shot whom" problem is fundamentally unsolvable with just timestamps and brightness detection.** This idea is creative but has too many logical holes for a competitive game.

[[Idea2_Concept]] | [[Accuracy_Meter]] | [[Home]]
