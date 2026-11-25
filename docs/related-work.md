# Related Work: What the Evidence Says About Editing for Readers

This note reviews Clark, Martin, and Mahowald (2026) in full, checks the summary in [research.md](../skills/human-writing/references/research.md) against it, and adds related papers that bear on the editing rules in [SKILL.md](../skills/human-writing/SKILL.md). It was compiled on 2026-11-25.

## How to read this note

Each source below states how much of it was read. "Full text" means that the methods, results, discussion, and limitations were read. "Abstract only" means that the full text was not available here, so only the abstract or a published excerpt was read, and the note says so wherever that source is used.

Each claim also carries an evidence label:

- **Model-text experiment**: an experiment or controlled comparison that uses model output directly.
- **Human reading experiment**: people read controlled versions of a text, and their comprehension, recall, or reading time was measured.
- **Correlational**: a corpus comparison or an observational association, with no manipulation of the text that readers saw.
- **Expert guidance**: a recommendation that is not backed by an experiment in the sources read here.

---

## Part 1. Clark, Martin, and Mahowald (2026), read in full

**Source.** Thomas Hikaru Clark, Matias B. Martin, and Kyle Mahowald. 2026. *Why is AI-generated language so hard to understand?* arXiv:2610.29162v1. <https://arxiv.org/abs/2610.29162>

**What was read.** The full arXiv HTML text was read, including the abstract, Sections 1 to 7, and Appendices A to D. The HTML build did not render the figures, and no PDF renderer was available, so the numeric values in Figures 2 to 10 were not read. Every claim below comes from the text, the figure captions, or Tables 1 to 5.

### What the paper does

The paper tests two hypotheses (Section 1):

- **H1.** Frontier and near-frontier models overuse linguistic features that are associated with comprehension difficulty in humans.
- **H2.** A pressure for information density during post-training shifts model language away from human patterns.

**Experiment 1 (Section 3, Appendix A and B).** The authors collected text from 14 models: four Claude models, three GPT-5.6 models, GLM 5, Kimi K2.5, and five small open models (Llama 3.1 8B base and Instruct, and Olmo 3 7B base, Instruct, and Think). The text came from three settings:

- Chat: 10 topics, 12 turns each, with a simulated user played by Claude Sonnet 4.6. This produced 1,428 replies.
- Coding: 5 real Python repositories, 11 episodes each, run only on the nine frontier models.
- Essays: 10 essays for each of 7 PERSUADE 2.0 prompts, written by every model. This produced 980 essays.

The paper measures eight quantities that group into six features: unattested bigrams, trigram perplexity, standardized dependency length, object relative clauses with and without a relativizer, stacked noun compounds (three or more nouns), denominal verbs, and inanimate subjects of animate verbs. Denominal verbs and inanimate subjects are first proposed by the spaCy parse and then accepted or rejected by an external classifier (Appendix B.1).

The text is compared with two references. The first is a genre-matched human corpus: OpenSubtitles for chat, StackExchange for coding, and top-scoring student essays (scores of 5 or 6, grades 6 to 12) for essays, plus Wikipedia. The second is a round-trip translation of each model sentence through Japanese and back with NLLB-200 3.3B. This holds the meaning fixed while the wording changes, so a feature that drops after the round trip is one the model chose over an available alternative (Section 3.4). The round trip was repeated with a Russian pivot and with TranslateGemma 4B as a check (Appendix B.5).

**Experiment 2 (Section 4, Appendix C).** The authors fine-tuned Qwen2.5-1.5B-Instruct with GRPO on a task that turns a JSON event into one English sentence. Each item can be written with either member of a syntactic alternation. The trained alternations are the dative, the object relative (`the book (that) the professor wrote`), the complement clause (`knew (that) the answer was wrong`), and a particle-shift control in which both orders have the same length (Table 3). The reward is correctness times a format check, minus a per-token length penalty λ of 0, 0.01, 0.03, or 0.1, with a KL coefficient β of 0 or 0.04, over three seeds (Table 4, Equation 3).

### What the paper finds

