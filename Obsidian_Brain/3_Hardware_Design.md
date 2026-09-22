# Hardware Design

To stay under ~333 INR per set, we have to get creative and hack existing cheap items.

## The Vest (Chest Mount)
We need a way to hold the phone securely on the chest while leaving the camera exposed.
**Materials:**
- Elastic straps (local tailor shop).
- Plastic quick-release buckles.
- A cheap waterproof mobile pouch (the clear plastic ones used for swimming).
**Assembly:**
Sew or superglue the elastic straps to the waterproof pouch to create a simple chest harness. The phone slips into the pouch, camera facing out.
*Cost: ~80 INR per vest.*

## The Target Markers
**Materials:**
- A4 Paper and a Printer.
- Lamination or clear packing tape (to make them sweat-proof).
- Safety pins or velcro to attach to the front/back of players.
**Design:** Use a 5x5 ArUco marker dictionary. They are highly optimized for fast computer vision detection. Print them as large as possible (e.g., 15cm x 15cm) so they can be detected from a distance.
*Cost: ~20 INR per player.*

## The Gun
**Materials:**
- Cheap plastic toy gun (e.g., a basic cap gun or water gun from a wholesale market like Sadar Bazaar).
- Bluetooth Selfie Remote (very cheap wholesale).
**Assembly:**
1. Gut the toy gun (remove water tanks/springs).
2. Take apart the Bluetooth remote, expose the small push button on the PCB.
3. Solder two wires to the button's contacts.
4. Wire those to a microswitch positioned behind the gun's physical plastic trigger.
5. Secure the Bluetooth PCB and battery inside the empty gun shell.
**How it works:** When the player pulls the physical trigger, it closes the circuit on the Bluetooth remote, which sends a wireless "click" to the phone.
*Cost: ~100 INR (Gun) + ~60 INR (Remote) = ~160 INR.*
