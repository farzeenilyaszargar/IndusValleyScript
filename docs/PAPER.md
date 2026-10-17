# Structural Constraints in the Indus Sign System: A Reproducible Computational Investigation

Research draft, version 0.21 | 18 October 2026 | Not peer reviewed

Prepared with Codex for the IndusValleyScript research repository. This draft reports executed exploratory analyses. It is not a claim of decipherment or a human author's approved publication.

## Abstract

We investigate whether public Indus transcription data support reproducible constraints useful for eventual decipherment. A pinned ICIT-derived export supplies 5,679 records, reduced to 2,156 distinct complete single-line sequences, 9,221 tokens and 637 sign IDs. A separate annotated CISI subset supports morphology and correspondence audits. We index 715 glyph-reference files and acquire 3,916 official Mahadevan records with raw uncertainty/layout metadata and 417 separate sign-list references, supplemented by 641 original graphic forms and two postscript signs. Of 2,742 secondary sequences matching primary base codes, 265 strip doubtful readings and 92 concatenate lines. Methods include entropy controls, held-out sequence models, masked reconstruction, positional/context representations and controlled language/administrative comparisons. Bigrams average 5.452 bits/token versus 6.450 for unigrams across five splits; synthetic two-sign gaps are recovered at top1 in 12.7%. A richer explicitly non-phonetic administrative generator also supports masked prediction and bigram gains. These results establish structural constraints and source-quality limits, without identifying a language family, sound values or translations. Independent semantic and archaeological anchors remain necessary for decipherment.

## 1. Research question and prior work

The objective is to recover constraints that might assist decipherment while avoiding circular assignment of meanings. Previous n-gram research found directional and positional regularities and proposed missing-sign prediction [1]. Entropy comparisons argued for linguistic structure [2], while Sproat showed that structured nonlinguistic alternatives undermine simple classification by entropy [3]. Rao and colleagues subsequently framed their evidence as cumulative rather than conclusive [4]. Network approaches motivate sign-context analysis [5].

Semantic proposals require a separate evidential layer. Parpola's fish/star rebus program motivates a test of combinations but does not supply independently established values for this dataset [6]. Ration and transaction interpretations offer alternatives [7]. Image recognition can improve transcription without solving meaning [8]. A recent synthetic-baseline preprint motivates multiple controls and sensitivity audits, but its results are not treated as an independent validation of ours [9]. This project does not reproduce all experiments in those works.

## 2. Materials, provenance and representation

The main source is the public field-cady ICIT-derived CSV, pinned at commit 30308260d8da50151a79185c9e98404db9da331a. Its upstream attribution passes through Yajnadevam's Lipi repository; individual transcriptions have not been checked against seal photographs. Proposed Sanskrit strings, translations, interpretive classes, and notes are excluded using an explicit whitelist. Excluding these fields avoids direct label contamination but does not remove possible upstream transcription biases.

Eligibility requires a closed string of three-digit tokens delimited by plus signs, without unknown/separator IDs 000 or 999. Damaged or open-boundary strings and multiple lines are excluded. There are 3,591 eligible rows; exact sequence deduplication leaves 2,156. The mean length is 4.277, median 4, and maximum 13. This filter is conservative, not a guarantee of undamaged originals: unmarked uncertainties may remain.

The separate mayig CISI transcription is pinned at ad2f1e218a34b8c33c57de0d6cb8d99272765bbb. It contains 179 annotated Mohenjo-daro sides. Requiring zero annotated damage/uncertainty and a single line, then deduplicating, leaves 91 sequences with 451 tokens and 133 Parpola IDs. The description catalogue contains 395 non-damage entries with attributed cross-references and feature schemas. This is a selected subset, not a civilization-wide sample.

The explorer image directory at commit 8dc5837469bc6694c05f9b310eee90b08399df9e contains 715 reference glyph files. Its numeric index omits nine files and lists nine non-placeholder IDs without files. Tree-based verification recovers every observed non-placeholder ID in the main export. References are linked, not redistributed; file existence does not establish accurate glyph-to-sign mapping or photographic coverage of every artifact.

Dense integers are assigned independently by namespace, reserving PAD, UNK, BOS, and EOS. Integer distance has no linguistic meaning. ICIT strings retain stored order; metadata does not establish whether that order is already normalized. Initial/final labels therefore denote stored positions. CISI strings are reversed according to the source's explicit sealing transcription convention. Different catalogues are not merged by matching numbers.

For representation-sensitivity comparison we acquired pinned candidate Classical Tamil verses (Akananuru and Purananuru) and UD Vedic Sanskrit word-form data. Acquisition hashes and coverage are recorded in docs/language_resource_inventory.json; raw files remain outside tracked artifacts. The Tamil repository declares Apache 2.0 and the Vedic treebank CC BY-SA 4.0. Opaque derived numeric samples with attributed licenses are packaged for offline metric reproduction. Missing Akananuru edition links and differences between Sanskrit README counts and actual snapshot counts are documented. These later literary proxies have not been phonetically aligned to Indus signs. Corpus availability does not establish chronology, linguistic descent, or comparability of written units.

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

### 3.4 Hidden-state grammar and near-copy extension

The extension design was committed before execution in docs/EXPERIMENT_002.md, after prior exploration of the same corpus. We fit generative hidden Markov models with 2, 4, or 8 hidden states, initialization seeds 17 and 29, and 5/10/20-iteration EM checkpoints. Eighteen configurations are selected by seed-42 validation loss only. Emissions use a training-unigram prior with strength 5; start and transition/stop events receive pseudo-count 0.5. Explicit per-state stop probabilities give a variable-length likelihood. The denominator is signs plus one stop event; unseen sign IDs collapse to UNK. States remain abstract, without semantic or phonetic values. Scaled forward/backward computations were checked against exhaustive hidden-path enumeration in a small independent test case.

For near-copy sensitivity, canonical exact/reversed sequences of equal length at least three are linked if either orientation differs by one sign. Connected components remain together in train/validation/test; two-sign and singleton texts receive only exact/reverse grouping. We shuffle components with seed 42 and allocate 80/10/10 percent by component count, reporting actual text proportions. Confidence intervals resample components. These are similarity groups, not verified artifact families, and transitive links can join otherwise different texts.

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

Most-frequent-sign mask baselines range from 9.4 to 11.4 percent. For seed 42, the bigram improvement is 0.980 bits/token, with bootstrap interval [0.795, 1.164]. Reversing all sequences preserves substantial predictive gains, so statistical direction preference alone does not settle reading direction.

### 4.2 Controls and generalization

On the seed-42 sign-only task, unigram, independent slot, and bigram losses are 7.085, 6.829, and 6.111 bits/sign respectively. Because the slot model knows length and scores only signs, these values should not be compared directly to the EOS-inclusive table. The slot model explains some predictability, while the tested bigram explains more.

Holding out Harappa, the unigram score is 6.463 and bigram score 5.665 bits/token on 757 distinct sequences. Holding out Mohenjo-daro, the unigram score is 6.553 and bigram score 5.646 bits/token on 1105 distinct sequences. Transfer does not establish universal grammar, since cataloguing conventions and shared artifact practices may also travel between sites.

A synthetic administrative slot generator, fitted to training-only positional distributions and supplied the observed lengths, yields conditional entropy 5.109 bits versus 3.892 observed. It fails to match adjacency and long repeats in this run. This rejects neither administration nor semasiography generally: the generator intentionally lacks local dependency, and synthetic duplicate records are retained for the descriptive comparison.

