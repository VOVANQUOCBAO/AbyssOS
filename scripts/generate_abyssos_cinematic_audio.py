import json
import math
import random
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "pixverse_shots.json"
OUTPUT = ROOT / "assets" / "audio" / "abyssos-cinematic-v2.wav"
SAMPLE_RATE = 22050


def clamp(value: float) -> int:
    value = max(-1.0, min(1.0, value))
    return int(value * 32767)


def load_timeline():
    payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    shots = payload["shots"]
    total_duration = sum(shot["duration"] for shot in shots)

    timeline = []
    cursor = 0.0
    for shot in shots:
      start = cursor
      cursor += shot["duration"]
      timeline.append((start, cursor, shot["id"]))

    return total_duration, timeline


def scene_profile(time_s: float, timeline):
    for start, end, shot_id in timeline:
        if start <= time_s < end:
            if "planetfall" in shot_id:
                return {"drone": 0.18, "noise": 0.02, "pulse": 0.0, "alarm": 0.0, "uplink": 0.0}
            if "ocean-descent" in shot_id:
                return {"drone": 0.2, "noise": 0.03, "pulse": 0.05, "alarm": 0.0, "uplink": 0.0}
            if "scan" in shot_id:
                return {"drone": 0.17, "noise": 0.025, "pulse": 0.14, "alarm": 0.0, "uplink": 0.0}
            if "ruins" in shot_id:
                return {"drone": 0.16, "noise": 0.02, "pulse": 0.08, "alarm": 0.0, "uplink": 0.03}
            if "leviathan" in shot_id:
                return {"drone": 0.22, "noise": 0.04, "pulse": 0.12, "alarm": 0.12, "uplink": 0.0}
            if "signal-rise" in shot_id:
                return {"drone": 0.18, "noise": 0.02, "pulse": 0.1, "alarm": 0.02, "uplink": 0.12}

    return {"drone": 0.18, "noise": 0.02, "pulse": 0.0, "alarm": 0.0, "uplink": 0.0}


def main() -> None:
    random.seed(882144)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    total_duration, timeline = load_timeline()
    frame_count = int(SAMPLE_RATE * (total_duration + 0.25))

    with wave.open(str(OUTPUT), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)

        phase_a = 0.0
        phase_b = 0.0

        for index in range(frame_count):
            time_s = index / SAMPLE_RATE
            profile = scene_profile(time_s, timeline)

            phase_a += (2 * math.pi * 42.0) / SAMPLE_RATE
            phase_b += (2 * math.pi * 84.0) / SAMPLE_RATE

            drone = math.sin(phase_a) * profile["drone"] + math.sin(phase_b) * (profile["drone"] * 0.32)
            noise = (random.random() * 2 - 1) * profile["noise"]
            swell = math.sin(2 * math.pi * 0.05 * time_s) * 0.05

            sonar = 0.0
            pulse_position = time_s % 4.8
            if pulse_position < 0.18:
                envelope = 1.0 - (pulse_position / 0.18)
                sonar = math.sin(2 * math.pi * 680.0 * time_s) * envelope * profile["pulse"]

            uplink = 0.0
            uplink_position = time_s % 1.3
            if uplink_position < 0.12:
                uplink = math.sin(2 * math.pi * 980.0 * time_s) * (1.0 - uplink_position / 0.12) * profile["uplink"]

            alarm = 0.0
            alarm_position = time_s % 0.75
            if alarm_position < 0.1:
                alarm = math.sin(2 * math.pi * 220.0 * time_s) * (1.0 - alarm_position / 0.1) * profile["alarm"]

            sample = drone + noise + swell + sonar + uplink + alarm
            wav_file.writeframesraw(clamp(sample).to_bytes(2, byteorder="little", signed=True))

    print(f"Saved audio to {OUTPUT}")


if __name__ == "__main__":
    main()
