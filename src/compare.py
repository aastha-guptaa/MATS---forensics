#!/usr/bin/env python3
"""Compare hand-labeled annotations (labels.json) with auto-grader output (auto_labels.json).

Computes:
1. Exact match accuracy for highest_rung.
2. Set exact match for rungs_present.
3. Mean Jaccard similarity across rungs_present sets.
4. Agreement rates on boolean fields (disclaim, wc_proxy, ambiguous).
5. Trivial baseline accuracy (predicting the most frequent hand-labeled highest_rung).
"""
import argparse
import json
from collections import Counter


def jaccard_similarity(set_a: set, set_b: set) -> float:
    """Compute Jaccard similarity coefficient between two sets."""
    if not set_a and not set_b:
        return 1.0
    union = set_a | set_b
    if not union:
        return 1.0
    return len(set_a & set_b) / len(union)


def load_hand_labels(path: str) -> dict:
    with open(path) as f:
        data = json.load(f)
    return {r["index"]: r for r in data}


def load_auto_labels(path: str) -> dict:
    auto = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if not r.get("error"):
                auto[r["index"]] = r
    return auto


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hand", default="experiments/e01/labels.json", help="Path to hand labels JSON")
    parser.add_argument("--auto", default="experiments/e01/auto_labels.json", help="Path to auto labels JSONL")
    parser.add_argument("--out", default=None, help="Optional output JSON path for results summary")
    args = parser.parse_args()

    hand = load_hand_labels(args.hand)
    auto = load_auto_labels(args.auto)

    common_indices = sorted(set(hand.keys()) & set(auto.keys()))
    n = len(common_indices)
    if n == 0:
        print("No matching indices found to compare.")
        return

    # Trivial baseline (most common highest_rung in hand labels)
    hand_highest_counts = Counter(hand[i]["highest_rung"] for i in common_indices)
    mode_rung, mode_count = hand_highest_counts.most_common(1)[0]
    trivial_accuracy = mode_count / n

    # Highest rung exact match
    highest_exact_matches = sum(
        1 for i in common_indices if hand[i].get("highest_rung") == auto[i].get("highest_rung")
    )
    highest_exact_rate = highest_exact_matches / n

    # Set exact match & Jaccard
    set_exact_matches = sum(
        1 for i in common_indices if set(hand[i].get("rungs_present", [])) == set(auto[i].get("rungs_present", []))
    )
    set_exact_rate = set_exact_matches / n

    jaccards = [
        jaccard_similarity(set(hand[i].get("rungs_present", [])), set(auto[i].get("rungs_present", [])))
        for i in common_indices
    ]
    mean_jaccard = sum(jaccards) / n

    # Boolean field agreements
    bool_fields = ["disclaim", "wc_proxy", "ambiguous"]
    bool_agreement = {}
    for field in bool_fields:
        matches = sum(1 for i in common_indices if hand[i].get(field) == auto[i].get(field))
        bool_agreement[field] = matches / n

    # Find highest_rung mismatches
    highest_mismatches = []
    for i in common_indices:
        h_hr = hand[i].get("highest_rung")
        a_hr = auto[i].get("highest_rung")
        if h_hr != a_hr:
            highest_mismatches.append({
                "index": i,
                "prompt_id": hand[i].get("prompt_id"),
                "hand_highest": h_hr,
                "auto_highest": a_hr,
                "hand_rungs": hand[i].get("rungs_present"),
                "auto_rungs": auto[i].get("rungs_present"),
            })

    results = {
        "n_compared": n,
        "trivial_baseline": {
            "mode_rung": mode_rung,
            "accuracy": trivial_accuracy,
        },
        "highest_rung_exact_match": highest_exact_rate,
        "rungs_present_set_exact_match": set_exact_rate,
        "rungs_present_mean_jaccard": mean_jaccard,
        "bool_field_agreement": bool_agreement,
        "highest_rung_mismatches": highest_mismatches,
    }

    print("=== Agreement Summary ===")
    print(f"Hand Records: {len(hand)} | Auto Records: {len(auto)} | Common Compared (n): {n}")
    print(f"Trivial Baseline (always '{mode_rung}'): {trivial_accuracy:.2%}")
    print(f"Highest Rung Exact Match: {highest_exact_rate:.2%} ({highest_exact_matches}/{n})")
    print(f"Rungs Present Set Exact Match: {set_exact_rate:.2%} ({set_exact_matches}/{n})")
    print(f"Rungs Present Mean Jaccard: {mean_jaccard:.4f}")
    print("Boolean Agreement:")
    for k, v in bool_agreement.items():
        print(f"  {k}: {v:.2%}")

    if args.out:
        with open(args.out, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results written to {args.out}")


if __name__ == "__main__":
    main()
