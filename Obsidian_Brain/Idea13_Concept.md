# 💡 Idea 13: RuView — WiFi Radar Arena (Zero Player Electronics)

> **The most radical architecture: players carry NOTHING electronic. The arena itself does all the sensing.**

## What is RuView?
[RuView](https://github.com/ruvnet/RuView) is an open-source WiFi sensing platform that uses **ESP32-S3** microcontrollers to analyze **WiFi Channel State Information (CSI)**. When WiFi signals travel through a room, human bodies distort them in measurable ways. By placing a mesh of ESP32-S3 nodes around the arena, the system can:
- Detect and track **all player positions** (~0.45m accuracy)
- Estimate **body pose** (17-point skeleton, 92.9% accuracy)
- Recognize **activities** (walking, crouching, standing, arm gestures)
- Work **through walls and in total darkness** — it's radio, not light
- Self-calibrate to a new room in **~30 seconds**

## How It Works for Laser Tag
1. **The Arena:** Mount 4-6 ESP32-S3 boards around the room (on walls, corners, ceiling). They create a WiFi CSI mesh that blankets the entire space.
2. **The Server (Laptop):** Runs the RuView processing pipeline (Docker-based). Receives CSI data from all nodes and reconstructs a real-time 2D/3D map of all player positions and body orientations.
3. **The Gun:** A simple toy gun with a single cheap button/switch. When pressed, it sends a signal (via a tiny ESP32-C3 SuperMini, or even just a Bluetooth remote connected to a "hub" phone) saying: *"Player 5 just fired."*
4. **The Shot Resolution:** The server knows:
   - Player 5's position (from CSI tracking)
   - Player 5's body orientation / arm direction (from pose estimation)
   - All other players' positions
   - The arena's wall layout (pre-mapped once)
   - → **Server does a ray-cast** from Player 5's position in their aim direction. If the ray hits another player's position before hitting a wall, it's a HIT.
5. **Feedback:** The server sends hit/damage notifications to players' phones (which are just in their pockets, running a lightweight notification app — NOT used as sensors or cameras).
6. **The Props:** The gun is literally just a prop with a button. The vest is purely cosmetic. The phone stays in your pocket and vibrates/beeps when you're hit.

## Why This Is Architecturally Unique

| Aspect | Every Other Idea | Idea 13 (RuView) |
| :--- | :--- | :--- |
| **Player electronics** | Phone as camera/sensor, LEDs, circuits | ❌ NOTHING. Just a button. |
| **Phone role** | Core sensor (camera, mic, etc.) | Just receives notifications in pocket |
| **Detection method** | Optical (camera, light) | Radio wave physics (WiFi CSI) |
| **Works in darkness** | Some do, some don't | ✅ Radio doesn't need light |
| **360° coverage** | Requires multiple sensors/beacons | ✅ Radio tracks full body from all angles |
| **Obstruction handling** | Camera-based (natural LOS) | ⚠️ Must be calculated in software (ray-casting against pre-mapped walls) |
| **Per-player cost** | ₹100-325 per set | ~₹0 per player (cost is in infrastructure) |
| **Infrastructure cost** | ₹0 (phones do everything) | ₹3,000-6,000 (ESP32 nodes) |

## Hardware & Cost

### Arena Infrastructure (One-Time)
| Item | Qty | Cost/Unit (INR) | Total (INR) |
| :--- | :---: | :--- | :--- |
| ESP32-S3 DevKit boards | 4-6 | 700-800 | 2,800-4,800 |
| USB power adapters + cables | 4-6 | 50 | 200-300 |
| Mounting (3M hooks, zip ties) | - | - | 100 |
| **Infrastructure Total** | | | **3,100-5,200** |

### Per-Player Equipment
| Item | Cost (INR) |
| :--- | :--- |
| Toy gun (pure prop) | 80 |
| Tiny trigger button (or Bluetooth remote) | 30-60 |
| Vest (cosmetic only, no electronics) | 0-50 |
| **Per Player Total** | **110-190** |
| **12 Players Total** | **1,320-2,280** |

### Grand Total
| Config | Infrastructure | 12 Players | TOTAL |
| :--- | :--- | :--- | :--- |
| **Minimum (4 nodes)** | 3,100 | 1,320 | **4,420 INR** ⚠️ |
| **Optimal (6 nodes)** | 5,200 | 2,280 | **7,480 INR** ❌ |

> ⚠️ **Budget Challenge:** Even the minimum config is ~₹420 over the ₹4,000 budget. The optimal 6-node setup blows the budget entirely.

### Budget Rescue Options
1. **Use ESP32-C3 SuperMini** instead of full DevKits (~₹150-200 each). 4 nodes = ₹600-800. **Total drops to ~₹2,000-3,000!** But C3 has weaker CSI capabilities than S3.
2. **Borrow/share ESP32s** — if you or friends already have ESP32 boards from other projects, the marginal cost drops to zero.
3. **Use only 3 nodes** in a smaller arena. Accuracy drops but may still be functional for a tight space.

## Links
- [[Idea13_Cons]]
- [[Accuracy_Meter]]
- [[Home]]
