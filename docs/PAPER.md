# Structural Constraints in the Indus Sign System: A Reproducible Computational Investigation

Research draft, version 0.1 | 15 October 2026 | Not peer reviewed

Prepared with Codex for the IndusValleyScript research repository. This draft reports executed exploratory analyses. It is not a claim of decipherment or a human author's approved publication.

## Abstract

We investigate whether public Indus transcription data support reproducible constraints useful for eventual decipherment. A pinned ICIT-derived export supplies 5,679 records, reduced to 2,156 distinct complete single-line sign sequences, 9,221 tokens, and 637 observed sign IDs. We also audit a separate annotated CISI subset and index 715 verified glyph-reference files. Methods include entropy permutation controls, held-out n-gram models, positional templates, distributional embeddings, adjacency candidates, cross-site transfer, a morphology-based tally/fish test, and substitution invariance. Bigram models average 5.452 bits/token versus 6.450 for unigrams across five splits. Three permutation tests yield lower-tail Monte Carlo p=0.005. These results establish constraints relative to specified baselines, without identifying a language family, phonetic values, or translations. The work provides a falsifiable foundation and identifies data and external anchors needed for further progress.

## 1. Research question and prior work

The objective is to recover constraints that might assist decipherment while avoiding circular assignment of meanings. Previous n-gram research found directional and positional regularities and proposed missing-sign prediction [1]. Entropy comparisons argued for linguistic structure [2], while Sproat showed that structured nonlinguistic alternatives undermine simple classification by entropy [3]. Rao and colleagues subsequently framed their evidence as cumulative rather than conclusive [4]. Network approaches motivate sign-context analysis [5].

Semantic proposals require a separate evidential layer. Parpola's fish/star rebus program motivates a test of combinations but does not supply independently established values for this dataset [6]. Ration and transaction interpretations offer alternatives [7]. Image recognition can improve transcription without solving meaning [8]. A recent synthetic-baseline preprint motivates multiple controls and sensitivity audits, but its results are not treated as an independent validation of ours [9]. This project does not reproduce all experiments in those works.

## 2. Materials, provenance and representation

The main source is the public field-cady ICIT-derived CSV, pinned at commit 30308260d8da50151a79185c9e98404db9da331a. Its upstream attribution passes through Yajnadevam's Lipi repository; individual transcriptions have not been checked against seal photographs. Proposed Sanskrit strings, translations, interpretive classes, and notes are excluded using an explicit whitelist. Excluding these fields avoids direct label contamination but does not remove possible upstream transcription biases.

Eligibility requires a closed string of three-digit tokens delimited by plus signs, without unknown/separator IDs 000 or 999. Damaged or open-boundary strings and multiple lines are excluded. There are 3,591 eligible rows; exact sequence deduplication leaves 2,156. The mean length is 4.277, median 4, and maximum 13. This filter is conservative, not a guarantee of undamaged originals: unmarked uncertainties may remain.

The separate mayig CISI transcription is pinned at ad2f1e218a34b8c33c57de0d6cb8d99272765bbb. It contains 179 annotated Mohenjo-daro sides. Requiring zero annotated damage/uncertainty and a single line, then deduplicating, leaves 91 sequences with 451 tokens and 133 Parpola IDs. The description catalogue contains 395 non-damage entries with attributed cross-references and feature schemas. This is a selected subset, not a civilization-wide sample.

The explorer image directory at commit 8dc5837469bc6694c05f9b310eee90b08399df9e contains 715 reference glyph files. Its numeric index omits nine files and lists nine non-placeholder IDs without files. Tree-based verification recovers every observed non-placeholder ID in the main export. References are linked, not redistributed; file existence does not establish accurate glyph-to-sign mapping or photographic coverage of every artifact.

Dense integers are assigned independently by namespace, reserving PAD, UNK, BOS, and EOS. Integer distance has no linguistic meaning. ICIT strings retain stored order; metadata does not establish whether that order is already normalized. Initial/final labels therefore denote stored positions. CISI strings are reversed according to the source's explicit sealing transcription convention. Different catalogues are not merged by matching numbers.

## 3. Methods and validation design

### 3.1 Descriptive statistics and permutation tests

We count unigram types, tokens, lengths, hapax signs, and subsequences repeated across distinct texts. Adjacent conditional entropy is the empirical estimate H(Y|X) = -sum p(x,y) log2 p(y|x), excluding boundary tokens and never joining separate inscriptions. This sparse plug-in estimate is downward biased; it is used comparatively within matched corpus conditions, not as an absolute entropy rate.

Three controls use 199 seeded permutations each: shuffle within each text, shuffle all tokens while retaining lengths, and shuffle columns among texts of exactly equal length. The last preserves exact position/length marginals while destroying adjacency. Lower-tail p-values use (1 + number of null values at or below observed)/(trials + 1), with resolution 0.005. These are exploratory tests; applying Bonferroni to these three tests gives adjusted p=0.015. Neither result is a posterior probability of language.