### 4.3 Candidate grammar, collocations and morphology

The seed-42 empirical role grammar covers 66.8 percent of held-out sequences, versus 32.3 percent of a single within-text shuffle. Coarse rare/flexible classes allow substantial coverage; this is not grammatical validation. There are 163 train-selected adjacency candidates, and 47 distinct five-sign subsequences recur across distinct complete texts. Such units could be names, formulae, codes, or other combinations.

In the clean CISI subset, 17 simple-stroke-before-fish adjacencies occur, versus mean 5.902 under the shuffle control, with upper-tail p=0.002. This is compatible with constrained number-like/fish combinations. It cannot distinguish fish as stars, commodities, identity markers, or components of words. No sound value or translation follows from this test.

### 4.4 A negative result for unconstrained substitution

Ten different bijective assignments of abstract syllable labels preserve conditional entropy exactly, to numerical precision. For 637 distinct labels there are 637! possible bijections, about 10^1511.4. This is a label-invariance demonstration, not a count of historically viable languages. It establishes that frequency and adjacency statistics alone cannot select the actual label meanings. A configured numerical grammar is achievable; recovery of the historical spoken language requires additional constraints.

### 4.5 Hidden-state grammar: a negative predictive result

Validation selects 8 states, initialization seed 29, and 20 EM iterations. Its test loss is 5.919 bits/token, compared to 5.461 for the validation-selected bigram. HMM improvement is -0.457 bits/token, with grouped bootstrap interval [-0.583, -0.343]. Thus the tested compact HMM family performs worse. This does not reject all latent grammars or linguistic interpretations; the parameterization, priors, training duration and short texts constrain the test. The chosen state count lies at the largest tested value, so the experiment does not establish an optimal state count. Exported emissions and posterior positional profiles are structural descriptions, not deciphered categories.

### 4.6 Near-copy robustness

In the original seed-42 split, 57 of 169 test texts of length at least three (33.7 percent) have a one-sign neighbour in training. The new graph has 1,713 connected components; the largest contains 74 canonical sequences. Component splitting produces 1,690 training, 235 validation, and 231 test texts.

On this new holdout, unigram loss is 6.527 and bigram loss 5.606 bits/token. Improvement is 0.922, with component-bootstrap interval [0.755, 1.077]. Prediction gains therefore survive this conservative similarity grouping. The change from the earlier score is not a causal measurement of leakage, since holdout size and composition differ. The comparison does not remove relationships between unequal-length texts or establish actual archaeological independence.

### 4.7 Annotated allograph history: no observed predictive gain

Experiment 003 validates the custom feature vectors of all 92 eligible CISI objects against the source schemas. These objects contain 455 sign occurrences, 133 base IDs, and 210 distinct base-ID/custom-morphology combinations. Default damage, line and uncertainty values are excluded from variant identity. The full variant inventory, integer encodings, descriptions, custom schemas and object references are exported separately; variants are not assumed to be independent graphemes.

Both prediction models target the same next base sign. The alternative uses only the preceding sign's morphology and interpolates to a base bigram when a variant history is sparse or unseen. It never uses the target's own morphology to predict that target. Base and variant strengths are validation-selected from 1/5/20/100, with exact/reversed base duplicates sharing partitions. Eligible object occurrences are retained, unlike the earlier deduplicated CISI summary.

Across five small holdouts of ten canonical groups, variant-history improvements range from -0.154 to -0.046 bits/token, averaging -0.080. All five point estimates favour base bigrams, while four confidence intervals overlap zero. This supplies no positive predictive support for this representation. It does not prove the variants have identical meanings or sounds: variant histories are sparse, and the sample is geographically narrow. The five holdouts overlap, so they are not five independent negative discoveries. Sound assignments or sign merging would require independent epigraphic and linguistic evidence.

### 4.8 Language-proxy representation sensitivity

Experiment 004 uses ten seeded matched-length samples for each of four conditions: Tamil words, Tamil letter-plus-mark clusters, Sanskrit words, and Sanskrit letter-plus-mark clusters. Every sample contains the exact Indus length list, 2,156 snippets and 9,221 tokens. A document eligible for each length is chosen uniformly, then a contiguous window is chosen uniformly, with replacement. No window crosses a document. Tamil documents are individual verses; Vedic documents are sentence blocks, using all upstream splits for descriptive sampling rather than predictive evaluation. Word/cluster normalization and source hashes are fixed before execution. Letter clusters group a Unicode base letter with following marks; they are not full extended grapheme clusters, phonetic syllables, or Sanskrit aksharas. Word separators are omitted from the cluster stream. Translations and semantic annotations do not supply Indus values.

| Proxy and unit | Mean H conditional | Mean shuffle-minus-real | Distance to Indus H |
|---|---|---|---|
| Tamil letter marks | 4.214 | 1.021 | 0.322 |
| Tamil words | 0.380 | 0.197 | 3.512 |
| Vedic Sanskrit letter marks | 3.427 | 0.760 | 0.465 |
| Vedic Sanskrit words | 1.958 | 0.072 | 1.934 |

All scores are in bits; Indus H conditional is 3.892, and its matched 49-shuffle-minus-real value is 0.869. Ranking by mean absolute conditional-entropy distance selects Vedic Sanskrit for word units and Tamil for letter-plus-mark units. The rank reversal is a negative result for using this single distance as a language identifier. The apparent winner depends on representation even with equal text lengths and token totals.

The sampled vocabulary sizes differ substantially: about 6,677 Tamil word types, 4,409 Sanskrit word types, 202 Tamil cluster types and 36 Sanskrit cluster types, versus 637 Indus sign types. Sparse word counts force low empirical conditional entropy even in frequency-preserving shuffles, illustrating estimator bias rather than low true language entropy. Sampling also produces duplicates: mean counts range from about 9 Tamil word windows to 363 Sanskrit cluster windows. Samples are not deduplicated because exact length matching is the declared design; overlap and document reuse remain limitations. The Vedic pool includes multiple citation texts and strata, not exclusively Rigvedic verse. The 49 shuffled trials have p-value resolution 0.02 and are descriptive controls, not decisive linguistic evidence. No language-family assignment, sign/word equivalence or phonetic key follows from the comparison.

### 4.9 Graphic stroke-count constraints and interpretive ambiguity

Experiment 005 examines described stroke counts rather than treating arbitrary sign IDs as values. We map only catalogue groups P121-P130 to one through ten short strokes, and P144/P145/P147/P150/P151 to one through five tall strokes. This represents catalogue morphology, not independently proven numeral values. Height remains distinct. The 91 complete deduplicated CISI texts contain 79 such slots; 11 tally-before-tally and three terminal cases are excluded from the following-sign test, leaving 65 events. The slot records retain object IDs, position and following-sign morphology for later epigraphic audit.

Mutual information between described count and following base-sign ID is 1.619 bits, compared to a mean 1.408 under 999 count-label permutations restricted by height and coarse initial/medial position. The upper-tail p-value is 0.002, or 0.004 after correcting the two prespecified tests. Short strokes alone yield 1.535 bits vs null mean 1.296, adjusted p=0.008. Sparse followers inflate empirical mutual information, so the excess over the matched null, rather than the raw score alone, matters. Slot-level exchangeability is assumed; this does not control every object-family or archaeological dependency.