1. **Against the round-trip paraphrases, frontier models overuse rare n-grams, denominal verbs, inanimate subjects, and object relatives without `that`, and they underuse object relatives with `that`** (Section 3.5, Figures 4 and 6). This holds across almost all frontier and near-frontier models and all three settings for the n-gram measures. *Model-text experiment (controlled for meaning), but correlational with respect to reader difficulty.*
2. **Stacked nouns and dependency length follow the same pattern in chat and coding, but not in essays.** In essays, dependency length is unchanged or slightly longer after the round trip, and stacked nouns change significantly for only two models (Section 3.5).
3. **Against human text, the abstract claims that all nine frontier and near-frontier models use more inanimate subjects and more low-frequency n-grams, and that most also use longer dependencies, more stacked nouns, and more reduced object relatives in conversation.** Two details limit this claim. Denominal verbs and inanimate subjects were not scored on the human chat and coding corpora (Appendix B.4), and the human chat baseline is film subtitles. So the human comparison for inanimate subjects rests on the essay setting (Figure 3b).
4. **The effects are smaller for single-turn essays than for multi-turn chat and coding** on n-gram measures, dependency length, stacked nouns, and denominal verbs. The authors *hypothesize* that this is because essays involve a single prompt, and they *speculate* that long conversations demand more compression (Section 3.5). They do not test this.
5. **Model families differ.** Llama and the Olmo base and Instruct models change least under the round trip. Olmo Think patterns with the frontier models, and within Olmo the n-gram effects grow from base to Instruct to Think (Section 3.5).
6. **Claude Opus 5.5 is lower than Opus 5 on 19 of 21 difficulty-linked comparisons, with non-overlapping 95% intervals in eight** (Section 3.5). The paper does not say what changed between the two models.
7. **A length penalty alone pushes the model toward the shorter variant, even though both variants earn the same reward** (Section 4.2). Without KL regularization, any positive λ produced a categorical preference: over 98% short variants for both trained `that` alternations. With KL regularization, the shift was gradual. With λ = 0 and no KL, seeds ranged from 0% to 100%, which means there was no stable preference.
8. **The preference transfers partly to untrained constructions.** It transferred consistently to `sure (that)` and `so (that)`. Of the four far-transfer alternations, only the genitive (`the house's roof` over `the roof of the house`) shifted, and only without KL. The passive and the purpose clause (`to` versus `in order to`) did not shift, and `all (of)` was already near ceiling (Appendix C).

### What the paper does not do

- **It does not measure human comprehension.** No reading-time, eye-tracking, or comprehension experiment was run. The link between each feature and reader difficulty comes from earlier psycholinguistic work that the paper cites (Section 3.1). The title asks a question that the paper answers indirectly.
- **It makes no editing recommendations.** The remedies it points to are about training models: rewarding models for effective communication (Section 5), the observation that Opus 5.5 improved on Opus 5, the observation that KL regularization damped the shift (Section 4.2), and uniform information density as a preference-optimization metric, citing Li and Xu (2026) (Section 2). The conclusion asks future work to align model output "with the needs of human comprehenders, in the service of user experience and monitorability" (Section 6).
- **It says nothing about omitting content.** "Compression" in this paper means choosing the shorter of two forms that carry the same meaning, such as dropping `that`. The round-trip design holds content fixed. The paper also notes that human-feedback training is known to reward *longer* outputs (Singhal et al., 2024), which is why it ties compression to verifiable-reward training instead (Section 5). Wordy answers and compressed syntax can therefore occur together.
- **Its stated limitations** are that it covers only some models, only English, and a small number of seeds, and that it uses proxies because it cannot watch frontier models being post-trained (Section 7).

### What the paper suggests for editing, read cautiously

The paper gives no editing advice, but three of its observations bear on an editor:

- Humans keep an optional `that` more often when the words after it are less predictable (Section 4.1, citing Levy and Jaeger 2007 and Jaeger 2010). The trained models lost that sensitivity to context. An editor who restores cue words should therefore restore them where the next words are hard to predict, not everywhere.
- The paper concedes that avoiding inanimate subjects would often lengthen the sentence: "bites" stands in for "causes an issue" (Section 3.1). The edit costs words, and the paper does not show that the edit pays for itself.
- The denominal-verb examples in Table 2 include ordinary verbs such as *cushions*, *mirrors*, *masking*, *filters*, and *staging*, as well as coinages such as *speed-runnable*. The measured feature is broader than ad hoc coinages, so a count of denominal verbs is not a list of words to rewrite.

### Where research.md is wrong, overstated, or incomplete

