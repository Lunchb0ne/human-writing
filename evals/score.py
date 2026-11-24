#!/usr/bin/env python3
"""Pure-spaCy psycholinguistic readability scorer for human-writing.

Grounded in Clark, Martin, & Mahowald (2026) (arXiv:2610.29162v1).
Requires spaCy (en_core_web_trf, en_core_web_md, or en_core_web_sm).
"""

from __future__ import annotations

import argparse
import functools
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any

# Verbs that presuppose a mind or body; odd with an inanimate subject.
ANIMATE_VERBS = {
    "remember", "forget", "know", "refuse", "shake", "learn", "understand",
    "want", "prefer", "care", "expect", "ask", "bite", "swallow", "eat",
    "tell", "respect", "decide", "think", "believe", "feel", "notice",
    "realize", "assume", "trust", "complain", "promise", "agree", "choose",
    "sleep", "wake",
}
HUMAN_LEMMAS = {
    "person", "people", "human", "reader", "writer", "user", "developer",
    "engineer", "reviewer", "teammate", "author", "editor", "maintainer",
    "operator", "client", "customer", "team", "group", "crew", "staff",
    "admin", "owner", "member", "student", "researcher", "model", "agent",
    "assistant", "someone", "anyone", "everyone", "nobody", "who",
}
DENOMINAL_VERBS = {
    "calendar", "calendar'd", "action", "task", "bucket",
    "sunset", "greenlight", "architect", "whiteboard", "roadmap",
}
ORC_IDIOM_HEADS = {"way", "time", "day", "moment", "reason", "place"}
RELATIVIZERS = {"that", "which", "who", "whom", "whose", "where", "when", "why"}
SKIP_ENTITIES = {"PERSON", "ORG", "NORP", "GPE"}
PROPER_SKIP = {"PERSON", "ORG", "WORK_OF_ART", "GPE"}
COLLISION_STOPWORDS = {"that", "this", "will", "been"}
SUBJECT_DEPS = ("nsubj", "nsubjpass")
NOMINAL_POS = ("NOUN", "PROPN")
WIKI_BINS = ((1, 5), (6, 10), (11, 15), (16, 20), (21, 30))

WEIGHTS = {
    "inanimate_mental_verbs": 2.0,
    "reduced_orcs": 1.5,
    "stacked_nouns": 1.5,
    "denominal_verbs": 1.5,
    "word_collisions": 1.5,
    "dropped_so_that": 1.0,
    "inanimate_genitives": 1.0,
    "long_dependencies": 1.0,
    "long_sentences_gt32": 1.0,
    "fragments": 1.0,
}

FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.S)
FENCED_CODE_RE = re.compile(r"```.*?```", re.S)
BEFORE_EXAMPLE_RE = re.compile(r"^\s*[-*+]\s+Before:\s+.*$", re.M | re.I)
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
HEADING_RE = re.compile(r"^#{1,6}\s+.*$", re.M)
LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+", re.M)
LONG_PAREN_RE = re.compile(r"\([^)]{22,}\)")
COLLISION_EXACT_RE = re.compile(r"\b(?P<stem>[a-z]{4,12})(?:\.[a-z0-9]{1,5})?\s+(?P=stem)(?:s|es|ed|ing)?\b", re.I)
COLLISION_ER_RE = re.compile(r"\b(?P<stem>[a-z]{3,12})er(?:\.[a-z0-9]{1,5})\s+(?P=stem)e?(?:s|ed|ing)\b", re.I)


@functools.cache
def _load_spacy() -> tuple[Any, str]:
    try:
        import spacy  # type: ignore
    except ImportError as exc:
        raise SystemExit("spaCy and en_core_web_sm are required. Run: mise install && mise run sync") from exc
    for name in ("en_core_web_trf", "en_core_web_md", "en_core_web_sm"):
        try:
            return spacy.load(name), name
        except OSError:
            continue
    raise SystemExit("spaCy and en_core_web_sm are required. Run: mise install && mise run sync")