The only three followers represented at least five times all admit multiple described counts:

| Following sign | Events | Described count: frequency |
|---|---|---|
| P004 | 5 | 3: 4, 4: 1 |
| P050 | 5 | 1: 1, 2: 1, 3: 1, 4: 2 |
| P086 | 8 | 3: 3, 4: 1, 6: 2, 8: 2 |

P004 is described as a burden-carrying person, P050 as a plain fish, and P086 as a branching tree form. These are visual descriptions, not commodity names. The observed combinations exhibit count/follower constraints under the specified null, but do not establish either unrestricted quantities or one fixed value per category. The test is motivated by competing administrative, ration and astronomical interpretations, including Mukhopadhyay's discussion of restricted number/sign combinations [10]. It does not replicate that paper's exact catalogue classes or refute a proposed reading: a verified glyph crosswalk and larger independently reviewed sample are missing.

Most importantly, no independent commodity amounts, matched weights or metrological scale are available for these objects. The experiment therefore cannot calibrate a unit, prove that three strokes mean the number three, or translate a fish sign as a star, gemstone, commodity, or personal-name element. Its contribution is an auditable morphological constraint table and specific combinations to check against independent evidence.

### 4.10 Paired-object catalogue correspondence

Experiment 006 strictly joins first-face Mohenjo-daro catalogue IDs to uniquely labeled ICIT-export objects, requiring both transcriptions to be complete single-line strings of equal length. Of 179 candidate objects, 85 pairs are accepted and 94 excluded: 87 Parpola-ineligible, five length mismatches and two ICIT-ineligible. Equal length does not prove equal segmentation or object/face identity. Grouping connects exact/reversed strings in either catalogue, retaining repeated texts within partitions. Seed 42 produces 67 training, nine validation and nine test objects.

On training positions, H(Parpola ID | ICIT ID) is 1.947 bits for direct alignment and 0.087 when reversing the ICIT sequence. Reversed alignment is selected using training data alone. This is relative source-order evidence for these matched objects, not global photographic verification of reading direction. The earlier main-corpus positional results still refer to stored ICIT order, and have not been automatically reinterpreted as prefixes or suffixes.

The learned majority correspondences correctly predict 32/42 validation positions and 31/39 test positions (79.5 percent including unseen-ID failures). Source-ID coverage is 82.1 percent on test data; 2/9 whole test sequences are correct. Known-source-only probabilistic loss is 3.485 bits/position using fixed additive 0.5 smoothing over training targets plus UNK; unknown target IDs collapse for this score. It does not measure translations.

The shortlist contains 29 training-derived review-priority correspondences, requiring at least three occurrences on two objects and >=90 percent agreement. Conflicting rows and unsuccessful objects remain in the output. Namespaces remain separate: no candidate mapping is treated as an independently glyph-verified equivalence, propagated to all inscriptions, or given a sound/meaning. Shared catalogue ancestry, source transcription errors, the face-ID assumption, small holdout and excluded segmentation disagreements limit independence. The result provides a reproducible path toward catalogue reconciliation needed before constrained interpretation.

### 4.11 Reference-glyph screening and numerical morphology

Experiment 007 screens the 29 shortlisted reference glyphs against their supplied Parpola shape descriptions. This is Codex-assisted review of standardized catalogue drawings, not blinded expert review or examination of original-object photographs. Broad shapes are compatible with the descriptions, while the 002 short/tall-stroke conflict, the rounded/angular 817/861 variants grouped under P385, and the uncertain asymmetric-animal label remain unresolved. No candidate is promoted to an independently verified equivalence or assigned a sound or semantic value.

All 715 pinned reference images were acquired into private local cache. Source URLs and SHA-256 hashes are preserved. Scalar numeric descriptors encode thresholded ink bounding-box aspect, ink density, centroid, second moments and eight-connected component counts. Image assets, fonts and reconstructible pixel grids are not packaged. These features describe rendering morphology; cropping, antialiasing, stylistic choices, crossings and gaps can affect them. They are not learned linguistic or semantic embeddings.

The six already screened simple-stroke examples produce component counts 1, 2, 3, 4, 1 and 3 for IDs 001, 002, 003, 004, 031 and 033, matching their described shapes. Two independent synthetic-mask tests check connectivity and translation invariance. The source-derived matches validate extraction only, not discovery of numerical values. Optional Pillow-based production can reacquire/hash-check the images; default offline reproduction validates the committed numerical snapshot's hash and arithmetic invariants rather than regenerating image features. Original-object and catalogue provenance verification remains necessary before interpretation.

### 4.12 Metadata-conditioned formula models and smoothing sensitivity

Experiment 008 retains all 3591 eligible artifact rows with their metadata, grouping exact/reversed texts before partitioning. Seed 42 yields 2989 training, 303 validation and 299 test rows. Duplicates remain weighted as observed occurrences, so these scores are not directly comparable to the earlier deduplicated benchmark. Metadata conditions use the literal type prefix, site, or their combination, and back off to pooled bigrams. Both smoothing strengths are selected on validation data from 1/5/20/100. Target signs, speculative translations and interpretive classes are excluded from metadata.

| Metadata condition | Test bits/token | Gain vs selected pool | Gain at matched smoothing |
|---|---|---|---|
| type | 5.439 | 0.060 | 0.015 |
| site | 5.532 | -0.034 | -0.079 |
| site_type | 5.419 | 0.079 | 0.034 |

The validation-selected pooled benchmark scores 5.499 bits/token. Site-plus-type gains 0.079 bits/token, with grouped 98.33 percent interval [0.013, 0.151] as a three-comparison sensitivity. However, the metadata models select pooled strength 100 while the pooled benchmark selects 20. An exploratory matched-strength ablation, added after initial scores without reselecting models, reduces the type and site-plus-type increments to 0.015 and 0.034 bits/token. Their 95 percent intervals [-0.059, 0.081] and [-0.020, 0.088] overlap zero. Site-only conditioning is worse at matched smoothing (increment -0.079, interval [-0.149, -0.021]). Thus the nominal aggregate gain is partly attributable to smoothing differences; this test does not establish a robust independent metadata contribution.

Confidence intervals resample whole exact/reversed groups (1,000 draws); related molds, near copies and uncertain type annotations are not fully controlled. Test rows are dominated by 159 seals and 94 tablets, with other categories much smaller. Archaeological usage differences remain plausible, but these fitted formulas do not decode commodities, names, dialects or grammatical parts of speech. Metadata and transcription quality require further review before interpreting a single reconstructed grammar across object classes.

### 4.13 Published fish-rebus witnesses and conditional readings

Experiment 009 examines selected published astronomical proposals [11] and their critique [12]. H-9's exported stored string is 220-017: a plain-fish reference followed by seven-stroke morphology, matching the graphic example named by Parpola. M-112 contains 220-016 in the export, but its annotated CISI transcription contains P126 followed by P056, a modified fish rather than P050. Damage/uncertainty elsewhere excludes this object from the earlier clean CISI subset. Thus the absence of six/plain-fish there cannot be used to reject the published example; eligibility and sign-subtype disagreement must be reported first. These are retrospective named-witness checks, not independent discoveries or original-object photo verification.