1. **It never says that the paper ran no human study.** A reader of research.md would assume that the difficulty was measured. It was inferred from prior literature.
2. **It attributes an editing fix to the paper.** The sentence "so the fix is to restore cue words where a reader could misparse, not to add them everywhere" is the summary's own inference. The paper's remedies are all about training (Sections 2, 4.2, 5, and 6).
3. **"Alignment can reverse the drift"** overstates Section 5. The paper reports that Opus 5.5 improved on Opus 5 and says that it is "possible to reward models for effective communication." It does not say that alignment caused the improvement. research.md also omits that only 8 of the 19 comparisons had non-overlapping intervals.
4. **"Within Olmo, these difficulty-linked features increased monotonically from Base to Instruct to Think"** overgeneralizes. The paper states the Base to Instruct to Think growth for the n-gram effects under round-trip translation. Olmo Base produced only essays, so a three-step trend cannot exist in chat.
5. **"Multi-turn chat and coding amplified dependency length and stacked nouns more than single-turn essays"** presents a hypothesis as a finding. The paper observes smaller effects in essays and only hypothesizes that the single prompt is the cause.
6. **The human-baseline finding leaves out its caveats.** Inanimate subjects and denominal verbs were not scored on the human chat and coding corpora. The chat baseline is film subtitles, and the essay baseline is top-scoring school essays. research.md also omits the abstract's second clause: that most models also use longer dependencies, more stacked nouns, and more reduced object relatives than humans in conversation.
7. **The table row for reduced object relatives cites a mechanism that the paper does not give.** research.md says that dropping `that` "triggers garden-path re-parses." The paper cites Staub (2010) for why object relatives are harder than subject relatives *in general* (word order and dependency length). It counts reduced relatives because they skip an optional word. It also predicted that models would overuse object relatives overall because they replace longer passives. research.md drops that prediction.
8. **The table calls the feature "ad-hoc denominal verbs,"** but the measure also counts conventional denominal verbs (Table 2). See the cautious reading above.
9. **"Readers process text incrementally ... so natural human writing favors UID"** merges two separate ideas. Distance-sensitive memory motivates *dependency length minimization*. Uniform information density is about spreading surprisal evenly. The paper presents UID as one "purported pressure" and cites availability-based production as another (Section 2).
10. **"Models converge on information compression"** is stated as fact. The paper states it as a hypothesis, supports it with a 1.5B-parameter proof of concept on single sentences, and explicitly "speculates" about the cause (Sections 4.3 and 5).
11. **Experiment 2 details are missing.** research.md does not list the dative, object-relative, and particle-control alternations; it does not say that the KL-regularized runs also shifted, only more slowly; it does not say that the λ = 0 runs had no stable preference; and it does not say that the passive and purpose-clause alternations did not shift at all.
12. **The note on length and verbosity is missing.** The paper's point that human-feedback training rewards longer output (Section 5) matters for this skill. It means that model prose can be long overall and compressed at the level of the phrase, and the skill should fix the phrase without padding or cutting the whole.

---

## Part 2. Related papers

### A. Reading cost of model text

**Cekini, Biondi, Boldrini, Passarella, and Conti (2026).** *The Cognitive Cost of LLM Writing: A Reading-Time Comparison with Human Text.* arXiv:2610.23715. <https://arxiv.org/abs/2610.23715>. Full text read.

The authors trained a RoBERTa model on human eye-tracking data to predict reading time per word. They then asked GPT-5.6 Terra to rewrite 496 news articles "without adding outside information or omitting substantive content" (Section IV-A). Results (Tables V to VIII):

- The rewrites were 2.66% shorter (496 versus 511 words).
- Predicted reading time *per word* rose by 1.57% (233.4 versus 229.9 ms), so total predicted time fell by only 1.19%.
- Mean word length rose by 6.06%, word frequency fell by 7.61%, and lexical diversity (MTLD) rose by 31.83%. Surprisal fell by 6.51%.
- The more an article was shortened, the more the per-word time rose (Spearman ρ = −0.458). Heavier shortening went with longer, rarer, and more varied words.

The authors conclude that "textual conciseness should not automatically be equated with cognitive ease" (Section V-A). The main limitation is that reading times were *predicted* by a model, not measured on people (Section VI). *Model-text experiment with a predicted human measure; correlational for the length effect.*

**Reinhart et al. (2025).** *Do LLMs write like humans? Variation in grammatical and rhetorical styles.* PNAS 122, e2422455122. arXiv:2410.16107v2. <https://arxiv.org/abs/2410.16107>. Full arXiv text read; the SI tables were not read.

The authors gave models the first 500 words of human texts and compared each continuation with the human second half, using Biber's 66 features. Instruction-tuned models used present participial clauses at 2 to 5 times the human rate (GPT-4o: 5.3 times, d = 1.38), `that` clauses as subjects 2.6 times as often (d = 0.77), nominalizations 2.1 times as often (d = 1.23), and phrasal coordination 1.9 times as often (d = 0.81). GPT-4o used the agentless passive at about half the human rate. Base Llama models were close to human rates, which points to instruction tuning as the cause. The authors call the result "an informationally dense, noun-heavy style." They did not test comprehension. *Correlational.*