### 3.2 Held-out predictive models

Exact sequences and their reversals share a split group. Five fixed seeds (42-46) allocate approximately 80/10/10 percent of groups to training, validation, and test. Unigrams use additive 0.5 smoothing. Bigram and trigram distributions interpolate context counts with a lower-order prior using strengths 1, 5, 20, or 100, selected on validation loss. Models are not refitted on test data. The principal score includes each inscription's EOS prediction.

Unseen sign IDs are mapped to a single UNK event for likelihood scoring. This is a closed-vocabulary-plus-UNK task; its perplexity does not measure correct identification of each previously unseen sign. First-choice and top-five masked prediction, in contrast, require the actual sign to be in the training inventory. Their denominator includes all test positions. Each target is hidden and candidates ranked by P(candidate|left) times P(right|candidate), with boundary symbols at edges. The mask baseline chooses the most frequent actual training sign, excluding EOS. This is synthetic masking of known transcriptions, not validated restoration of damaged originals.

Paired bootstrap intervals resample test inscription groups 500 times for unigram-to-bigram loss differences. They describe uncertainty conditional on this corpus and split, not uncertainty in archaeological transcription. Cross-site transfer removes any training sequence, including its reverse, attested at the target site. Strength 20 is fixed without target-site tuning. An independent positional-slot predictor provides an additional sign-only comparison with supplied text length and EOS removed.

### 3.3 Representations, grammar and morphology

Training-only directional contexts produce positive pointwise mutual information (PPMI) vectors, with 32-dimensional deterministic signed projections for numerical use. Exact sparse-vector cosine similarity yields candidate neighbours among signs observed at least five times. Similarity is evidence of contextual resemblance, not semantic equivalence or allography.

Operational initial, medial, final, singleton, flexible, and rare classes use training counts: a dominant position must cover at least 65 percent of at least ten occurrences. Role sequences observed in training form a finite template grammar. Coverage is evaluated on unused sequences and one shuffled comparison. Templates cannot establish syntactic categories such as noun or verb. Train-only adjacency candidates require five occurrences and PMI of at least one bit; they are collocations rather than validated words. A directed transition graph reports supported adjacency, without semantic labels.

The CISI morphology experiment uses conservative catalogue sets: fish P048-P065 and simple stroke groups P121-P130, P144, P145, P147, P150, P151. We count tally-before-fish in the source-supported reading order and compare to 499 within-text permutations. These sets were refined after an initial description search included complex signs; the result is exploratory, not preregistered. Stroke groups are not assigned actual numerical values.

## 4. Results

### 4.1 Sequence constraints

Observed conditional entropy is 3.892 bits. Every sampled null entropy exceeds it. The length-position control makes fixed position alone an insufficient explanation under this permutation design. Artifact class, sites, allographs, related molds, and other latent factors may still explain part of the remaining dependence.

| Control | Mean bits | SD bits | Lower-tail p |
|---|---|---|---|
| within text | 4.593 | 0.018 | 0.005 |
| global frequency | 4.757 | 0.015 | 0.005 |
| length position | 4.958 | 0.011 | 0.005 |

Across five splits, bigrams improve prediction by 0.898-1.107 bits/token over unigrams. Each paired bootstrap interval excludes zero. Trigrams average 5.453 bits/token and do not consistently improve over bigrams; we therefore find no robust predictive gain from this tested extra context. The splits overlap, so their five scores are not five independent discoveries.

| Seed | Unigram bits | Bigram bits | Trigram bits | Mask top 1 | Mask top 5 |
|---|---|---|---|---|---|
| 42 | 6.442 | 5.461 | 5.461 | 35.5% | 55.0% |
| 43 | 6.520 | 5.413 | 5.423 | 32.1% | 56.8% |
| 44 | 6.394 | 5.496 | 5.484 | 29.0% | 52.1% |
| 45 | 6.416 | 5.419 | 5.440 | 32.7% | 57.5% |
| 46 | 6.476 | 5.469 | 5.457 | 31.9% | 55.8% |

Most-frequent-sign mask baselines range from 9.4 to 11.4 percent. For seed 42, the bigram improvement is 0.980 bits/token, with bootstrap interval [0.813, 1.163]. Reversing all sequences preserves substantial predictive gains, so statistical direction preference alone does not settle reading direction.

### 4.2 Controls and generalization

On the seed-42 sign-only task, unigram, independent slot, and bigram losses are 7.085, 6.829, and 6.111 bits/sign respectively. Because the slot model knows length and scores only signs, these values should not be compared directly to the EOS-inclusive table. The slot model explains some predictability, while the tested bigram explains more.

Holding out Harappa, the unigram score is 6.463 and bigram score 5.665 bits/token on 757 distinct sequences. Holding out Mohenjo-daro, the unigram score is 6.553 and bigram score 5.646 bits/token on 1105 distinct sequences. Transfer does not establish universal grammar, since cataloguing conventions and shared artifact practices may also travel between sites.

