# Feasibility Analysis

## Is it possible?
**Yes.** The idea of using a smartphone as the core computational and sensory unit is the *only* way to achieve this on a 4,000 INR budget for 12 players. If you had to buy microcontrollers, IR sensors, displays, and cameras for 12 sets, you would easily exceed 20,000 INR.

By adopting a **BYOD (Bring Your Own Device)** approach, you offload the most expensive components (screen, processor, camera, battery, networking) to the players themselves.

## How to solve "Line of Sight" and "Obstructions"
Traditional laser tag uses Infrared (IR) LEDs and IR receivers. If a wall is in the way, the IR beam hits the wall.
Since phones don't typically have IR receivers, we must use the **Camera + Computer Vision (CV)**.

### The Computer Vision Approach
1. Every player wears a highly visible, unique marker on their chest and back (like an [ArUco marker](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html) or a brightly colored QR-like code).
2. The phone on the player's chest is constantly recording (acting as the body cam).
3. When the player pulls the trigger on their "gun", the phone analyzes the current camera frame.
4. If it detects an enemy's marker in the center of the frame, it considers it a **HIT**.
5. Since a camera cannot see through walls, the obstruction problem is naturally solved! If the camera can't see the marker because of a wall, you can't shoot them.

## Key Challenges
1. **Motion Blur:** Players running will cause blurry camera frames. We need to use markers that are easy to detect even with slight blur.
2. **Lighting:** This setup will require a decently lit arena. It will not work well in pitch black without external lighting (though the phone flashlight could be used!).
3. **Trigger Input:** Getting a physical toy gun to tell the phone to "fire" without expensive electronics.

## See Also
- [[Idea1_Cons]] — Problems with this approach
- [[2_System_Architecture]] | [[3_Hardware_Design]] | [[4_Software_Design]] | [[5_Budget_Breakdown]]
- [[Home]] | [[Accuracy_Meter]]