For the larger complete unique diagnostic subset, provisional short-stroke reference aliases yield 43 plain-fish/stroke slots. Their described counts are 1 (2), 2 (10), 3 (14), 4 (6), 6 (10), and 7 (1). The published-example count set 3/6/7 occurs in 25/43 fish slots versus 162/770 other-follower slots. An exploratory count-label permutation gives upper-tail p=0.001; opposite stored adjacency gives p=0.149. This diagnostic assumes slot exchangeability, provisional reference-code correspondences and a declared stored-order convention. The count-set enrichment is our operational extension, not a claim that the published theory restricts every fish sequence to those counts. It supports a restricted graphic combination, not a constellation, number value or language family.

The audit includes an explicit conditional rendering of H-9 under Parpola's proposed fish/star rebus: if the strokes mean seven and the fish sign represents proposed miin/star, the author's eZu-miin reading refers to seven stars/Ursa Major [11]. This is a published hypothetical phonetic/semantic assignment, not a deciphered value adopted by this project. An unknown quantity/classifier template and an unknown category/rate template admit precisely the same two graphic tokens. No independent semantic label, measurement or bilingual identifies which interpretation is correct. The alternatives remain unresolved, and a plausible lexical parallel alone is insufficient to translate the inscription.

### 4.14 Uncertainty-sensitive training and source-agreement limits

Experiment 010 keeps the clean seed-42 validation/test objects fixed and varies only training eligibility. All broader objects have nonempty single-line transcriptions and no P000 unknown stretch; exact/reversed clean holdout copies and object IDs are excluded from additions. The intermediate condition limits each literal raw damage and uncertainty code to 25. This is not a calibrated percentage: damage codes can encode locations in higher digits. The broad condition retains all remaining damage/uncertainty-marked readings as transcription hypotheses, not known truths. Bigram smoothing is selected on the same clean validation set.

| Training condition | Objects | Clean-test bits | Gain vs clean |
|---|---|---|---|
| clean | 73 | 5.644 | 0.000 |
| raw_codes_le25 | 98 | 5.592 | 0.052 |
| all_known_singleline_readings | 135 | 5.597 | 0.047 |

Adding 25 intermediate-filter objects gives a 0.052-bit improvement with grouped 95 percent interval [-0.095, 0.230]. Adding 62 broader objects gives 0.047 bits, interval [-0.234, 0.329]. Both intervals overlap zero, and unseen clean-test token counts decrease from seven to five. The modest point gains may reflect coverage rather than correctness of uncertain readings. Ten canonical test groups are too few for strong conclusions, and guessed/damaged transcriptions cannot be promoted to accepted data merely because a predictor uses them.

A separate equal-length paired-source audit accepts 136 objects and examines 733 reversed aligned positions against supplied Wells alias lists. It finds 43 alias-absence positions; 38 have zero local damage and uncertainty codes. M-112's plain/modified fish disagreement is among these unmarked positions. Alias absence can reflect incomplete crosswalks, variant splitting or transcription differences; it is not automatically an error. The result shows that annotation filters alone do not establish cross-corpus agreement. Original-object/face and glyph verification remains an independent requirement before assigning phonetic values or interpreting inferred grammar.

### 4.15 Exact reconstruction of contiguous sign gaps

Experiment 011 extends synthetic masking to every contiguous one- or two-sign span of complete seed-42 held-out ICIT strings. Exact/reverse copies share partitions. Ordinary validation sequence loss selects bigram smoothing 20; neither masked targets nor test-neighbor strings inform candidate selection. Every actual training sign is allowed, excluding EOS/UNK. Exhaustive fillings are scored with left, internal and right transitions and normalized over that closed inventory. The unigram baseline has the same inventory and gap lengths. One-sign results exactly reproduce the earlier diagnostic. This follows the missing-sign prediction rationale reviewed in the Markov literature [13]; it is an independent benchmark, not a replication of published restoration claims.

| Gap length / model | Masks | Whole-gap top1 | Whole-gap top5 |
|---|---|---|---|
| 1 / unigram | 926 | 10.3% | 24.5% |
| 1 / bigram | 926 | 35.5% | 55.0% |
| 2 / unigram | 709 | 0.0% | 0.1% |
| 2 / bigram | 709 | 12.7% | 25.0% |

For two-sign gaps, the best bigram filling has 25.2% token accuracy; the entire true gap is in the training inventory in 96.1% of masks. The whole-gap top1 advantage over unigrams is 12.7 percentage points, grouped 95 percent interval [9.7, 15.7]. Bootstrap resampling keeps overlapping masks within each of 202 canonical inscription groups. All test targets, including unseen signs, remain in the accuracy denominator.

Mean top1 conditional probability for two-sign bigram fillings is 9.4%. Fixed posterior-bin observed accuracies and per-mask top-five candidates are exported for audit. These probabilities assume a known gap length and a closed candidate inventory; they omit unseen glyph possibilities and must not be interpreted as archaeological certainty. Synthetic masked truth is a secondary transcription, not independently verified glyph evidence. No completion of 000 unknown stretches is produced because their cardinality is unknown, and no recovered integer code acquires a phonetic or semantic value.

### 4.16 Richer administrative compatibility control

A recent preprint describes a purpose-built non-phonetic emblem system and stresses the specificity limits of structural measures [14]. We inspected selected construction, prediction and limitations passages, but could not retrieve its corpus from the checked article/source archive and repository searches. Its published results are not reproduced here. Experiment 012 is an independently authored control with declared parameters.

Our fictional inventory has 160 institutions, 96 guilds, 160 commodities, eight quantity emblems, four ranks and five validators. Optional institution, guild/rank, quantity/commodity and validation blocks match the exact Indus length list. Fixed institution/guild and guild/commodity licenses and preferred rank/quantity pairs induce dependencies; every token retains its semantic role and value. Only lengths are empirically matched: no Indus sign frequencies or transitions tune this generator, and no sounds or dictionary enter generation. Three seeds produce 2,156 records and 9,221 tokens each. Generated duplicates remain weighted, with exact/reversed copies kept within split groups; model smoothing is validation-selected using our established EOS/UNK benchmark.

| Seed | Types | Conditional bits | Unigram bits | Bigram bits | Mask top1 |
|---|---|---|---|---|---|
| 17 | 408 | 2.906 | 6.241 | 3.977 | 34.5% |
| 29 | 406 | 2.905 | 6.171 | 3.954 | 34.0% |
| 43 | 416 | 2.913 | 6.427 | 4.185 | 33.1% |

Every realization rejects its own within-text shuffle at the minimum possible p=0.010 with 99 trials, and every grouped unigram-to-bigram gain interval excludes zero. Mask prediction also exceeds each realization's frequent-sign baseline. Thus conditional predictability and shuffle rejection occur in a notation generated without phonetic values. The richer control repairs a limitation of the earlier independent-slot simulation: institutional licenses create local dependencies rather than merely different positional frequencies.

This is a compatibility demonstration, not a calibrated linguistic/non-linguistic classifier or a reconstruction of Harappan administration. Its vocabulary and duplicate frequencies differ from the real corpus; near-copy families are not separated, and three seeds sample one chosen architecture rather than all plausible alternatives. It does not show that Indus signs are non-linguistic, nor assign an institution, commodity, quantity or sound to any Indus ID. Structural gains alone remain insufficient to configure a historically justified spoken-language reading.

### 4.17 Primary Mahadevan acquisition, signs and annotation preservation

