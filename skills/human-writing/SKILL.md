---
name: human-writing
description: Write and edit prose so that it is easy for humans to read on a single pass. Use when drafting or revising documentation, READMEs, design notes, PR summaries, emails, or essays for human readers, rather than writing code or machine-readable configs.
license: MIT
metadata:
  author: Abhishek Aryan
  version: "0.1.0"
---

# Human Writing

Write prose that spreads information evenly across clauses instead of packing meaning into fewer tokens.

## When to use

Use this skill whenever you draft or edit text meant for a human reader: documentation, READMEs, design notes, PR descriptions, release notes, emails, Slack updates, or essays.

Skip this skill when writing source code, schemas, SQL, shell commands, test assertions, or verbatim quotes.

## What makes AI writing hard to read

Language models trained for coding, math, and verifiable rewards learn to minimize token count even when a shorter phrasing strains human working memory. People parse sentences word by word from left to right. When you drop cue words, stack nouns, separate a subject from its verb, or pair objects with human verbs, the reader has to stop and re-parse the sentence.

For background from Clark, Martin, and Mahowald (2026), see [the research notes](./references/research.md).

## Six checks for every editing pass

1. Keep optional cue words (`that` and `so that`) when dropping them forces a double-take.
   - Before: "We copied the three settings we needed so it stays clear."
   - After: "We copied the three settings that we needed so that it stays clear."

2. Unpack noun stacks of three or more nouns using prepositions or short relative clauses.
   - Before: "We adjusted the full height line highlight."
   - After: "We adjusted the highlight that covers the full line height."

3. Replace inanimate subjects paired with mental or human verbs using literal verbs or a human subject.
   - Before: "`focusBand` remembers the index, and `block.js` doesn't know about markers."
   - After: "`focusBand` stores the index, and `block.js` ignores the markers."

4. Keep subjects close to their verbs. Move long parentheticals and multi-item lists after the verb, and split overloaded sentences.
   - Before: "Shared controls (buttons, inputs, switches, and carets) live in Sass."
   - After: "Shared controls live as mixins in Sass, covering buttons, inputs, switches, and carets."

5. Avoid ad-hoc noun-to-verb conversions and adjacent noun/verb collisions.
   - Before: "`block.js` blocks edits, and yanks copied the markers."
   - After: "`block.js` prevents edits, and yanking across blocks copied the markers."

6. Replace telegraphic fragments and awkward inanimate `'s` genitives with smooth phrasing.
   - Before: "Changing `package.json`'s name splits storage. New setting `lineHeight` (1.2 to 1.8)."
   - After: "Changing the `name` field in `package.json` splits storage. We added `lineHeight`, which ranges from 1.2 to 1.8."

## Guardrails

- Preserve every code identifier, file path, flag, command, number, URL, and caveat verbatim.
- Preserve every causal link, actor, and prepositional relationship when you unpack nouns or split clauses. Do not invent causal connectors (such as `because`), turn purpose (`to prevent`) into guaranteed effect (`prevents`), drop an actor, or attach parenthetical config to the wrong verb.
- Keep total length close to the source or natural length. Do not add filler, throat-clearing, or repetitive summaries.

## Workflow

1. Draft the content or read the existing text once to verify facts and structure.
2. Run one focused pass checking the six items above, prioritizing sentences with parentheticals, noun chains, or missing `that`/`so that` cues.
3. Read dense sentences from start to finish. If your eye trips halfway through, split the sentence or restore the missing glue word.