def strip_markdown_scaffolding(text: str, exclude_before_examples: bool = True) -> str:
    """Strip YAML frontmatter, code blocks, headings, list markers, and optional Before examples."""
    text = FRONTMATTER_RE.sub("", text)
    text = FENCED_CODE_RE.sub(" ", text)
    if exclude_before_examples:
        text = BEFORE_EXAMPLE_RE.sub("", text)
    text = MD_LINK_RE.sub(r"\1", text)
    text = HEADING_RE.sub("", text)
    text = LIST_MARKER_RE.sub("", text)
    return " ".join(ln.strip() for ln in text.splitlines() if ln.strip())


def _is_inanimate(tok: Any) -> bool:
    return tok.lower_ == "module" or (
        tok.pos_ == "NOUN"
        and tok.ent_type_ not in SKIP_ENTITIES
        and tok.lemma_.lower() not in HUMAN_LEMMAS
    )


def _is_rel_pronoun(tok: Any) -> bool:
    return tok.lower_ in RELATIVIZERS or "Rel" in tok.morph.get("PronType")


def _compounds(tok: Any) -> list[Any]:
    found = []
    for child in tok.children:
        if child.dep_ == "compound" and child.pos_ in NOMINAL_POS:
            found += [child, *_compounds(child)]
    return found


def _count_compound_stacks(doc: Any) -> int:
    count = 0
    for tok in doc:
        if tok.pos_ not in NOMINAL_POS or (tok.dep_ == "compound" and tok.head.pos_ in NOMINAL_POS):
            continue
        chain = [tok, *_compounds(tok)]
        if len(chain) >= 3 and not all(t.pos_ == "PROPN" and t.ent_type_ in PROPER_SKIP for t in chain):
            count += 1
    return count


def _is_reduced_orc(verb: Any, doc: Any) -> bool:
    head = verb.head
    is_rel_verb = verb.dep_ == "relcl" or (verb.dep_ == "acl" and verb.tag_ in ("VBZ", "VBP", "VBD"))
    if not is_rel_verb or head.pos_ not in NOMINAL_POS or head.lemma_.lower() in ORC_IDIOM_HEADS:
        return False
    if verb.i <= head.i:
        return False
    subjects = [c for c in verb.children if c.dep_ in SUBJECT_DEPS]
    if not subjects or any(_is_rel_pronoun(s) for s in subjects):
        return False
    return not any(_is_rel_pronoun(t) for t in [*doc[head.i + 1 : verb.i], *verb.children])


def _is_purpose_so(tok: Any) -> bool:
    sent = tok.sent
    if tok.lower_ != "so" or tok.i + 1 >= sent.end:
        return False
    if tok.i > sent.start and tok.doc[tok.i - 1].text in (",", ";", "—", "--"):
        return False
    nxt = tok.doc[tok.i + 1]
    if nxt.lower_ == "that" or nxt.is_punct:
        return False
    if tok.dep_ == "mark" and tok.head.dep_ in ("advcl", "conj", "ccomp"):
        return True
    if tok.head.dep_ in ("advcl", "ccomp") and tok.i < tok.head.i:
        return True
    return any(
        v.dep_ in ("advcl", "ccomp")
        and v.i > tok.i
        and any(c.dep_ in (*SUBJECT_DEPS, "expl") and tok.i < c.i <= tok.i + 3 and c.i < v.i for c in v.children)
        for v in sent
    )


def _is_fragment(sent: Any) -> bool:
    words = [t for t in sent if not t.is_punct and not t.is_space]
    if len(words) < 2:
        return False
    root = sent.root
    subjectless_past = (
        root.pos_ == "VERB"
        and root.tag_ in ("VBD", "VBN")
        and root.lower_ != root.lemma_.lower()
        and not any(c.dep_ in (*SUBJECT_DEPS, "expl") for c in root.children)
        and not any(c.tag_ == "VB" for c in root.children)
    )
    has_finite = any(t.tag_ in ("VB", "VBP", "VBZ", "VBD", "MD") or t.pos_ == "AUX" for t in words)
    return subjectless_past or (len(words) >= 3 and not has_finite)


def _count_word_collisions(unwrapped: str) -> int:
    exact = sum(m.group("stem").lower() not in COLLISION_STOPWORDS for m in COLLISION_EXACT_RE.finditer(unwrapped))
    return exact + len(COLLISION_ER_RE.findall(unwrapped))


