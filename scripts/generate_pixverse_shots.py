import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "pixverse_shots.json"
OUTPUT_DIR = ROOT / "assets" / "pixverse"
SHOTS_DIR = OUTPUT_DIR / "shots"
METADATA_PATH = OUTPUT_DIR / "shots_metadata.json"


def resolve_pixverse_command():
    candidates = [
        shutil.which("pixverse.cmd"),
        shutil.which("pixverse"),
        str(Path.home() / "AppData" / "Roaming" / "npm" / "pixverse.cmd"),
        str(Path.home() / "AppData" / "Roaming" / "npm" / "pixverse.ps1"),
    ]

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            path = Path(candidate)
            if path.suffix.lower() == ".ps1":
                return ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(path)]
            return [str(path)]

    raise RuntimeError("Could not locate PixVerse CLI executable.")


def run_pixverse(args):
    pixverse_cmd = resolve_pixverse_command()
    result = subprocess.run(
        [*pixverse_cmd, *args, "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"PixVerse failed with code {result.returncode}")

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid PixVerse JSON output: {result.stdout}") from exc


def newest_file(path):
    files = [item for item in path.iterdir() if item.is_file()]
    return max(files, key=lambda item: item.stat().st_mtime) if files else None


def main():
    SHOTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    auth = run_pixverse(["auth", "status"])
    if not auth.get("authenticated"):
        raise RuntimeError("PixVerse CLI is not authenticated.")

    account = run_pixverse(["account", "info"])
    total_credits = account.get("credits", {}).get("total", 0)
    if total_credits <= 0:
        raise RuntimeError("No PixVerse credits available.")

    metadata = {
        "project": config["project"],
        "model": config["model"],
        "quality": config["quality"],
        "aspect_ratio": config["aspect_ratio"],
        "seed": config["seed"],
        "shots": [],
    }

    for shot in config["shots"]:
        prompt = f'{shot["prompt"]} {config["base_style"]}'
        create_args = [
            "create",
            "video",
            "--prompt",
            prompt,
            "--model",
            config["model"],
            "--quality",
            config["quality"],
            "--aspect-ratio",
            config["aspect_ratio"],
            "--duration",
            str(shot["duration"]),
            "--seed",
            str(config["seed"]),
            "--timeout",
            "1800",
            "--idempotency-key",
            f'abyssos-{shot["id"]}-{config["model"]}-{config["quality"]}',
        ]

        create_args.append("--no-audio" if not config.get("audio", False) else "--audio")
        create_args.append("--no-multi-shot" if not config.get("multi_shot", False) else "--multi-shot")

        print(f'Generating {shot["id"]}...')
        created = run_pixverse(create_args)
        video_id = created["video_id"]

        before = {item.name for item in SHOTS_DIR.iterdir() if item.is_file()}
        downloaded = run_pixverse(["asset", "download", str(video_id), "--type", "video", "--dest", str(SHOTS_DIR)])
        after = {item.name for item in SHOTS_DIR.iterdir() if item.is_file()}
        new_files = sorted(after - before)

        downloaded_path = downloaded.get("path")
        if downloaded_path:
            source_path = Path(downloaded_path)
        elif new_files:
            source_path = SHOTS_DIR / new_files[-1]
        else:
            source_path = newest_file(SHOTS_DIR)

        if source_path is None or not source_path.exists():
            raise RuntimeError(f'Could not find downloaded file for {shot["id"]}.')

        target_path = SHOTS_DIR / f'{shot["id"]}{source_path.suffix.lower()}'
        if source_path.resolve() != target_path.resolve():
            if target_path.exists():
                target_path.unlink()
            source_path.rename(target_path)

        metadata["shots"].append(
            {
                "id": shot["id"],
                "label": shot["label"],
                "duration": shot["duration"],
                "seek_start": shot["seek_start"],
                "video_id": video_id,
                "file_name": target_path.name,
                "file_path": str(target_path),
                "prompt": prompt,
                "cover_url": created.get("cover_url"),
                "video_url": created.get("video_url"),
            }
        )

        METADATA_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f'Saved {target_path.name}')

    print(f"All shots generated. Metadata saved to {METADATA_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
