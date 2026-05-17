"""
diagnostic.py — Cold start diagnostic cho một domain.

Đọc curriculum_sequence, lấy tối đa 5 concept đầu chưa có learner_state,
compose câu hỏi Bloom "understand", và print ra để Stage 2 dùng.

Usage:
  python diagnostic.py --domain mandarin
  python diagnostic.py --domain ai-concept --limit 3
"""

import argparse
import json
import sys
from pathlib import Path

EXHIBIT_ROOT = Path(r"C:\Projects\Dashboard\5. Exhibit")

BLOOM_DIAGNOSTIC_TEMPLATES = {
    "remember":   "Bạn nhớ [concept] là gì không? Mô tả trong 1–2 câu.",
    "understand": "Giải thích [concept] theo cách của bạn — tại sao nó hoạt động như vậy?",
    "apply":      "Đưa ra một ví dụ cụ thể bạn sẽ dùng [concept] như thế nào.",
    "analyze":    "So sánh [concept] với [concept] khác gần đó — điểm giống và khác là gì?",
    "evaluate":   "Khi nào [concept] không phải là lựa chọn tốt nhất?",
}


def load_graph(domain: str) -> dict:
    path = EXHIBIT_ROOT / domain / "knowledge-graph.json"
    if not path.exists():
        print(f"ERROR: knowledge-graph.json not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    graph = load_graph(args.domain)
    meta = graph.get("meta", {})
    curriculum = meta.get("curriculum_sequence", [])
    nodes = graph.get("nodes", {})

    print(f"\n=== COLD START DIAGNOSTIC: {args.domain.upper()} ===\n")
    print("Mục tiêu: xác định bloom level hiện tại của learner trước khi bắt đầu học.\n")
    print("Stage 2: Hỏi từng câu dưới đây, cập nhật update_graph.py sau mỗi câu.\n")
    print("-" * 60)

    count = 0
    for item in curriculum:
        if count >= args.limit:
            break
        concept = item["concept"]
        bloom_target = item.get("bloom_target", "apply")

        node = nodes.get(concept)
        if node:
            ls = node.get("learner_state", {})
            if ls.get("bloom_level") and ls["bloom_level"] != "remember":
                print(f"[SKIP] {concept} — already at bloom={ls['bloom_level']}")
                continue

        template = BLOOM_DIAGNOSTIC_TEMPLATES.get("understand", BLOOM_DIAGNOSTIC_TEMPLATES["understand"])
        question = template.replace("[concept]", concept.replace("_", " "))

        print(f"\nConcept [{count+1}]: {concept}")
        print(f"  bloom_target: {bloom_target}")
        if node:
            seeds = node.get("source_content", {}).get("misconception_seeds", [])
            if seeds:
                print(f"  misconception_seeds: {seeds}")
        print(f"\n  DIAGNOSTIC QUESTION:")
        print(f"  → \"{question}\"")
        print(f"\n  After answer: python update_graph.py --domain {args.domain} --concept {concept} --result [correct|incorrect] --bloom understand")

        count += 1

    if count == 0:
        print("Tất cả concepts trong curriculum đã có learner_state. Dùng review_scanner.py để xem concepts đến hạn.")

    print("\n" + "-" * 60)
    print(f"Diagnostic gồm {count} concept(s). Stage 2 cập nhật sau từng câu — không chờ hết {count} câu.")


if __name__ == "__main__":
    main()