Experiment 013 acquires the official Indus Research Centre/RMRL application's public archaeological collection through paginated reads. The frozen whitelist snapshot contains 3916 records, including 3573 nonempty text rows. Raw S1-S14 strings, doubtful asterisks, gaps, combined side/line codes, directions, object/field-symbol codes and locus/level metadata are retained with source update times and page hashes. Pagination is not an atomic historical database snapshot; offline results refer only to the committed frozen copy. No proposed sound mappings enter acquisition.

The original printed code tables and four sign-list pages were visually checked in the 1977 source [15]. Codes 4/5/9 denote vertical/symmetric/doubtful arrangements, respectively; a secondary codebook shifts those labels. The 417 original sign-list IDs now have separate integer tokens and page-linked glyph references. They are not merged into Parpola or Wells IDs, and raster book pages are not redistributed. A zero denotes an illegible stretch of unknown cardinality, mapped to a reserved unknown slot rather than a sign or padding; doubtful readings retain both base ID and uncertainty flag.

All 2742 secondary sequences [16] match a side-specific reconstruction of primary base IDs. However, 265 lose doubtful marks and 92 concatenate multiple primary lines. Primary records contain 504 doubtful tokens in total. Thus matching base codes does not certify clean text or preserve layout. The secondary export remains an audit comparator, not ground truth.

A declared strict screen retains 2391 single-line rows with 375 IDs and 1534 distinct exact/reverse canonical strings. It excludes gaps, doubtful signs, nonhorizontal/uncertain arrangements, count inconsistencies and unresolved layouts. All 417 IDs occur somewhere in the raw snapshot. This is acquisition and numerical encoding, not a new modeling result, face-verified crosswalk or semantic anchor. Original-object verification and controlled tests of the new corpus remain separate work.

### 4.18 Face-preserving field-symbol prediction

Experiment 014 uses strictly screened primary lines with their own field-symbol metadata. Before target filtering, rows sharing a source object number or exact/reversed sign string form connected components. This links all faces, including rows later excluded for target codes 0/999. There are 1321 components among 2,391 strict rows. Component-count splitting yields 1,427/787/177 rows; the largest component has 592 rows and lies wholly in validation, contributing 96 target rows. This large transitive group makes validation composition uneven and is retained rather than split to improve the score.

After literal target-code exclusions, training/validation/test have 878/198/99 rows. Exact codes with at least 20 distinct training objects remain separate; others become RARE. Target classes are raw codes, not animal-name glosses. The baseline interpolates site/object-type/length-bin class counts to pooled class priors. Validation selects strength 1; this stays fixed when training-only distinct-sign likelihoods are added. Validation chooses sign weight 0.5, with zero weight available as an ablation. No hidden target field enters the sign predictor.

| Model | Test bits/row | Accuracy | Macro recall |
|---|---|---|---|
| metadata baseline | 1.647 | 71.7% | 20.8% |
| metadata plus signs | 1.629 | 70.7% | 19.8% |

The paired log-loss gain is 0.017 bits per archaeological row, with connected-component 95 percent interval [-0.018, 0.051] across 88 test groups. The interval includes zero, while accuracy and macro recall both decrease. Always selecting the training-majority code scores 67.7% accuracy. Code 13 supplies 67/99 test rows; neither model correctly predicts any of the four other individually retained codes in this small test set. Five test metadata strata are unseen and 26/466 sign tokens are outside the training inventory.

This tested predictor does not establish an independent iconographic/semantic anchor or disprove all sign/motif associations. RARE combines heterogeneous targets, class imbalance is strong, one large group influences validation, and near-copy/mold-family independence remains unresolved. Connected splits, class-wise confusions, probability vectors and all validation candidates are exported. A sign could covary with motif through institutional or production conventions rather than name the depicted entity; no phonetic or lexical assignment follows.

### 4.19 Reference-number candidates and original photographs

Experiment 015 reads the original CISI 1 metadata page for M-1 through M-100 [17]. The book warns that Finnish concordance (FC) and Mahadevan reference numbers are not uniformly interchangeable. Consequently a matching FC/Mahadevan number is used only to generate a candidate transcription pair, not to establish an independently verified object identity. One uncertain numeric reading is flagged; no supplied sign alias selects or filters the pairs. An M-1 pilot and its aliases were inspected before design, so its whole duplicate group is forced into training.

Eligibility requires a unique Parpola A-face transcription and a strict primary Mahadevan side-0/line-0 record with the same candidate number and length. Of 100 references, 34 survive; exclusions are 45 Parpola-ineligible, 14 outside the supported reference range, four unequal lengths, two missing/ambiguous Parpola faces and one uncertain number. Exact/reverse copies in either namespace share groups. The 27/3/4 train/validation/test candidate split selects direct relative alignment by training correspondence entropy (0.153 vs 1.562 bits reversed).

A training-majority Parpola-to-Mahadevan mapper predicts 10/21 test positions, with 10/21 source-sign coverage and no fully correct test inscription. Every covered test position agrees, while unseen source signs remain failures. Fourteen training mappings reach the declared review threshold. These are conditional consistency results on unverified reference candidates, with only four test objects, not validation of all FC identities or sound values. No crosswalk is automatically propagated.

Original seal/impression photographs were actually inspected for M-1, M-3 and M-4 (printed pp. 1-3), rather than standardized drawings alone. M-1's HR 2406 edge marking matches its catalogue metadata; A-face and lowercase-a impression are visibly mirrored. M-3 shows three main graphic groups, with a broken lower/right body. M-4 has a longer mirrored sequence and textured/damaged surface, but its uncertain reference remains excluded. The record explicitly distinguishes this unblinded Codex-assisted screening from an expert transcription or complete allograph verification. The scans are cached privately, not redistributed. Further object-reference resolution and independent glyph review remain necessary.

### 4.20 Original graphic variants and postscript signs

Experiment 016 manually indexes every drawn form in the original variant appendix (printed pp.785-792) and inspects the sign-list postscript (printed p.25) [15]. The appendix count reconciles with the introduction only when the separate variant-addendum column is included:

| Section | Source families | Drawn forms |
|---|---|---|
| Main appendix | 167 | 615 |
| Variant addendum | 12 | 26 |
| Combined | 179 | 641 |

All 641 forms have a source page/column, a literal example citation and a separate research ordinal/integer. Continuations of one family across columns preserve ordinal order. These are source-defined graphic families, may include the normal form and are not 641 additional independent signs or sounds. The catalogue adds two postscript base-sign references, M418/M419, while keeping the existing 417-ID benchmark and its integer assignments unchanged. The cited postscript inscriptions 8401/9222 are absent from the frozen application snapshot.

The occurrence lookup finds 613 citations with one matching base-sign occurrence, 21 with repeated matching occurrences, five with no matching base ID and two unresolved parenthetical suffixes. Of the unique candidates, 133 are in rows flagged by the earlier source screen. No variant is automatically assigned even when the lookup is unique. The five remaining base-absence cases are MV254-main-07/1467, MV331-main-03/4592, MV347-main-04/7047, MV348-main-02/2055 and MV278-addendum-01/4595; enlarged page checks retained those printed citations rather than substituting convenient corpus matches.

