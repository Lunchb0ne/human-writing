# human-writing

An agent skill for writing and editing prose so that humans can read it cleanly on a single pass.

Grounded in Clark, Martin, and Mahowald (2026), [*Why is AI-generated language so hard to understand?*](https://arxiv.org/abs/2610.29162) (`arXiv:2610.29162`), this skill targets the syntactic compression habits that post-trained models pick up from coding, math, and verifiable-reward training.

## How it differs from similar skills

- **`blader/humanizer`** removes AI vocabulary clichés, forced triads, and promotional fluff.
- **`plain-writing`** favors brevity and direct language.
- **`human-writing`** fixes syntactic parsing friction: missing `that` and `so that` cues, stacked noun compounds, inanimate subjects paired with human verbs, long subject-verb separations, ad-hoc denominal verbs, and telegraphic fragments, without padding text or dropping technical facts.

## Installation

### Universal (`npx skills`)

Works across Claude Code, Codex, Cursor, Antigravity, OpenCode, Windsurf, and other `agentskills.io` tools:

```bash
npx skills add lunchb0ne/human-writing --global
```

Or target specific agents:

```bash
npx skills add lunchb0ne/human-writing --global --agent claude-code cursor codex
```

### Claude Code Plugin Marketplace

```text
/plugin marketplace add lunchb0ne/human-writing
/plugin install human-writing@human-writing
```

### Manual / Symlink (Antigravity, Claude Code, Codex)

```bash
git clone https://github.com/lunchb0ne/human-writing.git
ln -s "$PWD/human-writing/skills/human-writing" ~/.gemini/config/skills/human-writing
ln -s "$PWD/human-writing/skills/human-writing" ~/.claude/skills/human-writing
```

## Measuring and Hillclimbing the Skill

See [`evals/hillclimb.md`](./evals/hillclimb.md) for the `autoresearch`-style optimization loop and [`evals/rubric.md`](./evals/rubric.md) for the blind A/B judging rubric.

Provision Python 3.12, `uv`, and the `spaCy` environment (`en_core_web_sm`) in `.venv` using `mise`:

```bash
mise install
mise run sync
mise run test
mise run score-dev
mise run score-skill
```

Run ad-hoc scoring or validate a rewrite batch against hard preservation and length gates:

```bash
mise run score -- --text-file README.md
mise run score -- --corpus evals/corpus.jsonl --split dev --outputs evals/runs/iter-00.jsonl --strict
```

Without `mise`, use `uv run python evals/score.py ...` directly.

## License

[MIT](./LICENSE)
