# Research Summary: Why AI Text Is Hard to Read

Based on Thomas Hikaru Clark, Matias B. Martin, and Kyle Mahowald (2026), *Why is AI-generated language so hard to understand?* (`arXiv:2610.29162v1`).

## What the paper claims, and what it does not

The paper tests two hypotheses. The first is that frontier models overuse linguistic features that earlier psycholinguistic studies linked to reading difficulty. The second is that a pressure toward dense, short output during post-training causes this drift.

The paper does not run a reading-time, eye-tracking, or comprehension study. The link between each feature and reader difficulty comes from the earlier work that it cites. The paper also makes no editing recommendations. Its remedies are about training: rewarding models for communicating well, regularizing them against drift, and using uniform information density as a training signal.

## Background

Two separate ideas from psycholinguistics motivate the paper. First, readers process text word by word with limited, distance-sensitive working memory, so human writing tends to keep related words close together. Second, the uniform information density (UID) hypothesis says that writers spread information evenly. The paper presents UID as one possible pressure on human writing, not the only one.

The paper's hypothesis is that post-training for code, math, and tasks with verifiable rewards, under limited context and token budgets, pushes models toward shorter forms that carry the same meaning. It supports this hypothesis with the experiments below and states that the cause is speculative.

"Compression" in this paper means choosing the shorter of two forms with the same meaning, such as dropping an optional `that`. It does not mean leaving out content. The paper notes that human-feedback training is known to reward longer outputs, so model text can be long overall and still compressed phrase by phrase.

## Experiment 1: Corpus evidence across 14 models

- **Setup.** The authors collected text from 14 models: frontier and near-frontier models, plus Llama 3.1 8B and Olmo 3 7B variants. The text came from multi-turn chat (10 topics × 12 turns), coding sessions (5 Python repositories × 11 episodes, frontier models only), and PERSUADE 2.0 essays (7 prompts × 10 essays). Olmo Base wrote only essays.
- **Human baselines.** Genre-matched human text: film subtitles from OpenSubtitles for chat, StackExchange for coding, and top-scoring student essays, plus Wikipedia. Inanimate subjects and denominal verbs were not scored on the human chat and coding text, so the human comparison for those two features rests mainly on essays.
- **Meaning-controlled baseline.** Each model sentence was translated into Japanese and back with NLLB-200 3.3B, which keeps the meaning and varies the wording. A Russian pivot and TranslateGemma 4B served as checks. A feature that drops after the round trip is one that the model chose over an available alternative.
- **Findings against human text.** All nine frontier and near-frontier models used more inanimate subjects with animate verbs and more low-frequency n-grams. Most also used longer dependencies, more stacked nouns, and more object relative clauses without `that` in conversation.
- **Findings against round-trip paraphrases.** Frontier models overused rare n-grams, denominal verbs, inanimate subjects, and object relatives without `that`, and they underused object relatives that kept `that`. Stacked nouns and dependency length followed this pattern in chat and coding, but not in essays.
- **Setting.** The effects were smaller in single-turn essays than in multi-turn chat and coding. The authors *hypothesize* that the single prompt explains this. They do not test it.
- **Model families.** Llama and the Olmo Base and Instruct models changed least. Olmo Think patterned with the frontier models, and within Olmo the n-gram effects grew from Base to Instruct to Think.
- **Model versions.** Claude Opus 5.5 scored lower than Opus 5 on 19 of 21 difficulty-linked comparisons, and 8 of those had non-overlapping 95% intervals. The paper says that it is possible to reward models for communicating well. It does not say what changed between the two models.

## Experiment 2: A length penalty as a causal test

- **Setup.** The authors fine-tuned `Qwen2.5-1.5B-Instruct` with GRPO to turn a JSON event into one English sentence. Each item allowed two forms of a syntactic alternation with the same meaning and different lengths. The trained alternations were the dative, the object relative (`the book (that) the professor wrote`), the complement clause (`knew (that) the answer was wrong`), and a particle-shift control in which both forms had the same length. The reward was correctness minus a per-token length penalty, with and without KL regularization, over three seeds.
- **Results.**
  - A length penalty alone moved the model toward the shorter form, even though both forms earned the same correctness reward.
  - Without KL regularization, every positive length penalty produced over 98% short forms on both trained `that` alternations. With KL regularization, the shift was gradual.
  - With no length penalty and no KL regularization, seeds ranged from 0% to 100%, so there was no stable preference.
  - The preference transferred to untrained `so (that)` and `sure (that)`. Of the far-transfer alternations, only the genitive (`the house's roof` over `the roof of the house`) shifted, and only without KL regularization. The passive and purpose clauses did not shift.
- **Context.** Humans use both forms and choose by context. They keep an optional `that` more often when the words after it are hard to predict (Jaeger 2010, cited by the paper). The trained model lost that sensitivity. This is a proof of concept on one small model and single sentences.

## The features measured

| Feature | Why earlier work links it to reading difficulty |
|---|---|
| Low-frequency n-grams | Unpredictable word combinations slow word-by-word reading. |
| Long dependency length | Separating related words, such as a subject and its verb, strains working memory. |
| Object relative clauses without `that` | Object relatives are harder than subject relatives in general (Staub 2010). Dropping `that` removes an optional word. The paper also predicted that models would use more object relatives overall, in place of longer passives. |
| Stacked noun compounds (3+ nouns) | Noun chains leave it unclear which noun modifies which. |
| Denominal verbs | Nouns used as verbs force the reader to reanalyze the word. The measure counts ordinary verbs such as *cushions* and *mirrors* as well as coinages. |
| Inanimate subjects with animate verbs | A verb that needs a living subject, used with an object, can surprise the reader. The paper notes that rephrasing often makes the sentence longer. |

## How this skill uses the paper

The skill's rules are this repository's own inferences from the paper and from the reading studies summarized in `docs/related-work.md` in the source repository. In particular, the advice to restore `that` only where a reader could misread the sentence, rather than everywhere, follows from Jaeger (2010) and from reading studies of verb bias; the paper itself does not give it.
