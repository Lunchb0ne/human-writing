#!/usr/bin/env python3
"""Synthetic unit tests for evals/score.py (never touches test split data)."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EVALS_DIR))

import score  # noqa: E402


class ScorePsycholinguisticTests(unittest.TestCase):
    def test_inanimate_mental_verbs_positive_and_clean(self) -> None:
        bad = (
            "The cache manager (built last month to reduce latency) remembers recent tokens, "
            "`widget.js` doesn't know the state, and tight memory constraints bite under load."
        )
        good = (
            "The cache manager stores recent tokens, `widget.js` ignores the state, "
            "and tight memory limits slow down requests under load."
        )
        m_bad = score.score_text(bad)
        m_good = score.score_text(good)
        self.assertGreaterEqual(m_bad["inanimate_mental_verbs"], 3)
        self.assertEqual(m_good["inanimate_mental_verbs"], 0)

    def test_human_subjects_not_flagged_as_inanimate(self) -> None:
        text = "Engineers remember why language models learn compressed syntax when reviewers ask questions."
        m = score.score_text(text)
        self.assertEqual(m["inanimate_mental_verbs"], 0)

    def test_reduced_orcs_positive_and_clean(self) -> None:
        bad = (
            "We shipped the three settings we needed, tracked records each worker reads, "
            "and dropped packets the client kept."
        )
        good = (
            "We shipped the three settings that we needed, tracked records that each worker reads, "
            "and dropped packets that the client kept."
        )
        idiom = "That is the way we wrote it the first time we tried."
        m_bad = score.score_text(bad)
        m_good = score.score_text(good)
        m_idiom = score.score_text(idiom)
        self.assertGreaterEqual(m_bad["reduced_orcs"], 3)
        self.assertEqual(m_good["reduced_orcs"], 0)
        self.assertEqual(m_idiom["reduced_orcs"], 0)

    def test_stacked_nouns_positive_and_clean(self) -> None:
        bad = "We updated the connection pool retry budget config."
        good = "We updated the config that controls the retry budget for the connection pool."
        m_bad = score.score_text(bad)
        m_good = score.score_text(good)
        self.assertGreaterEqual(m_bad["stacked_nouns"], 1)
        self.assertEqual(m_good["stacked_nouns"], 0)

    def test_dropped_so_that_vs_comma_result(self) -> None:
        purpose_bad = "We pinned the release version so builds finish reliably."
        purpose_good = "We pinned the release version so that builds finish reliably."
        result_good = "The queue drained quickly, so workers stayed idle."
        self.assertGreaterEqual(score.score_text(purpose_bad)["dropped_so_that"], 1)
        self.assertEqual(score.score_text(purpose_good)["dropped_so_that"], 0)
        self.assertEqual(score.score_text(result_good)["dropped_so_that"], 0)

    def test_denominal_collisions_and_genitives(self) -> None:
        bad = (
            "`router.ts` routes calls, `package.json`'s version field changed, "
            "and we calendar'd a review after actions were bucketed."
        )
        good = (
            "`router.ts` forwards calls, the version field in `package.json` changed, "
            "and we scheduled a review after user actions were grouped."
        )
        m_bad = score.score_text(bad)
        m_good = score.score_text(good)
        self.assertGreaterEqual(m_bad["word_collisions"], 1)
        self.assertGreaterEqual(m_bad["inanimate_genitives"], 1)
        self.assertGreaterEqual(m_bad["denominal_verbs"], 2)
        self.assertEqual(m_good["word_collisions"], 0)
        self.assertEqual(m_good["inanimate_genitives"], 0)
        self.assertEqual(m_good["denominal_verbs"], 0)

    def test_long_parenthetical_and_spacy_fragments(self) -> None:
        bad_paren = (
            "The primary worker (configured across three availability zones with strict timeouts) "
            "drains the pending queue."
        )
        good_paren = "The primary worker drains the pending queue across three availability zones with strict timeouts."
        m_bad = score.score_text(bad_paren)
        m_good = score.score_text(good_paren)
        self.assertGreaterEqual(m_bad["long_parentheticals"], 1)
        self.assertEqual(m_good["long_dependencies"], 0)

        frag = "Updated build artifact upload step. New setting timeoutMs (100 to 500)."
        full = "We updated the upload step for build artifacts. We added a `timeoutMs` setting from 100 to 500."
        self.assertGreaterEqual(score.score_text(frag)["fragments"], 1)
        self.assertEqual(score.score_text(full)["fragments"], 0)

    def test_before_examples_excluded_by_default(self) -> None:
        sample = (
            "# Guide\n\n"
            "Write clear sentences for readers.\n\n"
            '1. Keep glue words.\n'
            '   - Before: "We copied the three settings we needed so it stays clear."\n'
            '   - After: "We copied the three settings that we needed so that it stays clear."\n'
        )
        excluded = score.score_text(sample, exclude_before_examples=True)
        included = score.score_text(sample, exclude_before_examples=False)
        self.assertEqual(excluded["reduced_orcs"], 0)
        self.assertEqual(excluded["dropped_so_that"], 0)
        self.assertGreaterEqual(included["reduced_orcs"], 1)
        self.assertGreaterEqual(included["dropped_so_that"], 1)

    def test_check_preserved_and_strict_gate(self) -> None:
        self.assertEqual(score.check_preserved("Use v2.4 with TTL=30", ["v2.4", "TTL"]), [])
        self.assertEqual(score.check_preserved("Use v2.4 only", ["v2.4", "TTL"]), ["TTL"])

        corpus_row = {
            "id": "syn-01",
            "split": "dev",
            "domain": "technical-docs",
            "prompt": "Rewrite clearly.",
            "input": "The retry budget monitor remembers `MAX_RETRIES=3` so queues stay healthy.",
            "must_preserve": ["MAX_RETRIES=3"],
        }
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)

            def write_jsonl(name: str, row: dict) -> str:
                path = tmp_dir / name
                path.write_text(json.dumps(row) + "\n", encoding="utf-8")
                return str(path)

            corpus = write_jsonl("corpus.jsonl", corpus_row)

            def strict_rc(output: str) -> int:
                outputs = write_jsonl("outputs.jsonl", {"id": "syn-01", "output": output})
                with contextlib.redirect_stdout(io.StringIO()):
                    return score.main(["--corpus", corpus, "--outputs", outputs, "--strict", "--json"])

            self.assertEqual(strict_rc("The monitor tracks `MAX_RETRIES=3` so that the queues remain healthy."), 0)
            self.assertEqual(strict_rc("The monitor tracks retries so that queues remain healthy."), 1)


if __name__ == "__main__":
    unittest.main()
