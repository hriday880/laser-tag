# Idea 4: Sound-Based (Ultrasonic Ping)

## The Core Concept
Instead of light, use **sound**. Each gun emits a unique ultrasonic frequency (above human hearing, ~18-22kHz) when fired. The phone's microphone picks it up.

## How It Works
1. **The Gun:** Contains a small piezo buzzer that emits a specific ultrasonic frequency when the trigger is pulled.
   - Gun 1 emits 18.0 kHz
   - Gun 2 emits 18.5 kHz
   - Gun 3 emits 19.0 kHz
   - etc.
2. **The Phone (Sensor):** The phone's microphone listens for ultrasonic frequencies. When it detects one, it performs a Fast Fourier Transform (FFT) to identify the exact frequency, which tells it which gun fired.
3. **Hit Registration:** Phone identifies the frequency → knows who shot → reports to server.

## Why Consider This?
- **Works in complete darkness** — sound doesn't need light.
- **Phones already have microphones** — no camera compatibility issues.
- **Cheap hardware** — piezo buzzers cost 5-10 INR each.
- **Unique identification** — different frequencies = different shooters.

## Links
- [[Idea4_Cons]] — The problems with this approach (spoiler: there are many).