def score_text(raw_text: str, exclude_before_examples: bool = True) -> dict[str, Any]:
    """Compute readability metrics and psycholinguistic penalty per 100 words."""
    nlp, model_name = _load_spacy()
    prose = strip_markdown_scaffolding(raw_text, exclude_before_examples=exclude_before_examples)
    unwrapped = INLINE_CODE_RE.sub(lambda m: m.group(1).strip(), prose)
    doc = nlp(INLINE_CODE_RE.sub("module", prose))

    sent_lengths: list[int] = []
    all_arcs: list[int] = []
    bin_arcs: list[list[int]] = [[] for _ in WIKI_BINS]
    fragments = 0

    for sent in doc.sents:
        words = [t for t in sent if not t.is_punct and not t.is_space]
        if not words:
            continue
        sent_lengths.append(len(words))
        arcs = [abs(t.i - t.head.i) for t in sent if t.dep_ != "ROOT" and not t.is_punct and not t.head.is_punct]
        all_arcs.extend(arcs)
        for (lo, hi), bucket in zip(WIKI_BINS, bin_arcs):
            if lo <= len(words) <= hi:
                bucket.extend(arcs)
        fragments += _is_fragment(sent)

    long_parens = len(LONG_PAREN_RE.findall(unwrapped))
    long_subj_verb = sum(
        t.dep_ in SUBJECT_DEPS and not _is_rel_pronoun(t) and abs(t.i - t.head.i) >= 6 for t in doc
    )
    mean_dep_len = round(statistics.mean(all_arcs), 3) if all_arcs else 0.0
    bin_means = [statistics.mean(b) for b in bin_arcs if b]

    result: dict[str, Any] = {
        "words": sum(sent_lengths),
        "sentences": len(sent_lengths),
        "mean_sentence_words": round(statistics.mean(sent_lengths), 2) if sent_lengths else 0.0,
        "sentence_len_std": round(statistics.pstdev(sent_lengths), 2) if len(sent_lengths) > 1 else 0.0,
        "long_sentences_gt32": sum(n > 32 for n in sent_lengths),
        "stacked_nouns": _count_compound_stacks(doc),
        "inanimate_mental_verbs": sum(
            t.dep_ in SUBJECT_DEPS
            and t.head.pos_ == "VERB"
            and t.head.lemma_.lower() in ANIMATE_VERBS
            and _is_inanimate(t)
            for t in doc
        ),
        "reduced_orcs": sum(_is_reduced_orc(t, doc) for t in doc),
        "dropped_so_that": sum(_is_purpose_so(t) for t in doc),
        "denominal_verbs": sum(t.pos_ == "VERB" and t.lemma_.lower() in DENOMINAL_VERBS for t in doc),
        "inanimate_genitives": sum(
            t.dep_ == "poss"
            and _is_inanimate(t)
            and any(c.dep_ == "case" and c.lower_ in ("'s", "’s") for c in t.children)
            for t in doc
        ),
        "word_collisions": _count_word_collisions(unwrapped),
        "long_parentheticals": long_parens,
        "long_dependencies": max(long_parens, long_subj_verb),
        "fragments": fragments,
        "mean_dep_len": mean_dep_len,
        "std_dep_len": round(statistics.mean(bin_means), 3) if bin_means else mean_dep_len,
    }
    weighted = sum(weight * result[key] for key, weight in WEIGHTS.items())
    result["psych_penalty_per_100w"] = round(weighted / max(result["words"], 1) * 100.0, 2)
    result["analyzer"] = model_name
    return result


def check_preserved(text: str, must_preserve: list[str]) -> list[str]:
    return [item for item in must_preserve if item not in text]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _score_row(row: dict[str, Any], outputs: dict[str, str] | None) -> dict[str, Any]:
    in_metrics = score_text(row["input"], exclude_before_examples=False)
    must_preserve = row.get("must_preserve", [])
    report = {"id": row["id"], "split": row["split"], "domain": row["domain"]}
    if outputs is None:
        return report | {
            "penalty": in_metrics["psych_penalty_per_100w"],
            "preserve_ok": not check_preserved(row["input"], must_preserve),
            "metrics": in_metrics,
        }
    if row["id"] not in outputs:
        raise SystemExit(f"Missing output for corpus item '{row['id']}'")
    output = outputs[row["id"]]
    out_metrics = score_text(output, exclude_before_examples=False)
    missing = check_preserved(output, must_preserve)
    in_pen, out_pen = in_metrics["psych_penalty_per_100w"], out_metrics["psych_penalty_per_100w"]
    return report | {
        "input_penalty": in_pen,
        "output_penalty": out_pen,
        "delta": round(out_pen - in_pen, 2),
        "len_ratio": round(out_metrics["words"] / max(in_metrics["words"], 1), 3),
        "preserve_ok": not missing,
        "missing": missing,
        "metrics": out_metrics,
    }