An initial citation audit prompted thirteen visually confirmed digit corrections, all recorded with before/after values and source pages. Count agreement and successful lookups do not independently certify every manual digit or the editor's allograph judgements. Original rasters remain in private cache; the repository publishes numeric metadata and page-linked glyph references. Graphic distinctions are preserved as evidence for later review, without new phonetic values, language identification or changes to historical transcriptions.

### 4.21 Constrained substitution with positive and negative controls

Experiment 017 follows a committed design. Substitution/noisy-channel passages in Knight et al. [18] and cognate constraints in Luo et al. [19] motivate calibration and explicit channel assumptions; neither published algorithm is replicated. Our bijective search maps 32 selected source symbols onto 32 frequent writing units in each pinned Tamil/Vedic proxy. Units use the earlier base-plus-following-marks normalization, not validated phonemes or aksharas. A fixed UNK preserves every other token and its edges. Target models use add-0.5 unigrams and strength20 interpolated bigrams, initial-unit plus internal-edge likelihood without EOS. These scores are distinct from earlier EOS-inclusive scores.

Complete source documents are split by exact/reverse groups, seed314, into disjoint model and calibration pools. Tamil has 472 model/316 calibration documents; Vedic has 16,442/10,740. The 32 units cover 58.0% of Tamil model tokens versus 99.8% of Vedic tokens. Source stages, literary genres, normalization and UNK rates differ sharply, making cross-language absolute losses unsuitable for family identification. Two proxies do not exhaust language possibilities.

Known artificial substitution ciphers use 2,156 held-source windows matching the Indus length list. Five starts each receive 20,000 annealing swaps and up to two greedy sweeps. Training fits keys, validation selects a restart, and test scores follow selection. Twenty fixed random keys and frequency rank are baselines. The calibration's source documents never train the target language model; its train/test windows may overlap within held documents, so this is a favorable artificial recovery check, not independent historical validation.

| Proxy / input | Frequency bits/token | Selected bits/token | Restart key agreement |
|---|---|---|---|
| Tamil / known cipher | 4.191 | 3.346 | 69.7% |
| Tamil / Indus | 4.456 | 3.862 | 6.6% |
| Tamil / nonphonetic | 4.760 | 4.000 | 14.1% |
| Vedic Sanskrit / known cipher | 4.420 | 3.680 | 36.9% |
| Vedic Sanskrit / Indus | 7.908 | 6.771 | 28.7% |
| Vedic Sanskrit / nonphonetic | 8.571 | 6.279 | 30.6% |

The selected Vedic calibration key recovers all 32 substitutions and 100% of covered test tokens; Tamil recovers 24/32 and 68.4% of covered tokens, versus frequency-key accuracy 20/32 and 9/32 respectively. The Tamil true-key oracle scores 3.235 bits/token, better than the selected 3.346: partial calibration failure remains visible. Recovery truth is consulted only after search and validation selection.

Indus split sizes are 1,723/216/217, before training-only sign selection; only 59.4% of test tokens have one of the 32 mapped signs. Gains over frequency rank are 0.594 Tamil and 1.137 Vedic bits/token. However, mean pairwise restart key agreement is only 6.6%/28.7%. The deliberately nonphonetic administrative control also improves, by 0.761/2.292 bits/token; gains therefore do not establish linguistic decoding. Its split is 1,740/197/219 and mapped test coverage 67.5%. Collapsing rare signs produces 93/217 Indus and 81/219 control test patterns seen in training, despite full-ID exact/reverse separation. Near-copy/family leakage and the restricted one-to-one alphabet further limit generalization.

All keys, restart and random scores, coverage and twenty conditional Unicode recodings per condition are exported in results/substitution_search.json. These incomplete strings are hypotheses, not translations. No external lexical, archaeological or bilingual observation validates a real key; no sound value is adopted. Known-cipher success shows the solver can recover a suitable artificial channel, while the controls show why score improvement alone is insufficient.

### 4.22 Novel-pattern substitution holdout audit

Experiment 018 is a retrospective sensitivity analysis: Experiment017's aggregate scores and overlap counts were already observed before its follow-up design was committed. It supplies no new independent corpus or blind confirmation. Keep the earlier training data, top32 training-selected signs, frozen target counts and five fitted keys unchanged. Remove validation strings whose exact/reverse encoded pattern appears in training. Remove test strings whose encoded pattern appears in training or retained validation. Every fixed UNK slot remains in place. Retained partitions have disjoint collapsed pattern sets; repeated patterns within one partition retain their row weights.

Indus training remains 1,723 texts; validation shrinks 216 to 128 (88 training-pattern exclusions) and test 217 to 122 (93 training-pattern and two validation-pattern exclusions). Control training stays 1,740; validation 197 to 115 (82 exclusions), test 219 to 137 (81 training-pattern and one validation-pattern exclusion). Retained test mapped-token coverage is 67.3% Indus and 71.6% control; unresolved tokens remain. Their 119 and 87 canonical collapsed test patterns respectively define bootstrap groups, not verified archaeological families. Full source strings, encodings, original split indices, exclusions and per-test losses are exported.

| Proxy / input | Frequency bits/token | Selected bits/token | Gain / 98.75% interval |
|---|---|---|---|
| Tamil / Indus | 4.976 | 4.283 | 0.693 [0.453, 0.975] |
| Tamil / nonphonetic | 4.976 | 4.138 | 0.837 [0.451, 1.270] |
| Vedic Sanskrit / Indus | 7.844 | 6.763 | 1.080 [0.700, 1.484] |
| Vedic Sanskrit / nonphonetic | 8.811 | 6.253 | 2.558 [1.537, 3.450] |

Intervals use 5,000 token-weighted canonical-pattern bootstrap draws, seed 20261017, with 98.75% percentiles as four-comparison Bonferroni sensitivity. All four also have 95% intervals excluding zero. These are corpus-conditional uncertainties, not evidence for a language or guarantees about unseen artifact families. Removing rows changes difficulty and coverage, so gains before/after filtering do not estimate a causal leakage effect.

Reselecting among the original five keys using only retained validation keeps start 29 for both Indus proxies and start 17 for the Tamil control. Vedic control changes 43 to 17; the original key scores 6.300 on the same subset versus 6.253 for the reselected key (frequency 8.811). Thus most of that control gain survives even without reselection. No training refit or vocabulary change occurs; stored training losses are independently reconstructed and checked before reuse. Both artificial cipher controls retain every row, reproduce previous test scores and retain 32/32 Vedic and 24/32 Tamil key recovery.

The improvement therefore extends beyond exactly repeated collapsed strings, but it also extends to the explicitly nonphonetic control. This narrows one explanation for the fit without validating any actual reading. Weak restart agreement, one-unit-per-sign restriction, literary target mismatch, unknown collapse, stored-order uncertainty and unseparated near-copy families remain. No phonetic key or language identification follows.

### 4.23 Full-vocabulary homophonic glyph channel

Experiment 019 addresses the previous top32-source restriction. It is motivated by selected homophonic/noisy-channel and type-update passages in Ravi and Knight [20], not a replication of their Bayesian CRP/Gibbs sampler or dictionary-based model. A deterministic key maps every training glyph to one of 32 selected proxy writing units; several glyphs may share a unit. All 32 units must be occupied so each target state's emission distribution is defined. Only source types unseen in training use a fixed source/target UNK slot. No full historical phonetic inventory, proto-language reconstruction or semantic anchor is supplied by these units.