### B. Information density in model training

**Singhal, Goyal, Xu, and Durrett (2024).** *A Long Way to Go: Investigating Length Correlations in RLHF.* COLM 2024. arXiv:2310.03716. <https://arxiv.org/abs/2310.03716>. Introduction and main results read.

Reward models learned from human preferences correlate strongly with output length. PPO with a reward based on length alone matched most of the gains of standard PPO (56% versus 58% win rate on WebGPT). This is the paper that Clark et al. cite to separate preference-driven *length* from verifiable-reward *compression*. *Model-training experiment; no reader comprehension measure.*

**Li and Xu (2026).** *Uniform Information Density-Based Preference Optimization.* arXiv:2610.14578. <https://arxiv.org/abs/2610.14578>. Method and Section 4.2 skimmed.

This is the training remedy that Clark et al. cite. It adds a reward for even information spread to SimPO and reports benchmark gains judged by models. Its linguistic check (Section 4.2) asks whether the tuned models' probabilities predict when an optional `that` is useful. It runs no human reading study, so it does not inform editing rules directly. *Model-training experiment.*

### C. Human comprehension of edited and simplified text

**Martínez, Mollica, and Gibson (2022).** *Poor writing, not specialized concepts, drives processing difficulty in legal language.* Cognition 224, 105070. <https://doi.org/10.1016/j.cognition.2022.105070>. Full text read (open access).

The authors wrote 12 contract excerpts in legalese and matched each with a version that kept every proposition but made four changes: rare words became common synonyms, center-embedded clauses became separate sentences, passives became actives, and all-caps text became normal case (Section 3.1.1). 108 native English readers each read six excerpts. Results (Section 3.2):

- Comprehension accuracy was 73.5% for the simple version and 67.7% for legalese (β = −0.179, p < .05).
- Recall of propositions was 42.4% versus 35.3% (β = −0.179, p < .05).
- A replication with the text in view and a bonus for accuracy found the same effect (β = −0.222, p < .05).
- Reading experience did not remove the effect.
- An exploratory analysis found the strongest effect for **center-embedding**, a smaller one for **word frequency**, and **no effect for passive voice or capitalization** (Section 3.2.3). The authors advise prioritizing "unpacking clauses into separate sentences and opting for higher frequency synonyms" (Section 4).

*Human reading experiment, with content held constant.*

**Agrawal and Carpuat (2024).** *Do Text Simplification Systems Preserve Meaning? A Human Evaluation via Reading Comprehension.* TACL 12, 432–448. <https://aclanthology.org/2024.tacl-1.24>. Full arXiv text read (arXiv:2312.10126).

112 native English readers answered multiple-choice questions after reading an original passage, a human simplification, or one of nine automatic simplifications. Each question had an "unanswerable" option. Results (Table 2, Section 5):

- Readers of the original scored 78.3%, and readers of the human Elementary version scored 77.2%. Human simplification cost almost nothing.
- ChatGPT simplifications scored 74.4%. The worst system, which was prone to deletion, scored 20.5%.
- Readers marked 14% to 65% of questions unanswerable for system outputs. The authors identify **over-deletion** as the main cause, because answers that appeared verbatim in the passage were answered correctly 93% of the time.
- One system lost 3 points when it simplified to grade 5 instead of grade 7, because it deleted more.

*Human reading experiment on model text.*

**Guo et al. (2025).** *Are LLM-generated plain language summaries truly understandable? A large-scale crowdsourced evaluation.* arXiv:2505.10409. <https://arxiv.org/abs/2505.10409>. Full text read.

150 lay readers produced 1,346 annotations on summaries of 50 biomedical abstracts. Each abstract had a human-written plain-language summary and GPT-4 summaries made under six prompting strategies. Results (Sections 2.2 to 2.5):

- Readers rated the GPT-4 summaries about as highly as the human ones.
- Readers answered multiple-choice questions significantly better after reading the *human* summaries. Free recall did not differ significantly.
- The human summaries were the shortest of all the versions.
- All five subjective ratings predicted comprehension. Faithfulness predicted it most strongly (β = 0.048), followed by the presence of needed background (definitions and context) and coherence.
- The summary that was prompted to prioritize simplicity was rated the *least* simple.

*Human reading experiment for the human versus model comparison; correlational for the rating predictors.*

