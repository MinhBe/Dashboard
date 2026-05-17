import argparse
import json
import os
import subprocess
import sys

def get_ffmpeg_path():
    # 1. Check if in PATH
    import shutil
    path = shutil.which("ffmpeg")
    if path:
        return path
    
    # 2. Check common WinGet paths
    common_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages")
    ]
    
    if os.path.exists(common_paths[0]):
        return common_paths[0]
        
    if os.path.exists(common_paths[1]):
        for root, dirs, files in os.walk(common_paths[1]):
            if "ffmpeg.exe" in files:
                return os.path.join(root, "ffmpeg.exe")
    return None

def download_audio(url: str, output_dir: str) -> dict:
    os.makedirs(output_dir, exist_ok=True)
    ffmpeg_path = get_ffmpeg_path()
    ffmpeg_dir = os.path.dirname(ffmpeg_path) if ffmpeg_path else None
    
    if ffmpeg_dir:
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

    # Get metadata first
    meta_cmd = [
        sys.executable, "-m", "yt_dlp",
        "--dump-json",
        "--no-download",
        "--cookies-from-browser", "chrome",
        "--js-runtimes", "node",
        url,
    ]
    if ffmpeg_dir:
        meta_cmd.extend(["--ffmpeg-location", ffmpeg_dir])

    result = subprocess.run(meta_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get metadata: {result.stderr}")

    metadata = json.loads(result.stdout.strip().split("\n")[0])
    info = {
        "title": metadata.get("title", ""),
        "channel": metadata.get("channel", "") or metadata.get("uploader", ""),
        "duration_seconds": metadata.get("duration", 0),
        "description": (metadata.get("description") or "")[:500],
        "url": url,
        "webpage_url": metadata.get("webpage_url", url),
    }

    # Download best audio, convert to 16kHz mono WAV
    output_template = os.path.join(output_dir, "%(id)s.%(ext)s")
    dl_cmd = [
        sys.executable, "-m", "yt_dlp",
        "-x",  # extract audio
        "--audio-format", "wav",
        "--audio-quality", "0",
        "--postprocessor-args", "ffmpeg:-ac 1 -ar 16000",
        "--cookies-from-browser", "chrome",
        "--js-runtimes", "node",
        "-o", output_template,
        url,
    ]
    if ffmpeg_dir:
        dl_cmd.extend(["--ffmpeg-location", ffmpeg_dir])
        
    subprocess.run(dl_cmd, check=True)

    # Find the downloaded wav
    audio_path = None
    for f in os.listdir(output_dir):
        if f.endswith(".wav"):
            audio_path = os.path.join(output_dir, f)
            break

    if not audio_path:
        # Check if it's still webm or m4a and try to convert manually if yt-dlp failed conversion
        raise RuntimeError("No WAV file produced by yt-dlp")

    # Rename to standard name
    standard_path = os.path.join(output_dir, "audio.wav")
    if os.path.exists(standard_path):
        os.remove(standard_path)
    os.rename(audio_path, standard_path)

    # Save metadata
    meta_path = os.path.join(output_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(info, ensure_ascii=False))
    return info

def main():
    parser = argparse.ArgumentParser(description="Download audio from YouTube")
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    args = parser.parse_args()
    download_audio(args.url, args.output_dir)

if __name__ == "__main__":
    main()
