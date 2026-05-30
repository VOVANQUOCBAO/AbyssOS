import json
import re
import sys
from pathlib import Path

from moviepy import VideoFileClip, concatenate_videoclips


ROOT = Path(__file__).resolve().parent.parent
METADATA_PATH = ROOT / "assets" / "pixverse" / "shots_metadata.json"
SHOTS_DIR = ROOT / "assets" / "pixverse" / "shots"
FINAL_DIR = ROOT / "assets" / "pixverse" / "final"
FINAL_VIDEO_PATH = FINAL_DIR / "abyssos-main.mp4"
SCENES_PATH = FINAL_DIR / "scene_map.json"


def natural_video_sort_key(path: Path):
    match = re.search(r"(\d+)", path.stem)
    order = int(match.group(1)) if match else 10**9
    return (order, path.name.lower())


def load_clips_from_folder():
    files = sorted([item for item in SHOTS_DIR.glob("*.mp4") if item.is_file()], key=natural_video_sort_key)
    if not files:
        raise FileNotFoundError(f"No clips found in folder: {SHOTS_DIR}")

    clips = []
    scene_entries = []
    current_start = 0.0

    for file_path in files:
        clip = VideoFileClip(str(file_path))
        clips.append(clip)
        duration = round(float(clip.duration or 0), 2)
        scene_entries.append(
            {
                "id": file_path.stem,
                "label": file_path.stem,
                "seek_start": round(current_start, 2),
                "duration": duration,
            }
        )
        current_start += duration

    return clips, scene_entries


def main():
    clips = []
    scene_entries = []

    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    try:
        if METADATA_PATH.exists():
            payload = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
            missing_clip = next((shot for shot in payload["shots"] if not Path(shot["file_path"]).exists()), None)

            if missing_clip is None:
                for shot in payload["shots"]:
                    clip_path = Path(shot["file_path"])
                    clip = VideoFileClip(str(clip_path))
                    clips.append(clip)
                    scene_entries.append(
                        {
                            "id": shot["id"],
                            "label": shot["label"],
                            "seek_start": shot["seek_start"],
                            "duration": shot["duration"],
                        }
                    )
            else:
                print(f"Metadata references missing clip: {missing_clip['file_path']}")
                print(f"Falling back to folder order in {SHOTS_DIR}")
                clips, scene_entries = load_clips_from_folder()
        else:
            clips, scene_entries = load_clips_from_folder()

        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(
            str(FINAL_VIDEO_PATH),
            codec="libx264",
            audio_codec="aac",
            fps=24,
            threads=4,
        )
        final_clip.close()
    finally:
        for clip in clips:
            clip.close()

    scene_map = {
        "video": str(FINAL_VIDEO_PATH),
        "duration": round(sum(shot["duration"] for shot in scene_entries), 2),
        "scenes": scene_entries,
    }

    SCENES_PATH.write_text(json.dumps(scene_map, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved final video to {FINAL_VIDEO_PATH}")
    print(f"Saved scene map to {SCENES_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
