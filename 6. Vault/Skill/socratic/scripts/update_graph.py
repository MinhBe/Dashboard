"""
update_graph.py — Cập nhật learner_state trong knowledge-graph.json sau mỗi Q&A exchange.

Usage:
  python update_graph.py --domain mandarin --concept greetings_basic --result correct --bloom understand
  python update_graph.py --domain ai-concept --concept gradient_descent --result incorrect --hint_fail
  python update_graph.py --domain math-for-ai --concept vectors_and_spaces --result correct --bloom apply --transfer_pass
  python update_graph.py --domain ai-concept --concept backpropagation --misconception skips_edge_cases --example "bỏ qua batch dimension"
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

EXHIBIT_ROOT = Path(r"C:\Projects\Dashboard\5. Exhibit")

BLOOM_ORDER = ["remember", "understand", "apply", "analyze", "evaluate"]
BLOOM_WEIGHTS = {"remember": 1, "understand": 2, "apply": 3, "analyze": 4, "evaluate": 5}

REVIEW_INTERVALS = {
    "remember": timedelta(days=1),
    "understand": timedelta(days=3),
    "apply": timedelta(days=7),
    "analyze": timedelta(days=14),
    "evaluate": timedelta(days=14),
    "needs_restructure": timedelta(days=1),
}


def load_graph(domain: str) -> dict:
    path = EXHIBIT_ROOT / domain / "knowledge-graph.json"
    if not path.exists():
        print(f"ERROR: knowledge-graph.json not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_graph(domain: str, graph: dict):
    path = EXHIBIT_ROOT / domain / "knowledge-graph.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"Updated: {path}")


def get_node(graph: dict, concept: str) -> dict:
    node = graph["nodes"].get(concept)
    if node is None:
        print(f"ERROR: concept '{concept}' not found in graph.", file=sys.stderr)
        sys.exit(1)
    return node


def next_review_ts(bloom_level: str, needs_restructure: bool) -> str:
    key = "needs_restructure" if needs_restructure else bloom_level
    interval = REVIEW_INTERVALS.get(key, timedelta(days=7))
    dt = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + interval
    return dt.isoformat()


def bloom_up(current: str, target: str) -> str:
    ci = BLOOM_ORDER.index(current)
    ti = BLOOM_ORDER.index(target)
    if ci < ti:
        return BLOOM_ORDER[ci + 1]
    return current


def update_mastery(node: dict) -> float:
    ls = node["learner_state"]
    bloom = ls.get("bloom_level", "remember")
    target = node.get("bloom_target", "apply")
    bw = BLOOM_WEIGHTS
    mastery = bw[bloom] / bw[target]
    hint_fail_rate = min(ls.get("hint_fails_total", 0) / 10.0, 1.0)
    mastery = mastery * (1 - 0.2 * hint_fail_rate)
    return round(min(mastery, 1.0), 3)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--concept", required=True)
    parser.add_argument("--result", choices=["correct", "incorrect"])
    parser.add_argument("--bloom", help="Current bloom level at time of answer")
    parser.add_argument("--hint_fail", action="store_true", help="A hint attempt failed")
    parser.add_argument("--transfer_pass", action="store_true", help="Passed transfer question")
    parser.add_argument("--misconception", help="Misconception type id (from misconception-types.json)")
    parser.add_argument("--example", help="Example of the misconception observed")
    parser.add_argument("--belief_prior", help="Set belief_prior for the concept")
    args = parser.parse_args()

    graph = load_graph(args.domain)
    node = get_node(graph, args.concept)
    ls = node["learner_state"]
    now_ts = datetime.now().isoformat()

    if args.belief_prior:
        ls["belief_prior"] = args.belief_prior
        print(f"Set belief_prior: {args.belief_prior}")

    if args.hint_fail:
        ls["hint_fails_total"] = ls.get("hint_fails_total", 0) + 1
        if ls["hint_fails_total"] >= 2:
            ls["needs_restructure"] = True
            print(f"FLAGGED needs_restructure=true (hint_fails_total={ls['hint_fails_total']})")

    if args.result == "correct":
        ls["consecutive_correct"] = ls.get("consecutive_correct", 0) + 1
        bloom = ls.get("bloom_level", "remember")
        target = node.get("bloom_target", "apply")
        if ls["consecutive_correct"] >= 2:
            new_bloom = bloom_up(bloom, target)
            if new_bloom != bloom:
                ls["bloom_level"] = new_bloom
                ls["consecutive_correct"] = 0
                print(f"Bloom level up: {bloom} → {new_bloom}")
        ls["needs_restructure"] = False
        ls["next_review"] = next_review_ts(ls["bloom_level"], False)

    elif args.result == "incorrect":
        ls["consecutive_correct"] = 0
        ls["next_review"] = next_review_ts(ls.get("bloom_level", "remember"), ls.get("needs_restructure", False))

    if args.transfer_pass:
        print("Transfer question passed — concept on track for MASTERED tier 1.")

    if args.misconception:
        pm = ls.setdefault("personal_misconceptions", {})
        entry = pm.setdefault(args.misconception, {
            "count": 0,
            "confirmed": False,
            "first_seen": now_ts,
            "last_seen": now_ts,
            "examples": []
        })
        entry["count"] += 1
        entry["last_seen"] = now_ts
        if args.example:
            entry["examples"].append(args.example)
        if entry["count"] >= 2:
            entry["confirmed"] = True
            print(f"Misconception CONFIRMED: {args.misconception} (count={entry['count']})")

    ls["mastery_probability"] = update_mastery(node)

    save_graph(args.domain, graph)
    print(f"mastery_probability={ls['mastery_probability']}, bloom={ls.get('bloom_level')}, next_review={ls.get('next_review')}")


if __name__ == "__main__":
    main()