To account for distinct source glyphs, the normalized channel uses P(s|g(s))=(f_s+0.5)/sum_r(f_r+0.5), summing only training glyphs assigned to that unit. Frequencies are training-only; source UNK emits with probability 1 from target UNK. The sequence probability combines the frozen target initial unigram/internal bigrams with every glyph emission, without EOS. Optimizing recoded fluency alone would omit the cost of explaining multiple distinct glyphs. These total glyph-space scores therefore cannot be compared directly with Experiment 017/018's incomplete recoding scores.

Equal-length one-substitution neighbors of length>=3, exact/reverse copies and their transitive closure stay in one partition. Groups are shuffled seed 42 and split 80/10/10% by component count. Indus has 1,713 components, largest 74 canonical texts, with 1,690/235/231 rows and 584 training glyph types across 637 total. Test source coverage is 96.9%; 53 types outside training receive no key. Control has 1,160 components, largest 117, with 1,822/167/167 rows, 396/408 types and 99.2% test coverage. Fixed-UNK test-pattern overlap with training is zero for every condition. Similarity groups are not independently verified artifact families; row proportions and difficulty differ from earlier splits. Source order remains as stored, not proven reading direction.

Five starts each receive 30,000 mixed type moves/swaps and up to two greedy single-type sweeps. Moves that empty a target unit are rejected. Training fits the key and add0.5 emission counts; validation selects a restart. Baselines are an arbitrary cyclic key, plus generic training-only add0.5 unigram and strength20 sign bigram models on the same full source alphabet, initial/internal likelihood and test rows. No model or direction is selected using test scores.

| Proxy / input | Channel bits/token | Source unigram | Source bigram |
|---|---|---|---|
| Tamil / known cipher | 4.385 | 4.885 | 4.689 |
| Tamil / Indus | 7.996 | 7.233 | 6.335 |
| Tamil / nonphonetic | 7.349 | 7.033 | 5.259 |
| Vedic Sanskrit / known cipher | 4.667 | 5.277 | 4.872 |
| Vedic Sanskrit / Indus | 7.454 | 7.233 | 6.335 |
| Vedic Sanskrit / nonphonetic | 6.383 | 7.033 | 5.259 |

Positive controls give two random opaque homophones to each unit in the earlier held-source windows; 64 aliases are scrambled, variant choices use seed 2031, and every training alias remains distinct. Both selected keys recover 64/64 aliases and 100% of covered test tokens, matching their true-key channel oracles. Tamil calibration split 1,821/202/133 (1,217 components, largest 249) and Vedic 1,760/209/187 (1,579 components, largest 272). All true target units occur among training aliases, satisfying the surjection constraint. Repeated/overlapping windows within held source documents can still cross partitions; source documents never train the target model. Truth is supplied only for generation and post-selection recovery diagnostics, never optimization.

Despite successful artificial recovery, both Indus proxy channels lose to source unigram (Tamil +0.763, Vedic +0.221 bits/token) and source bigram (Tamil +1.661, Vedic +1.119). These are held-out point comparisons, not universal rejection of language families or every homophonic model. Tamil/Vedic Indus emission costs are 2.166/2.682 bits/token on top of language parts 5.830/4.771. Mean pairwise key agreement across starts is 6.2%/7.4%, so fitted keys remain highly unstable. The nonphonetic Vedic channel beats its unigram by 0.650 but remains worse than its source bigram; the Tamil control loses to both. Thus even a channel gain need not imply phonetic content.

All 584 Indus training-glyph mappings, 53 unassigned types, unit occupancies, per-start keys/validation scores, split groups, per-test losses and twenty incomplete hypothetical recodings are exported. The previous source-vocabulary truncation is largely removed, while target-unit truncation, proxy chronology/genre, deterministic one-unit-per-sign assumptions, sparse signs, shared corpus ancestry and unknown original reading order remain. No mapping is adopted as a historical sound value. This calibrated extension supplies a failed broad-coverage attempt and a reusable channel, not a translation.

### 4.24 Joint validation selection of channel key and order

Experiment 020 freezes the earlier target counts, full training vocabulary, similarity components, source-row identities and hyperparameters. It tests stored vs reverse-stored token order within every string, without repartitioning or changing row order. Earlier forward results were already observed, making this a retrospective sensitivity check, not independent blind confirmation. Neither alternative corresponds automatically to absolute archaeological left/right reading, because source transcription and seal/impression orientation require separate verification.

Five forward keys are reused after source/key-digest and training/validation loss checks; five reverse keys receive the identical 30,000-proposal/two-sweep budget. Minimum validation loss chooses among all ten candidates, with stored-order/start-index tie preference. The generic strength20 sign bigram chooses its own direction by validation. Both choices occur before new test scores are computed; source unigram is verified invariant under reversal. Test row/token identities are identical across comparisons. No test-driven direction or restart replacement occurs.

| Proxy / input | Selected order | Channel bits/token | Selected sign bigram |
|---|---|---|---|
| Tamil / known cipher | stored | 4.385 | 4.698 |
| Tamil / Indus | reverse stored | 8.034 | 6.329 |
| Tamil / nonphonetic | stored | 7.349 | 5.259 |
| Vedic Sanskrit / known cipher | stored | 4.667 | 4.853 |
| Vedic Sanskrit / Indus | stored | 7.454 | 6.329 |
| Vedic Sanskrit / nonphonetic | stored | 6.383 | 5.259 |

Indus Tamil selects reverse-stored/cyclic, validation 7.563 versus best stored 7.684. Its test 8.034 is slightly worse than the earlier stored 7.996, a disclosed validation/test disagreement. Vedic selects stored/start 17 (validation 7.203 versus best reverse 7.252), preserving test 7.454. Both generic Indus bigrams select reverse-stored and score 6.329. Source unigram remains 7.233. Thus a simple reversal does not rescue these tested channel fits, but this result does not exclude other writing-unit inventories or linguistic systems.

Paired gains mean baseline minus selected channel, so negative values favor the baseline. Similarity-component bootstrap uses 5,000 draws, seed 20261018, weighting total bits/tokens within groups. Indus has 172 test components across 231 rows. Tamil gains over unigram/bigram are -0.801/-1.706 bits/token; 98.75% intervals as four-comparison sensitivity are [-1.101,-0.535]/[-1.995,-1.394]. Vedic gains are -0.221/-1.125, intervals [-0.499,0.014]/[-1.370,-0.891]. Its small unigram deficit is therefore uncertain at that sensitivity; both bigram deficits retain negative intervals. These bounds condition on this corpus and fitted selection; they do not incorporate every model/selection uncertainty or verify archaeological families.

Both artificial 64-alias controls choose stored order and recover 64/64 mappings, 100% covered-symbol and original-sequence token accuracy. The generic bigram nevertheless chooses reverse-stored for both synthetic controls, illustrating why a generic model's direction preference alone cannot establish true orientation. Cipher windows can still overlap within their held source documents. Nonphonetic controls retain stored order, scoring 7.349 Tamil and 6.383 Vedic versus unigram 7.033/bigram 5.259. The Vedic nonphonetic gain over unigram remains 0.650 (descriptive 95% interval [0.561,0.727]) while losing to bigram. Controls do not supply Indus semantics.

