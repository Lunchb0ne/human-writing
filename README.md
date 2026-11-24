# human-writing

An agent skill for writing and editing prose so that humans can read it cleanly on a single pass.

Grounded in Clark, Martin, and Mahowald (2026), [*Why is AI-generated language so hard to understand?*](https://arxiv.org/abs/2610.29162) (`arXiv:2610.29162`), this skill targets the syntactic compression habits that post-trained models pick up from coding, math, and verifiable-reward training.

## How it differs from similar skills

- **`blader/humanizer`** removes AI vocabulary clichés, forced triads, and promotional fluff.
- **`plain-writing`** favors brevity and direct language.
- **`human-writing`** fixes syntactic parsing friction: missing `that` and `so that` cues, stacked noun compounds, inanimate subjects paired with human verbs, long subject-verb separations, ad-hoc denominal verbs, and telegraphic fragments, without padding text or dropping technical facts.

## Before and after

Read each version once, from top to bottom, without going back. Notice where you have to stop and re-read a sentence in your head.

**Before** (an incident note written to show the compressed style that the paper describes):

> The sync retry backoff controller (added in v3.1 after the March outage to stop thundering-herd reconnects from mobile clients on flaky networks) remembers each device's last failure and doubles the delay the server returns. The queue worker health check endpoint decides which workers stay in rotation, but it doesn't know about jobs the scheduler already leased, so a worker the check marks unhealthy can still hold leases for up to 90 seconds. We calendar'd a fix for Q3. Until then, `sync.config`'s `maxLeaseSeconds` controls how long orphaned jobs wait, and the dashboard alert threshold settings page lets on-call lower it. Lowering it too far makes workers drop jobs they're still processing, which the retry controller then sees as failures and backs off on, slowing every device the worker served. New flag `--drain-before-restart` (default off). Ops teams running more than 8 workers per region should enable it so restarts don't strand leases.

**After** (rewritten with `human-writing`):

> We added the controller that handles retry backoff for sync in v3.1, after the March outage. Its purpose is to stop mobile clients on flaky networks from reconnecting all at once in a thundering herd. The controller stores the last failure for each device and doubles the delay that the server returns.
>
> The health check endpoint for queue workers determines which workers stay in rotation. However, it does not track jobs that the scheduler has already leased, so a worker that the check marks as unhealthy can still hold leases for up to 90 seconds. We have scheduled a fix for Q3.
>
> Until then, the `maxLeaseSeconds` setting in `sync.config` controls how long orphaned jobs wait. On-call engineers can lower it from the dashboard, on the page that sets alert thresholds. If they lower it too far, workers drop jobs that they are still processing. The retry controller then records those drops as failures and backs off, which slows every device that the worker served.
>
> We also added a new flag, `--drain-before-restart`, which is off by default. Ops teams that run more than 8 workers per region should enable it so that restarts do not strand leases.

The rewrite keeps every identifier, number, and caveat. It restores dropped `that` and `so that` cues, unpacks noun stacks such as "queue worker health check endpoint", replaces "remembers" and "doesn't know" with literal verbs, moves the long parenthetical out from between the subject and its verb, and turns the fragment about the new flag into a sentence. On `evals/score.py`, the penalty drops from 12.74 to 1.27 per 100 words, at the cost of 40 extra words.

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