def _mean(vals: Any, digits: int = 2) -> float:
    return round(statistics.mean(vals), digits)


def _summarize(rows: list[dict[str, Any]], split: str, with_outputs: bool) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "split": split,
        "count": len(rows),
        "analyzer": rows[0]["metrics"]["analyzer"] if rows else "none",
    }
    if not rows:
        return summary
    if with_outputs:
        summary |= {
            "mean_input_penalty": _mean(r["input_penalty"] for r in rows),
            "mean_output_penalty": _mean(r["output_penalty"] for r in rows),
            "mean_len_ratio": _mean((r["len_ratio"] for r in rows), 3),
            "preserve_pass_count": sum(r["preserve_ok"] for r in rows),
            "gate_failures": sum(not (0.75 <= r["len_ratio"] <= 1.35 and r["preserve_ok"]) for r in rows),
        }
    else:
        summary["mean_input_penalty"] = _mean(r["penalty"] for r in rows)
    summary["mean_std_dep_len"] = _mean((r["metrics"]["std_dep_len"] for r in rows), 3)
    return summary


def _format_row(r: dict[str, Any], with_outputs: bool) -> str:
    m = r["metrics"]
    prefix = f"  {r['id']:12s} [{r['domain']:17s}] "
    if with_outputs:
        return prefix + (
            f"penalty {r['input_penalty']:5.2f} -> {r['output_penalty']:5.2f} "
            f"(len={r['len_ratio']:.2f}, preserve={'ok' if r['preserve_ok'] else 'FAIL'}, std_dl={m['std_dep_len']:.2f})"
        )
    return prefix + (
        f"penalty={r['penalty']:5.2f} stacks={m['stacked_nouns']} inan_v={m['inanimate_mental_verbs']} "
        f"orc={m['reduced_orcs']} so_that={m['dropped_so_that']} gen={m['inanimate_genitives']} "
        f"coll={m['word_collisions']} denom={m['denominal_verbs']} dep={m['long_dependencies']} "
        f"frag={m['fragments']} std_dl={m['std_dep_len']:.2f}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score prose with arXiv:2610.29162v1 readability checks.")
    parser.add_argument("--text-file", type=Path, help="Score a single markdown or plain text file.")
    parser.add_argument("--corpus", type=Path, help="Path to evals/corpus.jsonl.")
    parser.add_argument("--outputs", type=Path, help="Optional JSONL with {id, output} pairs to evaluate.")
    parser.add_argument("--split", choices=("dev", "test", "all"), default="dev", help="Corpus split to score.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if preservation or length gates fail.")
    parser.add_argument("--include-examples", action="store_true", help="Include '- Before:' lines in markdown.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args(argv)
    if not args.text_file and not args.corpus:
        parser.error("Provide --text-file or --corpus")

    if args.text_file:
        metrics = score_text(args.text_file.read_text(encoding="utf-8"), not args.include_examples)
        if args.json:
            print(json.dumps(metrics, indent=2))
        else:
            print(f"File: {args.text_file} ({metrics['analyzer']})")
            for key, value in metrics.items():
                if key != "analyzer":
                    print(f"  {key}: {value}")
        return 0

    corpus = [row for row in load_jsonl(args.corpus) if args.split in ("all", row.get("split"))]
    outputs = {row["id"]: row["output"] for row in load_jsonl(args.outputs)} if args.outputs else None
    rows = [_score_row(row, outputs) for row in corpus]
    summary = _summarize(rows, args.split, outputs is not None)

    if args.json:
        print(json.dumps({"summary": summary, "items": rows}, indent=2))
    else:
        print(f"Split: {summary['split']} ({summary['count']} items, analyzer={summary['analyzer']})")
        for r in rows:
            print(_format_row(r, outputs is not None))
        print("Summary:", json.dumps(summary))

    return 1 if args.strict and summary.get("gate_failures") else 0


if __name__ == "__main__":
    sys.exit(main())