All ten candidate keys and validation scores, post-selection diagnostic test scores, selected conditional recodings, per-component gains and paired per-test losses are exported in results/channel_direction.json. Full source/split identities remain referenced to the frozen Experiment 019 artifact; integer-key/source digest excludes floating fields to preserve cross-platform numerical tolerance. No accepted sound values, actual reading direction, language identification or translation follows. Target 32-unit coverage and historical genre/stage mismatch remain priorities for further work.

### 4.25 Complete target-unit acquisition and feasibility

Experiment 021 prepares the broader target inventory rather than fitting a new Indus decoder. Exploratory whole-source counts were known before its design: 233 normalized Tamil units across 204,469 tokens and 38 Vedic units across 1,161,219. The Tamil text field contains three single Latin-letter tokens (a,b,r), all in the held source pool; they cannot explain the earlier model's 42% unknown mass. Rare and unusual mark combinations remain literal, with codepoint/name metadata rather than silent correction. These are writing units produced by normalization, not validated phonemes or reconstructed ancient sounds.

Using the exact frozen Experiment 017 model/held document IDs and sampled-window offsets, export every model-document unit, full unigram/internal bigram counts and the same held-source windows. No new poem selection or word dictionary is introduced. Coarsening these full counts back to the earlier 32-unit inventory reproduces every integer cell exactly. The same windows also reproduce the original cipher after its diagnostic permutation is inverted. Raw pinned source hashes are checked during optional preparation; full-input and coarse-input hashes plus identity/lineage checks support the offline audit. Adapted Vedic data retain CC BY-SA4.0 attribution.

| Proxy | Full model units | Held token coverage | True units absent in cipher training |
|---|---|---|---|
| Tamil | 225 | 99.98994% | 27 |
| Vedic Sanskrit | 37 | 99.99978% | 1 |

Tamil model has 225 units/124,964 tokens from 472 documents; its 316 held documents contain 79,505 tokens, with eight held-only unit types occurring once each. Vedic model has 37 units/698,682 tokens from 16,442 documents; 10,740 held documents contain 462,537 tokens, with one held-only unit (a rare Latin diacritic letter) occurring once. Full model coverage is 100% by construction. Earlier top32 model coverage 57.971%/99.811% quantifies target truncation within these fixed document pools; historical genre/stage mismatch remains unresolved.

New two-alias-per-unit artificial ciphers preserve the original 2,156-window length list and use variant seed 2031/alias permutation 1031. Similarity-component splitting yields Tamil 1,731/213/212 rows (2,059 components, largest 6), 362 training aliases of 450 planned; 198/225 true units occur in training, leaving 27 absent. Vedic 1,762/200/194 (1,580 components, largest 279), 70 aliases of 74 planned; 36/37 true units occur in training. Both have enough observed training glyph types numerically, but their true keys cannot satisfy the earlier requirement that every target unit receive an observed training glyph. Truth is used solely for this known artificial feasibility diagnostic.

This identifies a concrete obstacle to extending the existing surjective algorithm: deleting rare units or forcing arbitrary assignments would change the problem and could exclude the correct key. A broader normalized emission model must permit unoccupied units while accounting for unknown observations, for example by an explicit unknown emission and marginalization. That decoder is not implemented or scored in this release. Frozen inputs in data/full_target and results/full_target_audit.json now support its development. No expanded-target fit, Indus sound value, family identification or translation is claimed; earlier 32-unit experiments remain unchanged.

## 5. Limitations and implications for decipherment

The main dataset is a secondary public export. No new glyph transcription, full catalogue reconciliation, artifact-family grouping, or independent translation anchor has been established. Splitting reverse/exact copies does not eliminate all near-duplicate or formula leakage. Allograph distinctions may inflate the vocabulary and hapax rate (36.1 percent in the main subset). The complete-only filter selects against difficult inscriptions and may bias inference. Rare sign embeddings and small CISI morphology counts are unstable.

The models establish conditional predictability under declared controls. They cannot determine whether that structure encodes phonology, names, quantities, transactions, or a mixture. Fitting an unconstrained rebus or a surname list would risk selecting the desired answer through researcher flexibility. Later Tamil and Sanskrit proxies have now been compared structurally under fixed representation choices; the additional 32-unit conditional substitution experiment uses literary proxies, not historically matched, independently anchored Indus sound values. No Proto-Dravidian, Indo-Aryan, Austroasiatic or isolate identification is established.

The next useful steps are independent photo verification, allograph sensitivity, family-aware splitting, contextual prediction by object class, and constrained comparison with appropriately licensed historical corpora. A decipherment claim should require fixed values that translate unseen material and predict independent archaeological or bilingual observations. Exhaustive acquisition and genuine decipherment remain open objectives.

## 6. Reproducibility and research disclosure

All reported experiments were executed locally. Core analytical scripts use Python's standard library; Pillow is optional for reference-image feature production and ReportLab for PDF export. Source revisions, hashes, filtering decisions, split groups, sampled null entropies, learned vectors, and test outputs are committed. Run scripts/reproduce.py --check to verify source hashes, tests, regenerated analytical outputs and the fixed numeric glyph input (exact structure and values, floating-point tolerance 1e-12). Fresh image acquisition/feature generation is a separate optional step. The methods ledger distinguishes executed, revised, and pending work. The PDF is generated from this Markdown source.

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

[10] Mukhopadhyay. Administrative interpretation of Indus inscriptions: archaeological and script-internal evidence. Humanities and Social Sciences Communications, 2023. https://www.nature.com/articles/s41599-023-02320-7

[11] Parpola. A Dravidian solution to the Indus script problem. 2010 lecture. https://www.harappa.com/sites/default/files/pdf/Parpola-2010-Coimbatore.pdf

[12] Mahadevan. The Indus Fish Swam in the Great Bath. Bulletin of the Indus Research Centre 2, 2011. https://www.harappa.com/content/indus-fish-swam-great-bath

[13] Rao et al. A Markov model of the Indus script. PNAS, 2009. Author-hosted paper: https://raw.githubusercontent.com/ronojoy/indus/cab6c2d881307825f24d7ed28f7ad62de800ae13/papers/MarkovModelIndusScript.pdf

[14] Raghavendra. On the Non-Specificity of Statistical Measures Used in Script Decipherment. 2026 arXiv preprint; peer-review status not established here. https://arxiv.org/abs/2608.02999

[15] Mahadevan. The Indus Script: Texts, Concordance and Tables. ASI Memoir 77, 1977. Postscript p.25, code/sign-list pp.30-35 and graphic-variant appendix pp.785-792 inspected. Public scan: https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan

[16] Arun G K. IVS repository, pinned source export/parser and codebook, revision 7c0273f544998178a4e4f71b80407c52d1ac2f24. https://github.com/gkarun876/IVS

[17] Joshi and Parpola. Corpus of Indus Seals and Inscriptions 1: Collections in India. 1987. Photographs pp. 1-3 and metadata pp. 365-366 inspected in public scan. https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan

[18] Knight et al. Unsupervised Analysis for Decipherment Problems. COLING-ACL 2006. https://aclanthology.org/P06-2065/

[19] Luo, Cao and Barzilay. Neural Decipherment via Minimum-Cost Flow: From Ugaritic to Linear B. ACL 2019. https://aclanthology.org/P19-1303/

[20] Ravi and Knight. Bayesian Inference for Zodiac and Other Homophonic Ciphers. ACL 2011. Selected homophonic/noisy-channel and type-update sections inspected. https://aclanthology.org/P11-1025/
