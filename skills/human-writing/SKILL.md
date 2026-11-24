---
name: human-writing
description: Write and edit prose so that it is easy for humans to read on a single pass. Use when drafting or revising documentation, READMEs, design notes, PR summaries, release notes, emails, chat explanations, or essays for human readers, rather than writing code or machine-readable configs.
license: MIT
metadata:
  author: Abhishek Aryan
  version: "0.5.0"
---

# Human Writing

People read once, left to right, holding only a few words in working memory. Write so that each sentence can be understood on that single pass.

## When to use

Use this skill for any prose a person will read: documentation, READMEs, design notes, PR descriptions, release notes, code review comments, emails, chat answers, and essays.

Skip it for source code, schemas, SQL, shell commands, test assertions, and verbatim quotes.

## Why model prose is hard to read

Models trained heavily on code, math, and verifiable rewards learn to save tokens. They drop optional words, pack nouns together, coin short phrases, and give objects human verbs. Each habit saves a word or two and costs the reader a re-read. Clark, Martin, and Mahowald (2026) measured these habits across 14 models; see [the research notes](./references/research.md).

Your job is to spend those few words back where a reader would otherwise stumble. It is not to make the text longer, simpler, or more formal.

## What trips readers

1. **Missing cue words.** Keep `that` after verbs such as *know*, *find*, *show*, *ensure*, and *mean* when the next noun could be misread as the object. Keep `that` or `which` in object relative clauses, and keep `so that` for purpose.
   - Before: "The test confirmed the cache we rebuilt the index for was stale."
   - After: "The test confirmed that the cache that we rebuilt the index for was stale."
   - Humans drop these words when the rest of the sentence is predictable. Restore them where a reader could take a wrong turn, not everywhere.

2. **Stacked nouns.** A chain of three or more nouns that the writer coined on the spot forces the reader to guess which noun modifies which. Unpack those chains with a preposition or a short clause, and keep every word of the original.
   - Before: "the cache invalidation pipeline manager" → After: "the manager for the cache invalidation pipeline"
   - Leave compounds alone when readers of the document already know them as one term, such as "per-tenant LRU cache", "HTTP status code", or "PgBouncer saturation dashboard". Unpacking a familiar term into "the dashboard for PgBouncer saturation" makes it harder to read, not easier.

3. **Objects with minds.** Code, files, and documents do not remember, know, want, expect, promise, decide, refuse, forget, swallow, or bite. Say what actually happens.
   - Before: "`focusBand` remembers the index, and the docstring promises dotfiles are skipped."
   - After: "`focusBand` stores the index, and the docstring says that dotfiles are skipped."

4. **Long gaps between subject and verb.** Do not make the reader hold a subject through a parenthetical, a list, or a long modifier. Move that material after the verb or into its own sentence.
   - Before: "Shared controls (buttons, inputs, switches, and carets) live in Sass."
   - After: "Shared controls live in Sass. They cover buttons, inputs, switches, and carets."
   - The same goes for a trailing "-ing" clause that hides a second event: "the service scaled to 90 pods, queuing 3,600 connections and exceeding the limit" makes the reader work out who queued and who exceeded. Give each event its own subject and verb: "The service scaled to 90 pods. Together they opened 3,600 connections, which exceeded the limit of 2,000."

5. **Coined compressions.** Rewrite nouns used as verbs (`calendar'd`, `footnote it`), noun/verb look-alikes side by side (`` `block.js` blocks ``), invented compounds (`reader-patience budget`), and inanimate `'s` genitives (`package.json's name`). Use the ordinary phrase: "scheduled", "the `name` field in `package.json`".

6. **Telegraphic fragments.** Turn note-style fragments into sentences with a subject and a verb.
   - Before: "New setting `lineHeight` (1.2 to 1.8)."
   - After: "We added a `lineHeight` setting, which ranges from 1.2 to 1.8."

7. **Paragraphs that carry too much.** A reader can hold one topic at a time. Give each paragraph one job, such as what happened, why, what we did, or what we need from you, and start it with a sentence that names that job. When the text asks the reader to do two or more things, put each request on its own line or in a short numbered list with its owner and date. Put a condition or goal before the action that depends on it: "To skip this check, set `strict: false`."

## Guardrails

- **Keep every fact.** Preserve each identifier, path, flag, command, number, URL, and caveat exactly.
- **Keep every relationship.** When you unpack a phrase or split a sentence, keep who does what to what. Do not add a cause (`because`) the source did not state, turn a purpose (`to prevent`) into a promise (`prevents`), drop an actor, or attach a detail to the wrong noun.
- **Spend words only where the reader gains something.** Good additions are a restored cue word, a missing subject or verb, a paragraph break, a list for parallel items, or a link that the source implies but does not show, such as "3,600 connections (90 pods × 40)". Bad additions are summaries, throat-clearing transitions, restated points, and new claims. Most edits end up 10 to 25 percent longer than the source.
- **Leave clear sentences alone.** If a sentence already reads cleanly on one pass, keep it. Do not break good prose into short, choppy sentences, and do not swap a familiar word for a longer one.

## Workflow

1. Read the text once and note every place where you had to slow down or go back.
2. Fix those places with the checks above. Start with the paragraph structure, then fix long sentences, parentheticals, and noun chains.
3. Read the result from start to finish as a newcomer would. If your attention snags anywhere, fix that sentence again.

When drafting from scratch, write the draft first, then run the same pass over it.
