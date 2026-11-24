# Evaluation Rubric

Use this rubric when comparing a candidate `SKILL.md` rewrite (`B`) against either the raw input or a baseline rewrite (`A`). Always randomize A/B order across items and judge with a model family different from the writer.

## 1. Hard Gates (Reject Candidate on Failure)

1. **Fact and symbol preservation (score 1 to 5, must be >= 4.5 mean and 100% `must_preserve` match):**
   - Every identifier, file path, flag, command, number, URL, and caveat in `must_preserve` must appear intact.
   - No claims may be invented, weakened into ambiguity, or dropped.
2. **Length sanity (mean word ratio in `[0.75, 1.35]`):**
   - Reject rewrites that pad text with filler or delete substance to hit brevity.

## 2. Diagnostic Psycholinguistic Checks

Count remaining instances per item:
- Dropped `that` or `so that` where a reader can mis-attach a clause.
- Noun stacks of three or more nouns.
- Inanimate subjects paired with mental or human verbs.
- Verbs delayed past long parentheticals or multi-item lists.
- Ad-hoc denominal verbs or adjacent noun/verb collisions.
- Telegraphic fragments or awkward inanimate `'s` genitives.

## 3. Primary Comprehension Judgment (Blind A/B)

Ask the judge:

> Which version is easier for a human engineer to understand on a single left-to-right read without re-parsing, while keeping every technical fact intact and avoiding filler? Reply with `A`, `B`, or `TIE`, and cite the specific clause that drove your choice.

Compute `ab_win_rate = wins / (wins + losses + 0.5 * ties)` (or track ties separately). Keep a `SKILL.md` edit only if hard gates pass, `ab_win_rate` improves (or holds equal with a simpler `SKILL.md`), and `evals/score.py` confirms lower `psych_penalty`.
