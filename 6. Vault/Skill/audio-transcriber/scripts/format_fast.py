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

def format_fast(segments_path: str, output_dir: str, metadata_path: str = None):
    with open(segments_path, "r", encoding="utf-8") as f:
        segs = json.load(f)
    
    metadata = {}
    if metadata_path and os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    title = metadata.get("title", "Unknown Video")
    url = metadata.get("url", metadata.get("webpage_url", ""))
    
    safe_name = sanitize_filename(title) + "_Fast.md"
    output_path = os.path.join(output_dir, safe_name)

    os.makedirs(output_dir, exist_ok=True)

    lines = [
        f"### [FAST] Transcript: {title}",
        f"- **Nguồn:** {url}" if url else "",
        f"- **Ngày:** {date.today().strftime('%d/%m/%Y')}",
        f"- **Ngôn ngữ:** {segs.get('language', 'unknown')}",
        "", "---", ""
    ]

    for seg in segs["segments"]:
        start = seg["start"]
        timestamp = f"[{int(start // 60):02}:{int(start % 60):02}]"
        lines.append(f"{timestamp} {seg['text']}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Fast transcript saved: {safe_name}", file=sys.stderr)
    print(json.dumps({"file": safe_name, "mode": "fast"}))

def main():
    parser = argparse.ArgumentParser(description="Generate Fast timestamped transcript")
    parser.add_argument("--segments", "-s", required=True, help="Path to segments.json")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    parser.add_argument("--metadata", "-m", help="Path to metadata.json")
    args = parser.parse_args()
    format_fast(args.segments, args.output_dir, args.metadata)

if __name__ == "__main__":
    main()