**McNamara, Kintsch, Songer, and Kintsch (1996).** *Are Good Texts Always Better? Interactions of Text Coherence, Background Knowledge, and Levels of Understanding in Learning From Text.* Cognition and Instruction 14(1), 1–43. <https://doi.org/10.1207/s1532690xci1401_1>. **Full text not available.** The abstract and published excerpts of the results were read.

In Experiment 1, students learned more from a globally coherent and more explanatory biology text. In Experiment 2, local and global coherence were varied independently. Low-knowledge readers benefited from coherent text and recalled the version with gaps at both levels significantly worse. High-knowledge readers recalled every version well and did better on inference questions after reading the *less* coherent text, which the authors attribute to compensatory processing. *Human reading experiment.*

**Sundararajan and Adesope (2020).** *Keep it Coherent: A Meta-Analysis of the Seductive Details Effect.* Educational Psychology Review 32, 707–734. <https://doi.org/10.1007/s10648-020-09522-4>. **Full text not available; the abstract was read** (via the ERIC record EJ1263249).

The abstract reports that interesting but irrelevant information ("seductive details") hinders learning, with moderators that include delivery format, learner pacing, and question type. A secondary summary gives an overall effect of g = −0.33, but that figure could not be checked against the paper, so it is not relied on here. *Meta-analysis of human learning experiments, read at abstract level only.*

### D. Explanation length and human judgment

**Friedman et al. (2026).** *Not Too Short, Not Too Long: How LLM Response Length Shapes People's Critical Thinking in Error Detection.* IUI MIRAGE 2026 workshop. arXiv:2603.06878. <https://arxiv.org/abs/2603.06878>. Full text read.

24 participants judged model explanations of 42 to 150 words on 15 critical-thinking items (Section 3). When the model was wrong, participants caught the error 54% of the time with medium-length explanations, against 25% for short and 31% for long ones (Section 4). When the model was right, accuracy was high at every length. The sample is small, the lengths were split into data-driven thirds, and length was confounded with reading time (Section 5.1). *Human experiment, weak.*

### E. Foundational psycholinguistics behind the `that` rule

**Garnsey, Pearlmutter, Myers, and Lotocky (1997).** *The Contributions of Verb Bias and Plausibility to the Comprehension of Temporarily Ambiguous Sentences.* Journal of Memory and Language 37(1), 58–93. <https://doi.org/10.1006/jmla.1997.2512>. **Full text not available; the abstract was read.**

Eye-tracking and self-paced reading tested sentences such as *The senator regretted the decision had been made public*, where the noun after the verb could be read as its object. The abstract reports that the verb's usual pattern (whether it usually takes an object or a clause) and the plausibility of the noun as an object both affect reading quickly, and that they interact. It replicates Trueswell, Tanenhaus, and Kello (1993). In other words, a missing `that` costs the most after verbs that usually take a direct object, and when the next noun would make a sensible object. *Human reading experiment, read at abstract level only.*

### Papers found but not used

