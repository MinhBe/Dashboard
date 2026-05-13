import os
import sys
import subprocess
import json
import shutil

def check_ffmpeg():
    if shutil.which("ffmpeg"):
        return True
    
    # Check common WinGet paths
    common_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages")
    ]
    
    if os.path.exists(common_paths[0]):
        return True
        
    # Deep search in WinGet Packages
    if os.path.exists(common_paths[1]):
        for root, dirs, files in os.walk(common_paths[1]):
            if "ffmpeg.exe" in files:
                return True
    return False

def check_python_libs():
    libs = [
        "faster_whisper", "silero_vad", "noisereduce", "torch", 
        "numpy", "librosa", "scipy", "soundfile", "yt_dlp", "tqdm"
    ]
    missing = []
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            missing.append(lib)
    return missing

def check_models(skill_dir):
    models_dir = os.path.join(skill_dir, "models")
    if not os.path.exists(models_dir):
        return {"models_dir_exists": False, "whisper_downloaded": False}
    
    # Look for any folder matching faster-whisper
    whisper_downloaded = False
    for item in os.listdir(models_dir):
        if "faster-whisper" in item and os.path.isdir(os.path.join(models_dir, item)):
            whisper_downloaded = True
            break
            
    return {
        "models_dir_exists": True,
        "whisper_downloaded": whisper_downloaded
    }

def main():
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    results = {
        "ffmpeg": check_ffmpeg(),
        "python_libs": check_python_libs(),
        "models": check_models(skill_dir),
        "status": "ready"
    }
    
    if not results["ffmpeg"] or results["python_libs"] or not results["models"]["whisper_downloaded"]:
        results["status"] = "missing"
    
    print(json.dumps(results, indent=2))
    
    if results["status"] == "missing":
        print("\n--- PHÁT HIỆN THIẾU THÀNH PHẦN ---", file=sys.stderr)
        if not results["ffmpeg"]:
            print("[-] Thiếu FFmpeg: Hãy cài đặt ffmpeg và thêm vào PATH.", file=sys.stderr)
        if results["python_libs"]:
            print(f"[-] Thiếu thư viện Python: {', '.join(results['python_libs'])}", file=sys.stderr)
        if not results["models"]["whisper_downloaded"]:
            print("[-] Thiếu Whisper Model: Chạy scripts/setup.ps1 để tải.", file=sys.stderr)
        sys.exit(1)
    else:
        print("\n[+] Môi trường sẵn sàng! Hệ thống có thể chạy Offline.", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
