"""
reextract_trigger.py — Nhắc re-extraction khi knowledge nodes cũ hoặc có contradictions chưa giải quyết.

Trigger khi:
  - last_reextracted > 30 ngày
  - contradictions có unresolved items

Usage:
  python reextract_trigger.py                    # scan tất cả domains
  python reextract_trigger.py --domain ai-concept
  python reextract_trigger.py --days 60          # threshold khác (mặc định 30)
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

EXHIBIT_ROOT = Path(r"C:\Projects\Dashboard\5. Exhibit")


def load_graph(domain_path: Path) -> dict | None:
    graph_file = domain_path / "knowledge-graph.json"
    if not graph_file.exists():
        return None
    with open(graph_file, encoding="utf-8") as f:
        return json.load(f)


def scan_domain(domain: str, threshold_days: int) -> list[dict]:
    domain_path = EXHIBIT_ROOT / domain
    graph = load_graph(domain_path)
    if not graph:
        return []

    now = datetime.now()
    threshold = timedelta(days=threshold_days)
    flagged = []

    for concept, node in graph.get("nodes", {}).items():
        sc = node.get("source_content", {})
        reasons = []

        last_reextracted_str = sc.get("last_reextracted")
        if last_reextracted_str:
            try:
                last_dt = datetime.fromisoformat(last_reextracted_str)
                days_ago = (now - last_dt).days
                if days_ago > threshold_days:
                    reasons.append(f"last_reextracted {days_ago} ngày trước (threshold={threshold_days})")
            except ValueError:
                pass

        contradictions = node.get("contradictions", [])
        unresolved = [c for c in contradictions if not c.get("resolved", False)]
        if unresolved:
            reasons.append(f"{len(unresolved)} contradiction(s) chưa giải quyết")

        if reasons:
            flagged.append({
                "domain": domain,
                "concept": concept,
                "reasons": reasons,
                "unresolved_contradictions": unresolved,
                "source_name": sc.get("source_name", "unknown"),
                "last_reextracted": last_reextracted_str,
            })

    return flagged


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="Specific domain (default: all)")
    parser.add_argument("--days", type=int, default=30, help="Threshold ngày cho re-extraction (default: 30)")
    args = parser.parse_args()

    if args.domain:
        domains = [args.domain]
    else:
        domains = [d.name for d in EXHIBIT_ROOT.iterdir() if d.is_dir() and not d.name.startswith(".")]

    all_flagged = []
    for domain in domains:
        all_flagged.extend(scan_domain(domain, args.days))

    if not all_flagged:
        print(f"Không có concept nào cần re-extraction (threshold={args.days} ngày).")
        return

    print(f"\n=== RE-EXTRACTION TRIGGER ===")
    print(f"Ngày hôm nay: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Threshold: {args.days} ngày\n")

    for item in all_flagged:
        print(f"📌 {item['domain']}/{item['concept']} (source: {item['source_name']})")
        for reason in item["reasons"]:
            print(f"   ↳ {reason}")

        if item["unresolved_contradictions"]:
            print(f"   Contradictions cần giải quyết:")
            for c in item["unresolved_contradictions"]:
                print(f"     • Source says: \"{c.get('source_says', '?')}\"")
                print(f"       Learner believes: \"{c.get('learner_believes', '?')}\"")
                print(f"       Date: {c.get('date', '?')}")
        print()

    print("-" * 60)
    print(f"Tổng: {len(all_flagged)} concept(s) cần re-extraction.")
    print("\nQuy trình: dùng transcript-analysis skill để re-extract.")
    print("Khi re-extract, load contradictions list như context bổ sung:")
    print('  "Những contradiction này đã được ghi nhận: [list]. Re-extract với lens đó."')


if __name__ == "__main__":
    main()
