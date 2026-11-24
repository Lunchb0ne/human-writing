# Research Summary: Why AI Text Is Hard to Read

Based on Thomas Hikaru Clark, Matias B. Martin, and Kyle Mahowald (2026), *Why is AI-generated language so hard to understand?* (`arXiv:2610.29162v1`).

## Core Thesis

Human language balances production effort against listener comprehension. Readers process text incrementally with lossy, distance-sensitive working memory, so natural human writing favors **Uniform Information Density (UID)**: spreading information evenly across clauses, keeping cue words (`that`), and keeping syntactic dependencies short.

Modern LLMs undergo extensive post-training for math, coding, and verifiable-reward tasks (RLVR) under finite context and token budgets. Because correctness rewards do not explicitly reward human ease of parsing, models converge on **information compression**, packing the same meaning into fewer tokens using constructions that trigger backtracking and working-memory strain in humans.

## Experiment 1: Corpus Evidence Across 14 Models

- **Setup:** Evaluated 14 models (frontier closed/open models plus Llama and Olmo variants) across multi-turn chat (10 seeds x 12 turns), sandbox coding sessions (5 repos x 11 turns), and PERSUADE 2.0 essays (7 prompts).
- **Baselines:** Genre-matched human corpora (OpenSubtitles for chat, StackExchange for coding, student essays for PERSUADE, plus Wikipedia) and a meaning-controlled parallel corpus built via **round-trip translation** (English to Japanese and back with NLLB-200 3.3B, checked against Russian and TranslateGemma 4B).
- **Findings:**
  - Relative to human baselines, all nine frontier and near-frontier models used more **inanimate subjects with animate verbs** and more **low-frequency n-grams** (unattested bigrams and higher trigram perplexity).
  - Relative to round-trip paraphrases, frontier models overused rare n-grams, **denominal verbs**, inanimate subjects, and **reduced object relative clauses** (omitting `that`/`which`), while underusing object relative clauses that kept the relativizer.
  - Within Olmo, these difficulty-linked features increased monotonically from `Base` to `Instruct` to `Think`, with `Olmo Think` matching frontier models.
  - Multi-turn chat and coding amplified dependency length and stacked nouns more than single-turn essays.
  - Alignment can reverse the drift: Claude Opus 5.5 scored lower than Opus 5 on 19 of 21 difficulty-linked comparisons.

## Experiment 2: Causal Mechanism via RL Length Penalty

- **Setup:** Fine-tuned `Qwen2.5-1.5B-Instruct` with GRPO to convert structured JSON events into English sentences where each test case allowed two semantically equivalent syntactic alternations differing in token length (for example, `knew the answer was wrong` vs. `knew that the answer was wrong`).
- **Results:**
  - Adding a per-token length penalty shifted models toward the shorter variant even though both variants earned equal correctness reward.
  - Without KL regularization, models collapsed to over 98% short-variant usage on trained `that` alternations at every positive length penalty.
  - The compression habit generalized to untrained alternations: near transfer (`so (that)`, `sure (that)`) shifted consistently, and far transfer appeared on genitives without KL regularization.

## The Six Features Measured

| Feature | Why it hurts comprehension |
|---|---|
| Low-frequency n-grams | High-surprisal word combinations slow incremental reading and prediction. |
| Long dependency length | Separating heads from dependents (for example, subject from verb) overloads working memory. |
| Reduced object relative clauses | Dropping optional `that` removes an early structural cue and triggers garden-path re-parses. |
| Stacked noun compounds (3+ nouns) | Noun chains create temporary bracketing ambiguity about which noun modifies which. |
| Ad-hoc denominal verbs | Converting nouns into verbs forces part-of-speech reanalysis. |
| Inanimate subjects with animate verbs | Violating animacy selectional restrictions causes semantic reanalysis (P600-style surprises). |
