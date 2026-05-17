"""
review_scanner.py — Scan tất cả concepts đến hạn review.

Usage:
  python review_scanner.py                    # scan tất cả domains
  python review_scanner.py --domain mandarin  # chỉ scan 1 domain
  python review_scanner.py --overdue          # chỉ show quá hạn
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

EXHIBIT_ROOT = Path(r"C:\Projects\Dashboard\5. Exhibit")


def load_graph(domain_path: Path) -> dict | None:
    graph_file = domain_path / "knowledge-graph.json"
    if not graph_file.exists():
        return None
    with open(graph_file, encoding="utf-8") as f:
        return json.load(f)


def scan_domain(domain: str, overdue_only: bool) -> list[dict]:
    domain_path = EXHIBIT_ROOT / domain
    graph = load_graph(domain_path)
    if not graph:
        return []

    now = datetime.now()
    due = []

    for concept, node in graph.get("nodes", {}).items():
        ls = node.get("learner_state", {})
        next_review_str = ls.get("next_review")
        if not next_review_str:
            continue

        try:
            next_review_dt = datetime.fromisoformat(next_review_str)
        except ValueError:
            continue

        is_overdue = next_review_dt <= now
        if overdue_only and not is_overdue:
            continue

        due.append({
            "domain": domain,
            "concept": concept,
            "bloom_level": ls.get("bloom_level", "remember"),
            "mastery_probability": ls.get("mastery_probability", 0.0),
            "next_review": next_review_str,
            "overdue": is_overdue,
            "needs_restructure": ls.get("needs_restructure", False),
            "days_until": (next_review_dt - now).days,
        })

    return sorted(due, key=lambda x: x["next_review"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", help="Specific domain to scan (default: all)")
    parser.add_argument("--overdue", action="store_true", help="Show only overdue concepts")
    args = parser.parse_args()

    if args.domain:
        domains = [args.domain]
    else:
        domains = [d.name for d in EXHIBIT_ROOT.iterdir() if d.is_dir() and not d.name.startswith(".")]

    all_due = []
    for domain in domains:
        all_due.extend(scan_domain(domain, args.overdue))

    if not all_due:
        print("Không có concept nào cần review" + (" (overdue)" if args.overdue else "") + ".")
        return

    print(f"\n=== REVIEW SCANNER {'(OVERDUE ONLY)' if args.overdue else ''} ===")
    print(f"Ngày hôm nay: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    overdue_list = [x for x in all_due if x["overdue"]]
    upcoming_list = [x for x in all_due if not x["overdue"]]

    if overdue_list:
        print(f"⚠️  QUÁ HẠN ({len(overdue_list)} concepts):")
        for item in overdue_list:
            flag = " [RESTRUCTURE]" if item["needs_restructure"] else ""
            print(f"  • {item['domain']}/{item['concept']} — bloom={item['bloom_level']}, mastery={item['mastery_probability']:.2f}{flag}")
            print(f"    next_review: {item['next_review']} ({abs(item['days_until'])} ngày trước)")

    if upcoming_list and not args.overdue:
        print(f"\n📅 SẮP ĐẾN HẠN ({len(upcoming_list)} concepts):")
        for item in upcoming_list[:10]:
            print(f"  • {item['domain']}/{item['concept']} — bloom={item['bloom_level']}, mastery={item['mastery_probability']:.2f}")
            print(f"    next_review: {item['next_review']} (còn {item['days_until']} ngày)")

    print(f"\nTổng: {len(all_due)} concept(s) cần chú ý.")
    print("\nĐể bắt đầu học: gọi socratic skill với domain và concept đầu tiên trong danh sách.")


if __name__ == "__main__":
    main()
