# Idea 6: Bluetooth RSSI Proximity + Gyroscope Aiming

## The Core Concept
Forget cameras, light, and sound entirely. Use **radio signals** and **phone sensors**.

Each phone constantly broadcasts its Bluetooth signal. When a player fires, their phone uses its **gyroscope + compass** to determine the direction it's pointing, and checks which enemy phones are in that direction based on Bluetooth signal triangulation.

## How It Works
1. **All 12 phones** continuously broadcast Bluetooth Low Energy (BLE) beacons with their Player ID.
2. **Aiming:** The shooter holds their phone like a gun (or the phone is attached to the gun pointing forward). The phone's gyroscope and magnetometer know which direction it's facing.
3. **Firing:** When the trigger is pulled:
   - The phone reads RSSI (Received Signal Strength Indicator) from all nearby BLE beacons.
   - It determines which enemy phone is roughly in the direction the gun is pointing.
   - It calculates if that phone is within "range" based on signal strength.
4. **Hit Calculation:** Server cross-references the shooter's aim direction with known player positions (estimated from BLE triangulation between all phones).

## Why Consider This?
- **No line-of-sight hardware needed** — all processing is in software.
- **Zero additional hardware cost** — just phones and Bluetooth remotes.
- **Works in any lighting** — radio doesn't care about darkness.

## Links
- [[Idea6_Cons]] — The (many) problems with this approach.
