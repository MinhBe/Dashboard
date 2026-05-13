import argparse
import json
import os
import re
import sys
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "", name)
    name = name.strip().rstrip(".")
    return name if name else "transcript"

def format_max(segments_path: str, speakers_path: str, output_dir: str, metadata_path: str = None):
    with open(segments_path, "r", encoding="utf-8") as f:
        segs = json.load(f)
    with open(speakers_path, "r", encoding="utf-8") as f:
        speakers = json.load(f)

    metadata = {}
    if metadata_path and os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    title = metadata.get("title", "Unknown Video")
    channel = metadata.get("channel", "")
    url = metadata.get("url", metadata.get("webpage_url", ""))
    duration = metadata.get("duration_seconds", segs.get("duration_seconds", 0))

    safe_name = sanitize_filename(title) + "_Max.md"
    output_path = os.path.join(output_dir, safe_name)

    os.makedirs(output_dir, exist_ok=True)

    lines = []
    lines.append(f"### [MAX] Transcript: {title}")
    if url: lines.append(f"- **Nguồn:** {url}")
    if channel: lines.append(f"- **Tác giả:** {channel}")
    lines.append(f"- **Ngày:** {date.today().strftime('%d/%m/%Y')}")
    if duration: lines.append(f"- **Thời lượng:** {int(duration)}s")
    lines.append(f"- **Ngôn ngữ:** {segs.get('language', 'unknown')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("#### Speaker Diarization & Confidence Tagging")
    lines.append("")

    aligned = []
    for seg in segs["segments"]:
        start, end, text = seg["start"], seg["end"], seg["text"]
        speaker = "Nhân vật 1"
        for sp in speakers:
            if sp["start"] <= start < sp["end"]:
                speaker = sp["speaker_id"]
                break
        aligned.append({
            "start": start,
            "end": end,
            "text": text,
            "speaker": speaker,
        })

    group_order = []
    last_speaker = None
    for seg in aligned:
        sp = seg["speaker"]
        timestamp = f"[{int(seg['start'] // 60):02}:{int(seg['start'] % 60):02} - {int(seg['end'] // 60):02}:{int(seg['end'] % 60):02}]"
        
        if sp != last_speaker:
            lines.append(f"\n**{sp}** {timestamp}")
            last_speaker = sp
        
        lines.append(f"> {seg['text']}")

    lines.append("\n---")
    lines.append("*Bản transcript này đã được xử lý Denoise & VAD để đạt chất lượng tốt nhất.*")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Max transcript saved: {safe_name}", file=sys.stderr)
    print(json.dumps({"file": safe_name, "mode": "max"}))

def main():
    parser = argparse.ArgumentParser(description="Generate Max high-quality transcript")
    parser.add_argument("--segments", "-s", required=True, help="Path to segments.json")
    parser.add_argument("--speakers", "-sp", required=True, help="Path to speakers.json")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    parser.add_argument("--metadata", "-m", help="Path to metadata.json")
    args = parser.parse_args()
    format_max(args.segments, args.speakers, args.output_dir, args.metadata)

if __name__ == "__main__":
    main()