- A small eye-tracking study (13 participants) on AI-generated and human-authored text in ACM ETRA 2025 (<https://dl.acm.org/doi/10.1145/3715669.3726846>) was found but not read, and it is too small to support a rule.
- A 2026 randomized trial of LLM lay summaries of brain MRI reports on medRxiv was found in search results, but its full text was not read, so it is not used.

---

## Part 3. Does removing secondary detail help, or does it risk losing what readers need?

**Short answer.** Removing material that is irrelevant to the reader's task can help a little, but deleting content that the reader needs does real damage, and shortening text without removing content does not by itself make it easier to read. Most of the measured gains come from restructuring the same content, not from cutting it.

**Evidence that cutting can help.** The seductive-details meta-analysis (Sundararajan and Adesope, 2020; abstract only) reports that interesting but irrelevant material hinders learning. The key word is *irrelevant*: these studies remove material that does not serve the learning goal, not material that is merely secondary.

**Evidence that cutting can hurt.** Agrawal and Carpuat (2024) show that simplifiers which delete content leave readers unable to answer questions. The worst system cut accuracy from 78% to 20%, and even the better systems made 14% or more of questions unanswerable. Guo et al. (2025) found that faithfulness and needed background were the strongest predictors of lay comprehension, and that adding definitions or context helped. McNamara et al. (1996) found that low-knowledge readers need the links that an expert writer leaves out.

**Evidence that shorter is not the same as easier.** Cekini et al. (2026) found that when a model shortened articles while keeping their content, it did so with longer and rarer words, and predicted per-word reading time rose with the amount of shortening. Clark et al. (2026) describe the same trade at the level of syntax: the shorter form of an alternation is the harder one. Friedman et al. (2026) found that neither the shortest nor the longest explanations helped readers catch errors.

**Evidence that restructuring helps.** Martínez et al. (2022) kept every proposition and changed only the form, and recall rose from 35% to 42%. Human simplifiers in Agrawal and Carpuat (2024) kept accuracy level with the original.

**Where to draw the line.**

1. Decide what the reader must do or know after reading. Keep every fact that serves that purpose, including caveats, conditions, and numbers. This is what the comprehension questions in the studies above test.
2. Cut only material that serves no purpose for this reader, such as asides, restated points, and decorative detail. The seductive-details evidence supports this, though only at abstract level here.
3. When you are unsure whether a fact is needed, keep it. Deletion errors are the most damaging failure in the simplification studies, and they are invisible to the reader, who cannot know what is missing.
4. Moving secondary detail later in the text or into a separate section ("layering") is a reasonable way to keep information without blocking the main point. **None of the sources read here tests layering directly**, so this is expert guidance.
5. For a reader new to the topic, adding a short definition or link can help more than cutting (Guo et al., 2025; McNamara et al., 1996). For an expert reader, such additions matter less.

For this skill, which edits text that someone else wrote and has no way to ask the reader what they need, the existing guardrail to keep every fact is well supported. The skill's gains should come from restructuring, not deletion.

---

## Part 4. Editing rules distilled from the evidence

Each rule lists an example, the evidence, and the strength of that evidence.

### Rule 1. Break center-embedded clauses into separate sentences

- **Before:** "The payment, which includes the bonus under Section 3 and which we will call the Total Payment, will be reduced."
- **After:** "The payment will be reduced. It includes the bonus under Section 3. We will call it the Total Payment."
- **Evidence:** Martínez et al. (2022): un-embedding had the strongest effect on recall among the four changes. Clark et al. (2026): models use longer dependencies in chat and coding.
- **Strength:** Human reading experiment (strong), plus a model-text comparison.

### Rule 2. Prefer the common word when it means the same thing

- **Before:** "We remediated the regression and ameliorated latency."
- **After:** "We fixed the regression and reduced latency."
- **Evidence:** Martínez et al. (2022): replacing rare words with common synonyms had the second-largest effect on recall. Cekini et al. (2026): model rewrites use longer and rarer words, and predicted per-word reading time rises with them (ρ = 0.588 for word length, ρ = −0.405 for word frequency). Clark et al. (2026): models overuse rare word pairs.
- **Strength:** Human reading experiment, plus a model-text experiment with predicted reading times. Keep established technical terms that readers would search for by name.

### Rule 3. Keep `that` after a verb that usually takes a direct object when the next noun would make a sensible object

- **Before:** "We found the cache had expired."
- **After:** "We found that the cache had expired."
- **Evidence:** Garnsey et al. (1997, abstract only) and Trueswell et al. (1993, cited there): the cost of a missing `that` depends on the verb's usual pattern and on whether the next noun is a plausible object. Clark et al. (2026): models drop optional `that`, and a length penalty alone produces this. Jaeger (2010, cited by Clark et al.): humans keep `that` when the next words are hard to predict.
- **Strength:** Human reading experiment (for the cost); model-text experiment (for the habit).

### Rule 4. Keep the relativizer in object relative clauses when the clause is long or the head noun is far away

- **Before:** "The checks the migration we ran last week skipped are listed below."
- **After:** "The checks that the migration skipped are listed below. We ran the migration last week."
- **Evidence:** Clark et al. (2026): models overuse reduced object relatives and underuse the full form. Staub (2010, cited by Clark et al. and not read here) shows that object relatives are harder in general. The comprehension benefit of the overt `that` itself is not tested in the sources read here.
- **Strength:** Model-text comparison; the reader benefit is inferred.

### Rule 5. Unpack coined noun chains, and keep familiar compounds

- **Before:** "the build artifact upload step" → **After:** "the step that uploads build artifacts".
- **Evidence:** Clark et al. (2026): models overuse stacked nouns in chat and coding. The reading studies on noun compounds that the paper cites (Staub et al. 2007; Cohen and Staub 2014) were not read here.
- **Strength:** Model-text comparison; the reader cost is inferred from cited work.

### Rule 6. Say what an object actually does instead of giving it a mind

- **Before:** "The docstring promises that dotfiles are skipped."
- **After:** "The docstring says that dotfiles are skipped."
- **Evidence:** Clark et al. (2026): every frontier model overuses inanimate subjects with animate verbs. The authors note that a P600 response "may" follow without context and that rephrasing often lengthens the sentence.
- **Strength:** Model-text comparison; the reader cost is inferred. Prefer edits that cost few words.

### Rule 7. Turn nominalizations and trailing `-ing` clauses into clauses with a subject and a verb when they hide who did what

- **Before:** "Deployment of the fix occurred on Monday, causing a restart."
- **After:** "We deployed the fix on Monday. The deploy caused a restart."
- **Evidence:** Reinhart et al. (2025): instruction-tuned models use nominalizations at 2.1 times and present participial clauses at up to 5.3 times the human rate.
- **Strength:** Correlational. No study read here tests the comprehension effect.

### Rule 8. Do not convert passives to actives for their own sake

- **Example:** Keep "The flag is read at startup" when the actor does not matter. Name the actor only when the reader needs to know who acts.
- **Evidence:** Martínez et al. (2022): passive voice had no measurable effect on recall. Reinhart et al. (2025): models already use the agentless passive *less* than humans.
- **Strength:** Human reading experiment (exploratory analysis).

### Rule 9. Keep every fact that the reader needs, and cut only what serves no purpose for them

- **Before:** "Rollback takes about four minutes, except on the EU cluster, where it takes twelve because of the replication lag."
- **Bad cut:** "Rollback takes about four minutes."
- **Evidence:** Agrawal and Carpuat (2024): deletion is the main reason that readers cannot answer questions after simplification. Guo et al. (2025): faithfulness is the strongest predictor of comprehension.
- **Strength:** Human reading experiment on model text.

### Rule 10. Do not aim for a shorter text; aim for an easier one

- **Example:** "Ensure idempotent reinstalls" is shorter than "Make sure that running the installer twice gives the same result," but it costs the reader more per word.
- **Evidence:** Cekini et al. (2026): shortening came with costlier words, and the more an article was shortened, the more per-word time rose. Clark et al. (2026): the shorter member of an alternation is the harder one. Guo et al. (2025): the best-understood summaries were also the shortest, so length alone predicts nothing.
- **Strength:** Model-text experiment with predicted reading times; human reading experiment for the summaries.

### Rule 11. For readers new to a topic, add the definition or link they lack

- **Before:** "Enable WAL mode."
- **After:** "Enable WAL (write-ahead logging) mode, which lets reads continue while a write is in progress."
- **Evidence:** Guo et al. (2025): needed background was the second-strongest predictor of lay comprehension. McNamara et al. (1996, abstract and excerpts): low-knowledge readers recall less when links are missing, and high-knowledge readers do not need them.
- **Strength:** Correlational (Guo) and human reading experiment (McNamara). Add only what the source implies or states; do not add new claims.

### Rule 12. Give each paragraph one job, and state that job first

- **Evidence:** McNamara et al. (1996), Experiment 1: a globally coherent text produced better learning. No study read here tests topic sentences or paragraph splitting directly.
- **Strength:** Human reading experiment for global coherence; expert guidance for the specific form.

### Rule 13. Put a condition or goal before the action that depends on it

- **Before:** "Set `strict: false` to skip this check."
- **After:** "To skip this check, set `strict: false`."
- **Evidence:** None of the sources read here tests this ordering.
- **Strength:** Expert guidance.

### Comparing these rules with the current SKILL.md

**Rules that SKILL.md already has.**

- Missing cue words (Rules 3 and 4). SKILL.md correctly limits this to places where a reader could take a wrong turn, which matches Garnsey et al. (1997) and Jaeger (2010).
- Stacked nouns, with an exception for familiar terms (Rule 5).
- Objects with minds (Rule 6).
- Long gaps between subject and verb, including trailing `-ing` clauses (Rules 1 and, in part, 7).
- Coined compressions, including denominal verbs (Rules 2 and 5, in part).
- Paragraphs with one job, and conditions before actions (Rules 12 and 13).
- Keep every fact and every relationship (Rule 9).
- Do not make the text longer, simpler, or more formal for its own sake (Rule 10, in part).

**Rules that SKILL.md lacks.**

- **Prefer common words to rare synonyms** (Rule 2). SKILL.md says only "do not swap a familiar word for a longer one," which forbids making things worse but does not ask the editor to fix rare words in the source. This rule has the second-strongest human evidence in this review.
- **Rewrite nominalizations that hide the actor** (Rule 7). SKILL.md covers trailing `-ing` clauses but not nominalizations.
- **Do not convert passives to actives by default** (Rule 8). SKILL.md has no blanket active-voice rule, which is correct, but it could say so, because many style guides recommend it and the evidence does not support it.
- **Add a definition for a novice reader when the source implies it** (Rule 11). SKILL.md lists "a link that the source implies but does not show" as a good addition, but not a definition of a term.
- **Center-embedding as the top priority** (Rule 1). SKILL.md covers it under long gaps, but it does not say that this is the edit with the strongest evidence.

**Current rules that the evidence contradicts or does not support.**

- **"Bad additions are summaries ... and new claims."** The ban on new claims is supported by Agrawal and Carpuat (2024) and Guo et al. (2025). But Guo et al. found that added background (definitions, examples, and context) helped lay readers. If "summaries" is read broadly enough to cover a short definition, this guardrail is too strict for lay audiences.
- **"Most edits end up 10 to 25 percent longer than the source."** No source read here supports a target length in either direction. Cekini et al. (2026) and Guo et al. (2025) both show that length alone does not predict ease. The figure appears to come from this repository's own evals, not from the literature, and it should be presented that way.
- **Inanimate `'s` genitives (`package.json's name`).** Clark et al. (2026) found that a length penalty shifted the genitive toward the `'s` form, but only without KL regularization, and they did not test whether readers find it harder. This rule has no comprehension evidence behind it.
- **Objects with minds, and keep `that` in object relatives.** These are well supported as habits of model text, but the reader cost is inferred from cited work, not measured on model output. They are not contradicted, but their evidence is weaker than the evidence for Rules 1, 2, and 9.
- **Telegraphic fragments.** No source read here tests this rule. It is expert guidance.
- **The paragraph about why model prose is hard to read.** It says that Clark et al. "measured these habits across 14 models." That is accurate. It should not be read to mean that they measured the cost to readers, which they did not.

---

## Sources

- Agrawal, S., and Carpuat, M. (2024). Do Text Simplification Systems Preserve Meaning? A Human Evaluation via Reading Comprehension. *TACL* 12. <https://aclanthology.org/2024.tacl-1.24>
- Cekini, K., Biondi, E., Boldrini, C., Passarella, A., and Conti, M. (2026). The Cognitive Cost of LLM Writing: A Reading-Time Comparison with Human Text. arXiv:2610.23715. <https://arxiv.org/abs/2610.23715>
- Clark, T. H., Martin, M. B., and Mahowald, K. (2026). Why is AI-generated language so hard to understand? arXiv:2610.29162. <https://arxiv.org/abs/2610.29162>
- Friedman, N., et al. (2026). Not Too Short, Not Too Long: How LLM Response Length Shapes People's Critical Thinking in Error Detection. arXiv:2603.06878. <https://arxiv.org/abs/2603.06878>
- Garnsey, S. M., Pearlmutter, N. J., Myers, E., and Lotocky, M. A. (1997). The Contributions of Verb Bias and Plausibility to the Comprehension of Temporarily Ambiguous Sentences. *Journal of Memory and Language* 37(1). <https://doi.org/10.1006/jmla.1997.2512> (abstract only)
- Guo, Y., et al. (2025). Are LLM-generated plain language summaries truly understandable? A large-scale crowdsourced evaluation. arXiv:2505.10409. <https://arxiv.org/abs/2505.10409>
- Li, Y., and Xu, Y. (2026). Uniform Information Density-Based Preference Optimization. arXiv:2610.14578. <https://arxiv.org/abs/2610.14578>
- Martínez, E., Mollica, F., and Gibson, E. (2022). Poor writing, not specialized concepts, drives processing difficulty in legal language. *Cognition* 224, 105070. <https://doi.org/10.1016/j.cognition.2022.105070>
- McNamara, D. S., Kintsch, E., Songer, N. B., and Kintsch, W. (1996). Are Good Texts Always Better? *Cognition and Instruction* 14(1). <https://doi.org/10.1207/s1532690xci1401_1> (abstract and excerpts only)
- Reinhart, A., et al. (2025). Do LLMs write like humans? Variation in grammatical and rhetorical styles. *PNAS* 122, e2422455122. <https://arxiv.org/abs/2410.16107>
- Singhal, P., Goyal, T., Xu, J., and Durrett, G. (2024). A Long Way to Go: Investigating Length Correlations in RLHF. COLM 2024. <https://arxiv.org/abs/2310.03716>
- Sundararajan, N., and Adesope, O. (2020). Keep it Coherent: A Meta-Analysis of the Seductive Details Effect. *Educational Psychology Review* 32. <https://doi.org/10.1007/s10648-020-09522-4> (abstract only)
