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

def format_normal(segments_path: str, output_dir: str, metadata_path: str = None, speakers_path: str = None):
    with open(segments_path, "r", encoding="utf-8") as f:
        segs = json.load(f)
    
    metadata = {}
    if metadata_path and os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    speakers = []
    if speakers_path and os.path.exists(speakers_path):
        with open(speakers_path, "r", encoding="utf-8") as f:
            speakers = json.load(f)

    title = metadata.get("title", "Unknown Video")
    url = metadata.get("url", metadata.get("webpage_url", ""))
    
    safe_name = sanitize_filename(title) + "_Normal.md"
    output_path = os.path.join(output_dir, safe_name)

    os.makedirs(output_dir, exist_ok=True)

    lines = [
        f"### [NORMAL] {title}",
        f"- **Nguồn:** {url}" if url else "",
        f"- **Ngày:** {date.today().strftime('%d/%m/%Y')}",
        "", "---", ""
    ]

    # Align segments with speakers if available
    current_speaker = None
    paragraph = []

    for seg in segs["segments"]:
        start, text = seg["start"], seg["text"]
        
        # Determine speaker for this segment
        speaker = "Nhân vật"
        for sp in speakers:
            if sp["start"] <= start < sp["end"]:
                speaker = sp["speaker_id"]
                break
        
        if speaker != current_speaker:
            if paragraph:
                lines.append(" ".join(paragraph))
                lines.append("")
            lines.append(f"**{speaker}:**")
            paragraph = [text]
            current_speaker = speaker
        else:
            paragraph.append(text)
            # Simple paragraph splitting logic: if paragraph gets too long
            if len(paragraph) > 10:
                lines.append(" ".join(paragraph))
                paragraph = []

    if paragraph:
        lines.append(" ".join(paragraph))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Normal transcript saved: {safe_name}", file=sys.stderr)
    print(json.dumps({"file": safe_name, "mode": "normal"}))

def main():
    parser = argparse.ArgumentParser(description="Generate Normal-style narrative transcript")
    parser.add_argument("--segments", "-s", required=True, help="Path to segments.json")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    parser.add_argument("--metadata", "-m", help="Path to metadata.json")
    parser.add_argument("--speakers", "-sp", help="Path to speakers.json")
    args = parser.parse_args()
    format_normal(args.segments, args.output_dir, args.metadata, args.speakers)

if __name__ == "__main__":
    main()
