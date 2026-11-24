# Hillclimbing `skills/human-writing/SKILL.md`

Follow an `autoresearch`-style keep/revert loop against a clear quantitative baseline rather than tuning prompts by feel.

## 1. Establish the Baseline (`dev` split only)

1. Run `mise run score-dev` (or `uv run python evals/score.py --corpus evals/corpus.jsonl --split dev`) to record raw input scores.
2. Generate rewrites for the 8 `dev` prompts in two modes using at least two model families (for example, one Claude model and one Gemini or GPT model) so instructions do not overfit a single model:
   - `no-skill`: prompt alone (`evals/runs/baseline-noskill.jsonl`)
   - `v0`: prompt plus `skills/human-writing/SKILL.md` (`evals/runs/iter-00.jsonl`)
3. Score `iter-00.jsonl` with:
   ```bash
   mise run score -- --corpus evals/corpus.jsonl --split dev --outputs evals/runs/iter-00.jsonl --strict
   ```
4. Run blind A/B judging (`evals/rubric.md`) between `baseline-noskill` and `iter-00` using a separate judge model family with A/B order randomized across items.
5. Append the baseline row to `evals/results.tsv`.

## 2. Optimize `SKILL.md` in Single-Hypothesis Steps

Repeat on `split = dev` only (keep `split = test` untouched until the end):

1. **Inspect failures:** Pick the 2 or 3 worst `dev` items by `output_penalty`, lost caveats, or judge losses.
2. **Form one hypothesis:** Edit `skills/human-writing/SKILL.md` to fix one specific failure mode (for example, tighten an instruction, add one before/after example, or remove a rule that causes over-long prose). Keep `SKILL.md` concise; shorter instructions that score the same are better.
3. **Run candidate outputs:** Generate `evals/runs/iter-NN.jsonl` across the same model mix.
4. **Gate and compare:**
   - **Hard gate:** `--strict` must exit `0` (`100%` `must_preserve` verbatim match, word length ratio in `[0.75, 1.35]`), and preservation score must be `>= 4.5/5`.
   - **Keep rule:** Keep and `git commit` if blind A/B win rate against the previous kept best beats `50%` and `mean_output_penalty` drops (or ties with fewer words in `SKILL.md`).
   - **Revert rule:** Otherwise run `git checkout -- skills/human-writing/SKILL.md`, record the rejected hypothesis in `evals/results.tsv` so you do not retry it, and move on.

## 3. Optimize Frontmatter Discovery (`evals/triggers.json`)

After body instructions plateau:

1. Test whether each prompt in the `dev` split of `evals/triggers.json` activates `human-writing` from `name` and `description` alone.
2. Mutate only `description` in `skills/human-writing/SKILL.md` to raise trigger F1 (catching prose-editing prompts while staying silent on pure code/SQL/test prompts).

## 4. Final Holdout Check (`test` split)

Once optimization on `dev` converges:

1. Run `mise run score -- --corpus evals/corpus.jsonl --split test --outputs ... --strict`, blind A/B judge on the 4 `test` items, and `test` trigger checks.
2. Spot-check at least 5 blind A/B pairs yourself by reading them cold. If your judgment disagrees with the automated metrics, fix the rubric or scorer before continuing.
