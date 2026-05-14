import argparse
import os
import sys
import numpy as np
import soundfile as sf
import noisereduce as nr
import torch
from tqdm import tqdm

def get_ffmpeg_path():
    import shutil
    import os
    path = shutil.which("ffmpeg")
    if path: return path
    common_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages")
    ]
    if os.path.exists(common_paths[0]): return common_paths[0]
    if os.path.exists(common_paths[1]):
        for root, dirs, files in os.walk(common_paths[1]):
            if "ffmpeg.exe" in files: return os.path.join(root, "ffmpeg.exe")
    return None

def denoise_and_vad(input_path, output_path, vad_threshold=0.5):
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ.get("PATH", "")

    print(f"Loading audio: {input_path}", file=sys.stderr)
    data, sr = sf.read(input_path)
    if len(data.shape) > 1:
        data = data.mean(axis=1) # Mono conversion
    
    # 1. Noise Reduction
    print("Step 1: Reducing background noise...", file=sys.stderr)
    # Stationary noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=sr, prop_decrease=0.8)
    
    # 2. Voice Activity Detection (VAD)
    print("Step 2: Applying VAD (Silero)...", file=sys.stderr)
    try:
        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', 
                                      model='silero_vad', 
                                      force_reload=False)
        (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils
        
        wav = torch.from_numpy(reduced_noise).float()
        speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=sr, threshold=vad_threshold)
        
        if not speech_timestamps:
            print("Warning: No speech detected after denoising!", file=sys.stderr)
            sf.write(output_path, reduced_noise, sr)
        else:
            clean_audio = collect_chunks(speech_timestamps, wav)
            sf.write(output_path, clean_audio.numpy(), sr)
    except Exception as e:
        print(f"Warning: VAD failed ({e}), saving denoised audio only", file=sys.stderr)
        sf.write(output_path, reduced_noise, sr)
    
    print(f"Clean audio saved to: {output_path}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Denoise and VAD for cafe recordings")
    parser.add_argument("input", help="Input audio file")
    parser.add_argument("--output", "-o", required=True, help="Output clean audio file")
    parser.add_argument("--vad-threshold", type=float, default=0.4, help="VAD sensitivity (lower = more sensitive)")
    args = parser.parse_args()
    
    denoise_and_vad(args.input, args.output, args.vad_threshold)

if __name__ == "__main__":
    main()
