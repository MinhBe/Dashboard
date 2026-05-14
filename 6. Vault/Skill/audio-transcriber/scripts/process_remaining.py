import json
import os
import sys
import subprocess
import time
import shutil
from pathlib import Path
from datetime import datetime

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.normpath(os.path.join(SCRIPTS_DIR, ".."))
DEFAULT_TEMP = os.path.join(SKILL_DIR, "temp")
OUTPUT_DIR = r"C:\Users\Admin\Documents\Dashboard\1. Capture\Sandbox"
REMAINING_JSON = os.path.join(OUTPUT_DIR, "remaining_videos.json")
PROCESSED_LOG = os.path.join(SKILL_DIR, "processed_videos_fast.log")

_candidate_models = [
    os.path.join(os.path.dirname(SKILL_DIR), "models"),
    os.path.join(SKILL_DIR, "models"),
]
MODELS_DIR = None
for d in _candidate_models:
    if os.path.isdir(d) and any("faster-whisper" in item for item in os.listdir(d)):
        MODELS_DIR = d
        break
if not MODELS_DIR:
    MODELS_DIR = _candidate_models[0]

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def run(cmd):
    eprint(f"  [{os.path.basename(cmd[0])}] {' '.join(str(a) for a in cmd[1:])}")
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(cmd, capture_output=True, text=False, env=env)
        return result.returncode == 0
    except Exception as e:
        eprint(f"  [!] Exception: {e}")
        return False

def load_remaining():
    with open(REMAINING_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def save_remaining(videos):
    with open(REMAINING_JSON, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

def process_video(video_id, url):
    vid_dir = os.path.join(DEFAULT_TEMP, f"pipe_{video_id}")
    if os.path.exists(vid_dir):
        shutil.rmtree(vid_dir, ignore_errors=True)
    os.makedirs(vid_dir, exist_ok=True)

    # Step 1: Download
    eprint(f"\n{'='*50}")
    eprint(f"Processing: {video_id}")
    ok = run([sys.executable, os.path.join(SCRIPTS_DIR, "download_audio.py"), url, "-o", vid_dir])
    if not ok:
        eprint(f"  [!] Download failed for {video_id}")
        shutil.rmtree(vid_dir, ignore_errors=True)
        return False

    # Step 2: Denoise
    audio_wav = os.path.join(vid_dir, "audio.wav")
    clean_wav = os.path.join(vid_dir, "clean.wav")
    ok = run([sys.executable, os.path.join(SCRIPTS_DIR, "denoise.py"), audio_wav, "-o", clean_wav, "--vad-threshold", "0.4"])
    if not ok:
        eprint(f"  [!] Denoise failed for {video_id}")
        shutil.rmtree(vid_dir, ignore_errors=True)
        return False

    # Step 3: Transcribe
    segments_json = os.path.join(vid_dir, "segments.json")
    ok = run([sys.executable, os.path.join(SCRIPTS_DIR, "transcribe.py"), clean_wav, "-o", segments_json, "--model-dir", MODELS_DIR, "--device", "cuda", "--compute-type", "float16", "--beam-size", "3"])
    if not ok:
        eprint(f"  [!] Transcribe failed for {video_id}")
        shutil.rmtree(vid_dir, ignore_errors=True)
        return False

    # Step 4: Format Fast
    metadata_json = os.path.join(vid_dir, "metadata.json")
    ok = run([sys.executable, os.path.join(SCRIPTS_DIR, "format_fast.py"), "-s", segments_json, "-m", metadata_json, "-o", OUTPUT_DIR])
    if not ok:
        eprint(f"  [!] Format failed for {video_id}")
        shutil.rmtree(vid_dir, ignore_errors=True)
        return False

    # Log success
    with open(PROCESSED_LOG, "a", encoding="utf-8") as f:
        f.write(f"{video_id}\n")

    shutil.rmtree(vid_dir, ignore_errors=True)
    return True

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(DEFAULT_TEMP, exist_ok=True)

    remaining = load_remaining()
    total = len(remaining)
    if total == 0:
        eprint("No remaining videos to process!")
        return

    eprint(f"\n{'='*55}")
    eprint(f"  Processing {total} remaining videos (Fast + Solo)")
    eprint(f"{'='*55}\n")

    start_time = time.time()
    success_count = 0
    fail_count = 0

    while len(remaining) > 0:
        entry = remaining[0]
        video_id = entry["video_id"]
        url = entry["url"]

        ok = process_video(video_id, url)
        if ok:
            success_count += 1
            remaining.pop(0)
        else:
            fail_count += 1
            remaining.pop(0)

        save_remaining(remaining)

        elapsed = time.time() - start_time
        done = success_count + fail_count
        rate = done / max(elapsed, 1)
        eta = (len(remaining)) / max(rate, 0.001)
        eprint(f"\n  [{done}/{total}] ✔={success_count} ✘={fail_count} remaining={len(remaining)} ETA={eta:.0f}s")

    elapsed = time.time() - start_time
    eprint(f"\n{'='*55}")
    eprint(f"  COMPLETE")
    eprint(f"{'='*55}")
    eprint(f"  Success: {success_count}/{total}")
    eprint(f"  Failed : {fail_count}")
    eprint(f"  Time   : {elapsed:.0f}s ({elapsed/60:.1f}m)")
    eprint(f"{'='*55}\n")

if __name__ == "__main__":
    main()
