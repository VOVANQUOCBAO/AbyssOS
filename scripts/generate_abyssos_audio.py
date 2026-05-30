import math
import random
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "audio" / "abyssos-ambience.wav"
SAMPLE_RATE = 22050
DURATION = 30.2


def clamp(value: float) -> int:
    value = max(-1.0, min(1.0, value))
    return int(value * 32767)


def main() -> None:
    random.seed(734021)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    frame_count = int(SAMPLE_RATE * DURATION)
    with wave.open(str(OUTPUT), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)

        phase_1 = 0.0
        phase_2 = 0.0

        for index in range(frame_count):
            time_s = index / SAMPLE_RATE

            # Low underwater drone
            phase_1 += (2 * math.pi * 43.0) / SAMPLE_RATE
            phase_2 += (2 * math.pi * 86.0) / SAMPLE_RATE
            drone = math.sin(phase_1) * 0.22 + math.sin(phase_2) * 0.08

            # Slow swells to avoid a flat tone
            swell = math.sin(2 * math.pi * 0.07 * time_s) * 0.18

            # Filtered noise texture for water pressure feel
            noise = (random.random() * 2 - 1) * 0.06

            # Sparse sonar-like blips every ~6 seconds
            sonar = 0.0
            pulse_position = time_s % 6.0
            if pulse_position < 0.22:
                envelope = 1.0 - (pulse_position / 0.22)
                sonar = math.sin(2 * math.pi * 640.0 * time_s) * envelope * 0.12

            sample = drone + swell * 0.08 + noise + sonar
            wav_file.writeframesraw(clamp(sample).to_bytes(2, byteorder="little", signed=True))

    print(f"Saved audio to {OUTPUT}")


if __name__ == "__main__":
    main()