A synthetic administrative slot generator, fitted to training-only positional distributions and supplied the observed lengths, yields conditional entropy 5.109 bits versus 3.892 observed. It fails to match adjacency and long repeats in this run. This rejects neither administration nor semasiography generally: the generator intentionally lacks local dependency, and synthetic duplicate records are retained for the descriptive comparison.

### 4.3 Candidate grammar, collocations and morphology

The seed-42 empirical role grammar covers 66.8 percent of held-out sequences, versus 32.3 percent of a single within-text shuffle. Coarse rare/flexible classes allow substantial coverage; this is not grammatical validation. There are 163 train-selected adjacency candidates, and 47 distinct five-sign subsequences recur across distinct complete texts. Such units could be names, formulae, codes, or other combinations.

In the clean CISI subset, 17 simple-stroke-before-fish adjacencies occur, versus mean 5.902 under the shuffle control, with upper-tail p=0.002. This is compatible with constrained number-like/fish combinations. It cannot distinguish fish as stars, commodities, identity markers, or components of words. No sound value or translation follows from this test.

### 4.4 A negative result for unconstrained substitution

Ten different bijective assignments of abstract syllable labels preserve conditional entropy exactly, to numerical precision. For 637 distinct labels there are 637! possible bijections, about 10^1511.4. This is a label-invariance demonstration, not a count of historically viable languages. It establishes that frequency and adjacency statistics alone cannot select the actual label meanings. A configured numerical grammar is achievable; recovery of the historical spoken language requires additional constraints.

## 5. Limitations and implications for decipherment

The main dataset is a secondary public export. No new glyph transcription, full catalogue reconciliation, artifact-family grouping, or independent translation anchor has been established. Splitting reverse/exact copies does not eliminate all near-duplicate or formula leakage. Allograph distinctions may inflate the vocabulary and hapax rate (36.1 percent in the main subset). The complete-only filter selects against difficult inscriptions and may bias inference. Rare sign embeddings and small CISI morphology counts are unstable.

The models establish conditional predictability under declared controls. They cannot determine whether that structure encodes phonology, names, quantities, transactions, or a mixture. Fitting an unconstrained rebus or a surname list would risk selecting the desired answer through researcher flexibility. No Proto-Dravidian, Indo-Aryan, Austroasiatic, or isolate mapping has been tested on historically matched, independently held-out language corpora in this release.

The next useful steps are independent photo verification, allograph sensitivity, family-aware splitting, contextual prediction by object class, and constrained comparison with appropriately licensed historical corpora. A decipherment claim should require fixed values that translate unseen material and predict independent archaeological or bilingual observations. Exhaustive acquisition and genuine decipherment remain open objectives.

## 6. Reproducibility and research disclosure

All reported experiments were executed locally. Scripts use Python's standard library for acquisition and analysis; ReportLab is optional for PDF export. Source revisions, hashes, filtering decisions, split groups, sampled null entropies, learned vectors, and test outputs are committed. Run scripts/acquire.py, normalize.py, test_pipeline.py, analyze.py, extended.py, catalogue.py, and report.py in that order. The methods ledger distinguishes executed, revised, and pending work. The PDF is generated from this Markdown source.

Codex drafted code, literature notes, and text and executed the analyses. No specialist epigrapher has reviewed the transcription choices or semantic interpretation. This paper is an evolving research artifact, not a journal submission. Code and data: https://github.com/farzeenilyaszargar/IndusValleyScript

## References

[1] Yadav et al. Statistical analysis of the Indus script using n-grams. 2009 preprint, related 2010 PLOS ONE article. https://arxiv.org/abs/0901.3017

[2] Rao et al. Entropic evidence for linguistic structure in the Indus script. Science 324, 1165, 2009. https://pubmed.ncbi.nlm.nih.gov/19389998/

[3] Sproat. Ancient Symbols, Computational Linguistics, and the Reviewing Practices of the General Science Journals. Computational Linguistics 36(3), 2010. https://aclanthology.org/J10-3012/

[4] Rao et al. Entropy, the Indus Script, and Language: A Reply to R. Sproat. Computational Linguistics 36(4), 2010. https://aclanthology.org/J10-4016/

[5] Sinha et al. Network analysis of a corpus of undeciphered Indus civilization inscriptions indicates syntactic organization. 2010 preprint; Computer Speech and Language 25, 2011. https://arxiv.org/abs/1005.4997

[6] Parpola. 'Hind Leg' + 'Fish': Towards Further Understanding of the Indus Script. Scripta 1, 2009. https://www.harappa.com/content/hind-leg-fish-towards-further-understanding-indus-script

[7] Rao. The Indus Script and Economics. 2018. https://arxiv.org/abs/1812.00049

[8] Palaniappan and Adhikari. Deep Learning the Indus Script. 2017 preprint. https://arxiv.org/abs/1702.00523

[9] Nair. How Non-Linguistic Is the Indus Sign System? A Synthetic-Baseline Scorecard. 2026 preprint. https://arxiv.org/abs/2604.17828
