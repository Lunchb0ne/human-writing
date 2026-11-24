# human-writing

Open-standard agent skill (`agentskills.io`) and evaluation harness for human-readable prose.

## Repository layout

- `skills/human-writing/SKILL.md` holds the skill instructions distributed by `npx skills add` and `.claude-plugin/`. Keep it concise and focused on the editing workflow.
- `skills/human-writing/references/research.md` holds the summary of Clark, Martin, and Mahowald (2026).
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` expose the skill for Claude Code plugin marketplaces.
- `evals/` holds the held-out `dev`/`test` corpus (`corpus.jsonl`), trigger suite (`triggers.json`), blind judging rubric (`rubric.md`), deterministic scorer (`score.py`), optimization runbook (`hillclimb.md`), and experiment log (`results.tsv`).

## Conventions

- Keep `skills/human-writing/` self-contained. Do not put test harnesses, eval data, or CI files inside `skills/human-writing/`.
- Do not inspect or optimize directly against `"split": "test"` entries in `evals/corpus.jsonl` or `evals/triggers.json` while iterating on `SKILL.md`.
- Record every kept and reverted `SKILL.md` iteration in `evals/results.tsv`.
- Verify changes to `SKILL.md` and docs with `mise run score-skill` (or `uv run python evals/score.py --text-file skills/human-writing/SKILL.md`).
