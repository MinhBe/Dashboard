import argparse
import json
import os
import subprocess
import sys
import shutil

def run_command(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, text=True)
    if result.returncode != 0:
        print(f"Command failed with code {result.returncode}")
        return False
    return True

def get_video_ids(channel_url):
    cmd = ["yt-dlp", "--get-id", "--flat-playlist", channel_url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to get video IDs: {result.stderr}")
        return []
    return [id.strip() for id in result.stdout.strip().split("\n") if id.strip()]

def main():
    parser = argparse.ArgumentParser(description="Batch transcribe a YouTube channel")
    parser.add_argument("channel_url", help="YouTube channel URL")
    parser.add_argument("--output-dir", "-o", required=True, help="Final output directory for .md files")
    parser.add_argument("--mode", choices=["fast", "blog", "max"], default="fast", help="Transcription mode")
    args = parser.parse_args()

    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scripts_dir = os.path.join(skill_root, "scripts")
    temp_dir = os.path.join(skill_root, args.temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)

    log_path = os.path.join(skill_root, f"processed_videos_{args.mode}.log")
    processed_ids = set()
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            processed_ids = set(line.strip() for line in f if line.strip())

    video_ids = get_video_ids(args.channel_url)
    print(f"Found {len(video_ids)} videos. {len(processed_ids)} already processed in {args.mode} mode.")

    for vid_id in video_ids:
        if vid_id in processed_ids:
            print(f"Skipping {vid_id} (already processed)")
            continue

        print(f"\n>>> Processing video: {vid_id} (Mode: {args.mode})")
        url = f"https://www.youtube.com/watch?v={vid_id}"
        
        # 1. Download
        vid_temp = os.path.join(temp_dir, vid_id)
        if os.path.exists(vid_temp):
            shutil.rmtree(vid_temp)
        os.makedirs(vid_temp, exist_ok=True)

        if not run_command([sys.executable, os.path.join(scripts_dir, "download_audio.py"), url, "-o", vid_temp]):
            continue

        audio_wav = os.path.join(vid_temp, "audio.wav")
        clean_wav = os.path.join(vid_temp, "clean.wav")
        segments_json = os.path.join(vid_temp, "segments.json")
        speakers_json = os.path.join(vid_temp, "speakers.json")
        metadata_json = os.path.join(vid_temp, "metadata.json")

        # 2. Denoise
        if not run_command([sys.executable, os.path.join(scripts_dir, "denoise.py"), audio_wav, "-o", clean_wav]):
            continue

        # 3. Transcribe
        if not run_command([sys.executable, os.path.join(scripts_dir, "transcribe.py"), clean_wav, "-o", segments_json, "--model-dir", os.path.join(skill_root, "models")]):
            continue

        # 4. Diarize & Align (depending on mode)
        if args.mode == "fast":
            if not run_command([sys.executable, os.path.join(scripts_dir, "format_fast.py"), "-s", segments_json, "-m", metadata_json, "-o", vid_temp]):
                continue
        elif args.mode == "blog":
            if not run_command([sys.executable, os.path.join(scripts_dir, "diarize.py"), clean_wav, "-o", speakers_json]):
                continue
            if not run_command([sys.executable, os.path.join(scripts_dir, "format_blog.py"), "-s", segments_json, "-sp", speakers_json, "-m", metadata_json, "-o", vid_temp]):
                continue
        elif args.mode == "max":
            if not run_command([sys.executable, os.path.join(scripts_dir, "diarize.py"), clean_wav, "-o", speakers_json]):
                continue
            if not run_command([sys.executable, os.path.join(scripts_dir, "format_max.py"), "-s", segments_json, "-sp", speakers_json, "-m", metadata_json, "-o", vid_temp]):
                continue

        # 6. Copy to destination
        for f in os.listdir(vid_temp):
            if f.endswith(".md"):
                shutil.copy(os.path.join(vid_temp, f), os.path.join(args.output_dir, f))
                print(f"Copied {f} to {args.output_dir}")

        # 7. Cleanup & Log
        shutil.rmtree(vid_temp)
        with open(log_path, "a") as f:
            f.write(f"{vid_id}\n")
        processed_ids.add(vid_id)

    print("\nBatch processing completed!")

if __name__ == "__main__":
    main()
