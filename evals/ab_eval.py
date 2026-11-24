#!/usr/bin/env python3
"""Prepare blinded A/B comparison pairs and tally judge results."""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_outputs(path: Path) -> dict[str, str]:
    return {row["id"]: row["output"] for row in load_jsonl(path)}


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def cmd_prepare(args: argparse.Namespace) -> int:
    """Create randomized blind A/B pairs and the matching unblinding key."""
    corpus = [row for row in load_jsonl(args.corpus) if args.split in ("all", row.get("split"))]
    if not corpus:
        raise SystemExit(f"No items found for split '{args.split}' in {args.corpus}")
    outputs = {"baseline": load_outputs(args.baseline), "candidate": load_outputs(args.candidate)}
    for name, by_id in outputs.items():
        missing = [row["id"] for row in corpus if row["id"] not in by_id]
        if missing:
            raise SystemExit(f"Missing {name} outputs for ids: {', '.join(missing)}")

    rng = random.Random(args.seed)
    blind, key = [], {}
    for row in corpus:
        a, b = ("baseline", "candidate") if rng.random() < 0.5 else ("candidate", "baseline")
        blind.append({
            "id": row["id"],
            "domain": row.get("domain", ""),
            "prompt": row["prompt"],
            "input": row["input"],
            "must_preserve": row.get("must_preserve", []),
            "A": outputs[a][row["id"]],
            "B": outputs[b][row["id"]],
        })
        key[row["id"]] = {"A": a, "B": b}

    write_json(args.out_blind, blind)
    write_json(args.out_key, key)
    print(f"Prepared {len(blind)} blind pairs (seed={args.seed})")
    print(f"  blind: {args.out_blind}")
    print(f"  key:   {args.out_key}")
    return 0


def cmd_tally(args: argparse.Namespace) -> int:
    """Unblind judge outputs and compute win rate and preservation gates."""
    key = json.loads(args.key.read_text(encoding="utf-8"))
    judgments = {j["id"]: j for j in json.loads(args.judgments.read_text(encoding="utf-8"))}
    missing = [item_id for item_id in key if item_id not in judgments]
    if missing:
        raise SystemExit(f"Missing judgments for ids: {', '.join(missing)}")

    details = []
    for item_id, labels in key.items():
        judgment = judgments[item_id]
        winner = str(judgment.get("winner", "")).upper()
        if winner not in ("A", "B", "TIE"):
            raise SystemExit(f"Invalid winner '{winner}' for '{item_id}'")
        preserve = {labels["A"]: float(judgment["preserve_a"]), labels["B"]: float(judgment["preserve_b"])}
        if not all(1.0 <= p <= 5.0 for p in preserve.values()):
            raise SystemExit(f"Preservation scores out of [1, 5] for '{item_id}'")
        outcome = "TIE" if winner == "TIE" else "WIN" if labels[winner] == "candidate" else "LOSS"
        details.append({
            "id": item_id,
            "outcome": outcome,
            "raw_winner": winner,
            "candidate_preserve": preserve["candidate"],
            "baseline_preserve": preserve["baseline"],
            "clause": judgment.get("clause", ""),
        })

    outcomes = [d["outcome"] for d in details]
    wins, losses, ties = outcomes.count("WIN"), outcomes.count("LOSS"), outcomes.count("TIE")
    denom = wins + losses + 0.5 * ties
    win_rate = round(wins / denom, 4) if denom else 0.0
    cand_p = round(statistics.mean(d["candidate_preserve"] for d in details), 3) if details else 0.0
    base_p = round(statistics.mean(d["baseline_preserve"] for d in details), 3) if details else 0.0
    summary = {
        "total": len(details),
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "ab_win_rate": win_rate,
        "mean_preserve_candidate": cand_p,
        "mean_preserve_baseline": base_p,
        "preserve_gate_ok": cand_p >= 4.5,
    }

    print(
        f"A/B Tally: wins={wins}, losses={losses}, ties={ties}, "
        f"ab_win_rate={win_rate:.4f}, preserve_cand={cand_p:.3f}, "
        f"preserve_base={base_p:.3f}, gate_ok={summary['preserve_gate_ok']}"
    )
    for d in details:
        print(
            f"  {d['id']:12s} {d['outcome']:4s} "
            f"(cand_p={d['candidate_preserve']:.1f}, base_p={d['baseline_preserve']:.1f}) "
            f"- {d['clause']}"
        )
    print("Summary:", json.dumps(summary))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Blind A/B pair generator and tallier.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prep = subparsers.add_parser("prepare", help="Prepare blinded A/B items and key.")
    prep.add_argument("--corpus", type=Path, required=True)
    prep.add_argument("--split", choices=("dev", "test", "all"), default="dev")
    prep.add_argument("--baseline", type=Path, required=True)
    prep.add_argument("--candidate", type=Path, required=True)
    prep.add_argument("--seed", type=int, default=42)
    prep.add_argument("--out-blind", type=Path, required=True)
    prep.add_argument("--out-key", type=Path, required=True)
    prep.set_defaults(func=cmd_prepare)

    tally = subparsers.add_parser("tally", help="Unblind and tally judge decisions.")
    tally.add_argument("--key", type=Path, required=True)
    tally.add_argument("--judgments", type=Path, required=True)
    tally.set_defaults(func=cmd_tally)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
