# human-writing

This is an agent skill for writing and editing prose. It helps the agent write text that people can read cleanly on a single pass.

The skill is based on Clark, Martin, and Mahowald (2026), [*Why is AI-generated language so hard to understand?*](https://arxiv.org/abs/2610.29162) (`arXiv:2610.29162`). The paper shows that models compress their sentences after post-training on code, math, and tasks with verifiable rewards. They drop small words, stack nouns, and give objects human verbs. This skill undoes those habits. [`docs/related-work.md`](./docs/related-work.md) reviews related reading studies and the evidence behind each rule.

## How it differs from similar skills

- **`blader/humanizer`** removes clichéd AI vocabulary, forced lists of three, and promotional fluff.
- **`plain-writing`** favors brevity and direct language.
- **`human-writing`** fixes sentences that make a reader stop and re-read. It does this without padding the text or dropping technical facts. The table below shows the habits that it targets.

| Habit | Before | After |
|---|---|---|
| Dropped `that` | The test confirmed the cache we rebuilt the index for was stale. | The test confirmed that the cache that we rebuilt the index for was stale. |
| Stacked nouns | the cache invalidation pipeline manager | the manager for the cache invalidation pipeline |
| Objects with human verbs | `focusBand` remembers the index, and the docstring promises dotfiles are skipped. | `focusBand` stores the index, and the docstring says that dotfiles are skipped. |
| Long gap between subject and verb | Shared controls (buttons, inputs, switches, and carets) live in Sass. | Shared controls live in Sass. They cover buttons, inputs, switches, and carets. |
| Nouns used as verbs | We calendar'd a fix for Q3. | We scheduled a fix for Q3. |
| Note-style fragments | New setting `lineHeight` (1.2 to 1.8). | We added a `lineHeight` setting, which ranges from 1.2 to 1.8. |

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

The rewrite keeps every identifier, number, and caveat. It makes these changes:

- It restores the `that` and `so that` cues that the original dropped.
- It unpacks noun stacks such as "queue worker health check endpoint".
- It replaces "remembers" and "doesn't know" with literal verbs.
- It moves the long parenthetical out from between the subject and its verb.
- It turns the fragment about the new flag into a sentence.

The penalty from `evals/score.py` drops from 12.74 to 1.27 per 100 words, and the text grows by 40 words.

## Installation

### Universal (`npx skills`)

This command works with Claude Code, Codex, Cursor, Antigravity, OpenCode, Windsurf, and other tools that support `agentskills.io`:

```bash
npx skills add lunchb0ne/human-writing --global
```

To install the skill for only some agents, name them:

```bash
npx skills add lunchb0ne/human-writing --global --agent claude-code cursor codex
```

### Claude Code Plugin Marketplace

```text
/plugin marketplace add lunchb0ne/human-writing
/plugin install human-writing@human-writing
```

### Manual / Symlink (Antigravity, Claude Code, Codex)

Clone the repository, then link the skill folder into each agent's skills directory:

```bash
git clone https://github.com/lunchb0ne/human-writing.git
ln -s "$PWD/human-writing/skills/human-writing" ~/.gemini/config/skills/human-writing
ln -s "$PWD/human-writing/skills/human-writing" ~/.claude/skills/human-writing
```

## Measuring and Hillclimbing the Skill

[`evals/hillclimb.md`](./evals/hillclimb.md) describes the loop that we use to optimize the skill, which is modeled on `autoresearch`. [`evals/rubric.md`](./evals/rubric.md) holds the rubric for blind A/B judging.

Use `mise` to set up Python 3.12, `uv`, and a `spaCy` environment with the `en_core_web_sm` model in `.venv`:

```bash
mise install
mise run sync
mise run test
mise run score-dev
mise run score-skill
```

To score a single file, or to check that a batch of rewrites keeps every required fact and stays within the length limits, run:

```bash
mise run score -- --text-file README.md
mise run score -- --corpus evals/corpus.jsonl --split dev --outputs evals/runs/iter-00.jsonl --strict
```

Without `mise`, use `uv run python evals/score.py ...` directly.

## License

[MIT](./LICENSE)
