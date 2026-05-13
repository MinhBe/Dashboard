import argparse
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import torch
from sklearn.cluster import AgglomerativeClustering
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

def load_audio_mono(path: str, target_sr: int = 16000) -> tuple:
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ.get("PATH", "")
    
    import soundfile as sf
    data, sr = sf.read(path)
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    if sr != target_sr:
        import scipy.signal
        data = scipy.signal.resample(data, int(len(data) * target_sr / sr))
        sr = target_sr
    return data, sr


def get_speech_segments_vad(audio: np.ndarray, sr: int,
                            threshold: float = 0.5,
                            min_speech_ms: int = 500,
                            min_silence_ms: int = 300) -> list:
    import silero_vad
    model = silero_vad.load_silero_vad()

    audio_tensor = torch.from_numpy(audio).float()

    speeches = silero_vad.get_speech_timestamps(
        audio_tensor,
        model,
        threshold=threshold,
        sampling_rate=sr,
        min_speech_duration_ms=min_speech_ms,
        min_silence_duration_ms=min_silence_ms,
        return_seconds=True,
    )

    result = []
    for s in speeches:
        result.append({
            "start": s["start"],
            "end": s["end"],
        })
    return result


def extract_embeddings(audio: np.ndarray, sr: int,
                       segments: list) -> np.ndarray:
    import librosa
    embeddings = []

    for seg in tqdm(segments, desc='Embeddings', unit='seg',
                    bar_format='{desc}: {percentage:3.0f}%|{bar}| {n}/{total} [{elapsed}<{remaining}]',
                    file=sys.stderr):
        start_sample = int(seg["start"] * sr)
        end_sample = int(seg["end"] * sr)
        seg_audio = audio[start_sample:end_sample]

        if len(seg_audio) < sr * 0.3:
            seg_audio = np.pad(seg_audio, (0, max(0, int(sr * 0.3) - len(seg_audio))))

        mfcc = librosa.feature.mfcc(y=seg_audio, sr=sr, n_mfcc=20)
        delta = librosa.feature.delta(mfcc)
        delta2 = librosa.feature.delta(mfcc, order=2)
        feat = np.concatenate([
            mfcc.mean(axis=1),
            delta.mean(axis=1),
            delta2.mean(axis=1),
        ])
        embeddings.append(feat)

    return np.array(embeddings)


def cluster_speakers(embeddings: np.ndarray, distance_threshold: float = 0.75) -> list:
    if len(embeddings) == 0:
        return []
    if len(embeddings) == 1:
        return [0]

    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=distance_threshold,
        metric="cosine",
        linkage="average",
    )
    return clustering.fit_predict(embeddings).tolist()


def merge_segments(speech_segments_raw: list, audio: np.ndarray, sr: int,
                   clustering_labels: list) -> list:
    result = []
    seen_speakers = {}
    next_id = 1

    for i, seg in enumerate(speech_segments_raw):
        start = round(float(seg["start"]), 2) if isinstance(seg, dict) else round(float(seg.start), 2)
        end = round(float(seg["end"]), 2) if isinstance(seg, dict) else round(float(seg.end), 2)
        label = clustering_labels[i] if i < len(clustering_labels) else 0

        if label not in seen_speakers:
            seen_speakers[label] = f"Nhân vật {next_id}"
            next_id += 1

        result.append({
            "start": start,
            "end": end,
            "speaker_id": seen_speakers[label],
            "cluster_label": int(label),
        })

    return result


def diarize(audio_path: str, output_path: str, segments_path: str = None,
            vad_threshold: float = 0.5,
            min_speech_ms: int = 500,
            min_silence_ms: int = 300,
            distance_threshold: float = 0.75):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Loading audio...", file=sys.stderr)
    audio, sr = load_audio_mono(audio_path)

    print(f"Running VAD...", file=sys.stderr)
    speech_segments = get_speech_segments_vad(
        audio, sr,
        threshold=vad_threshold,
        min_speech_ms=min_speech_ms,
        min_silence_ms=min_silence_ms,
    )

    if not speech_segments:
        print("No speech detected!", file=sys.stderr)
        result = []
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        return

    print(f"Extracting speaker embeddings ({len(speech_segments)} segments)...", file=sys.stderr)
    embeddings = extract_embeddings(audio, sr, speech_segments)

    print(f"Clustering speakers...", file=sys.stderr)
    labels = cluster_speakers(embeddings, distance_threshold=distance_threshold)

    result = merge_segments(speech_segments, audio, sr, labels)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    n_speakers = len(set(labels))
    print(f"Detected {n_speakers} speakers, {len(result)} segments to {output_path}", file=sys.stderr)
    print(json.dumps({"num_speakers": n_speakers, "segments_count": len(result)}))


def main():
    parser = argparse.ArgumentParser(description="Speaker diarization")
    parser.add_argument("audio_path", help="Path to audio file (WAV 16kHz mono)")
    parser.add_argument("--output", "-o", required=True, help="Output JSON path")
    parser.add_argument("--segments", help="Path to transcription segments (for alignment)")
    parser.add_argument("--vad-threshold", type=float, default=0.5)
    parser.add_argument("--distance-threshold", type=float, default=0.75)
    args = parser.parse_args()

    diarize(
        args.audio_path,
        args.output,
        segments_path=args.segments,
        vad_threshold=args.vad_threshold,
        distance_threshold=args.distance_threshold,
    )


if __name__ == "__main__":
    main()
