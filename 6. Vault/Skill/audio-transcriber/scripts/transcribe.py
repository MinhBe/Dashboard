import argparse
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")

from tqdm import tqdm
from faster_whisper import WhisperModel


def transcribe(audio_path: str, output_path: str, model_dir: str = None,
               model_size: str = "large-v3-turbo", device: str = "cpu",
               compute_type: str = "int8", beam_size: int = 5,
               vad_filter: bool = True):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    import soundfile as sf
    audio_data, sr_orig = sf.read(audio_path)
    duration_sec = len(audio_data) / sr_orig

    print(f"Loading Whisper model ({model_size})...", file=sys.stderr)
    model = WhisperModel(
        model_size,
        device=device,
        compute_type=compute_type,
        download_root=model_dir,
        cpu_threads=os.cpu_count() or 4,
        num_workers=2,
    )

    segments, info = model.transcribe(
        audio_path,
        beam_size=beam_size,
        vad_filter=vad_filter,
        language=None,
        condition_on_previous_text=False, # Avoid looping on noise
        repetition_penalty=1.2,
        no_speech_threshold=0.6,
    )

    bar = tqdm(
        total=duration_sec, unit='s', desc='Transcribing',
        bar_format='{desc}: {percentage:3.0f}%|{bar}| {n:.1f}/{total_fmt}s [{elapsed}<{remaining}]',
        file=sys.stderr,
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('{\n')
        f.write(f'  "language": "{info.language}",\n')
        f.write(f'  "language_probability": {info.language_probability},\n')
        f.write(f'  "duration_seconds": {duration_sec},\n')
        f.write(f'  "segments": [\n')
        f.flush()

        first = True
        count = 0
        for seg in segments:
            # Confidence check: avg_logprob is logarithmic, -1.0 is roughly 36% confidence
            is_low_confidence = seg.avg_logprob < -1.0
            text_prefix = "[LOW_CONFIDENCE] " if is_low_confidence else ""
            
            seg_data = {
                "start": round(seg.start, 2),
                "end": round(seg.end, 2),
                "text": text_prefix + seg.text.strip(),
                "avg_logprob": round(seg.avg_logprob, 3),
                "no_speech_prob": round(seg.no_speech_prob, 3),
                "is_low_confidence": is_low_confidence,
                "words": [
                    {
                        "word": w.word,
                        "start": round(w.start, 2),
                        "end": round(w.end, 2),
                        "probability": round(w.probability, 3),
                    }
                    for w in (seg.words or [])
                ],
            }

            if not first:
                f.write(',\n')
            first = False
            json.dump(seg_data, f, ensure_ascii=False)

            bar.n = min(seg.end, duration_sec)
            bar.refresh()
            f.flush()
            count += 1

        bar.close()
        f.write('\n  ]\n')
        f.write('}\n')

    print(f"Saved {count} segments to {output_path}", file=sys.stderr)
    print(json.dumps({"language": info.language, "segments_count": count}))


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio with faster-whisper")
    parser.add_argument("audio_path", help="Path to audio file (WAV 16kHz mono)")
    parser.add_argument("--output", "-o", required=True, help="Output JSON path")
    parser.add_argument("--model-dir", help="Model download directory")
    parser.add_argument("--model-size", default="large-v3-turbo")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument("--beam-size", type=int, default=5)
    parser.add_argument("--no-vad", action="store_true")
    args = parser.parse_args()

    transcribe(
        args.audio_path,
        args.output,
        model_dir=args.model_dir,
        model_size=args.model_size,
        device=args.device,
        compute_type=args.compute_type,
        beam_size=args.beam_size,
        vad_filter=not args.no_vad,
    )


if __name__ == "__main__":
    main()
