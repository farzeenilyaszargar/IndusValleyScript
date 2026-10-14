"""Generate an evolving research paper and concise results summary from outputs."""
import json
import statistics as S
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/'results'/f'{name}.json').read_text())

def main():
    d=read('descriptive')['ICIT'];models=read('sequence_models');null=read('entropy_nulls')
    g=read('grammar');fish=read('numeral_fish');slot=read('slot_control');site=read('site_transfer')
    latent=read('latent_grammar');near=read('near_copy')
    allograph=read('allograph_history')
    language=read('language_representation')
    stroke=read('stroke_count_constraints')
    correspondence=read('catalogue_correspondence')
    stroke_rows='\n'.join(f'| {f["sign"]} | {f["events"]} | '+
        ', '.join(f'{count}: {n}' for count,n in f['stroke_count_distribution'].items())+' |'
        for f in stroke['followers'] if f['support_at_least_5'])
    language_rows='\n'.join(f'| {name.replace("_"," ")} | {r["summary"]["conditional_bits"]["mean"]:.3f} | '
        f'{r["summary"]["order_constraint_bits"]["mean"]:.3f} | '
        f'{r["summary"]["absolute_conditional_entropy_distance"]["mean"]:.3f} |'
        for name,r in language['comparison'].items())
    mean=lambda order:S.mean(r[f'order_{order}']['test_bits_per_token_including_EOS'] for r in models)
    audit=json.loads((ROOT/'data/processed/audit.json').read_text())
    rows='\n'.join(f'| {r["seed"]} | {r["order_1"]["test_bits_per_token_including_EOS"]:.3f} | '
                   f'{r["order_2"]["test_bits_per_token_including_EOS"]:.3f} | '
                   f'{r["order_3"]["test_bits_per_token_including_EOS"]:.3f} | '
                   f'{100*r["mask_prediction"]["top1_rate"]:.1f}% | '
                   f'{100*r["mask_prediction"]["top5_rate"]:.1f}% |' for r in models)
    nullrows='\n'.join(f'| {kind.replace("_"," ")} | {null[kind]["mean"]:.3f} | '
                      f'{null[kind]["sd"]:.3f} | {null[kind]["p_monte_carlo"]:.3f} |'
                      for kind in ('within_text','global_frequency','length_position'))
    siteparagraph=' '.join(f'Holding out {name}, the unigram score is {r["unigram_bits"]:.3f} '
                          f'and bigram score {r["bigram_bits"]:.3f} bits/token on {r["test"]} distinct sequences.'
                          for name,r in site.items())
    paper=f'''# Structural Constraints in the Indus Sign System: A Reproducible Computational Investigation

Research draft, version 0.6 | 15 October 2026 | Not peer reviewed

Prepared with Codex for the IndusValleyScript research repository. This draft reports executed exploratory analyses. It is not a claim of decipherment or a human author's approved publication.

## Abstract

We investigate whether public Indus transcription data support reproducible constraints useful for eventual decipherment. A pinned ICIT-derived export supplies {audit['icit_raw_rows']:,} records, reduced to {d['texts']:,} distinct complete single-line sign sequences, {d['tokens']:,} tokens, and {d['signs']} observed sign IDs. We also audit a separate annotated CISI subset and index 715 verified glyph-reference files. Methods include entropy permutation controls, held-out n-gram models, positional templates, distributional embeddings, adjacency candidates, cross-site transfer, a morphology-based tally/fish test, and substitution invariance. Bigram models average {mean(2):.3f} bits/token versus {mean(1):.3f} for unigrams across five splits. Three permutation tests yield lower-tail Monte Carlo p=0.005. These results establish constraints relative to specified baselines, without identifying a language family, phonetic values, or translations. The work provides a falsifiable foundation and identifies data and external anchors needed for further progress.

## 1. Research question and prior work

The objective is to recover constraints that might assist decipherment while avoiding circular assignment of meanings. Previous n-gram research found directional and positional regularities and proposed missing-sign prediction [1]. Entropy comparisons argued for linguistic structure [2], while Sproat showed that structured nonlinguistic alternatives undermine simple classification by entropy [3]. Rao and colleagues subsequently framed their evidence as cumulative rather than conclusive [4]. Network approaches motivate sign-context analysis [5].

Semantic proposals require a separate evidential layer. Parpola's fish/star rebus program motivates a test of combinations but does not supply independently established values for this dataset [6]. Ration and transaction interpretations offer alternatives [7]. Image recognition can improve transcription without solving meaning [8]. A recent synthetic-baseline preprint motivates multiple controls and sensitivity audits, but its results are not treated as an independent validation of ours [9]. This project does not reproduce all experiments in those works.

## 2. Materials, provenance and representation

The main source is the public field-cady ICIT-derived CSV, pinned at commit 30308260d8da50151a79185c9e98404db9da331a. Its upstream attribution passes through Yajnadevam's Lipi repository; individual transcriptions have not been checked against seal photographs. Proposed Sanskrit strings, translations, interpretive classes, and notes are excluded using an explicit whitelist. Excluding these fields avoids direct label contamination but does not remove possible upstream transcription biases.

Eligibility requires a closed string of three-digit tokens delimited by plus signs, without unknown/separator IDs 000 or 999. Damaged or open-boundary strings and multiple lines are excluded. There are {audit['icit_eligible_rows']:,} eligible rows; exact sequence deduplication leaves {d['texts']:,}. The mean length is {d['mean_length']:.3f}, median {d['median_length']:.0f}, and maximum {d['max_length']}. This filter is conservative, not a guarantee of undamaged originals: unmarked uncertainties may remain.

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

Observed conditional entropy is {d['conditional_entropy_bits']:.3f} bits. Every sampled null entropy exceeds it. The length-position control makes fixed position alone an insufficient explanation under this permutation design. Artifact class, sites, allographs, related molds, and other latent factors may still explain part of the remaining dependence.

| Control | Mean bits | SD bits | Lower-tail p |
|---|---|---|---|
{nullrows}

Across five splits, bigrams improve prediction by {min(r['bigram_improvement_bits'] for r in models):.3f}-{max(r['bigram_improvement_bits'] for r in models):.3f} bits/token over unigrams. Each paired bootstrap interval excludes zero. Trigrams average {mean(3):.3f} bits/token and do not consistently improve over bigrams; we therefore find no robust predictive gain from this tested extra context. The splits overlap, so their five scores are not five independent discoveries.

| Seed | Unigram bits | Bigram bits | Trigram bits | Mask top 1 | Mask top 5 |
|---|---|---|---|---|---|
{rows}

Most-frequent-sign mask baselines range from 9.4 to 11.4 percent. For seed 42, the bigram improvement is {models[0]['bigram_improvement_bits']:.3f} bits/token, with bootstrap interval [{models[0]['bigram_improvement_bootstrap95'][0]:.3f}, {models[0]['bigram_improvement_bootstrap95'][1]:.3f}]. Reversing all sequences preserves substantial predictive gains, so statistical direction preference alone does not settle reading direction.

### 4.2 Controls and generalization

On the seed-42 sign-only task, unigram, independent slot, and bigram losses are {slot['unigram_bits']:.3f}, {slot['independent_slot_bits']:.3f}, and {slot['bigram_bits']:.3f} bits/sign respectively. Because the slot model knows length and scores only signs, these values should not be compared directly to the EOS-inclusive table. The slot model explains some predictability, while the tested bigram explains more.

{siteparagraph} Transfer does not establish universal grammar, since cataloguing conventions and shared artifact practices may also travel between sites.

A synthetic administrative slot generator, fitted to training-only positional distributions and supplied the observed lengths, yields conditional entropy 5.109 bits versus 3.892 observed. It fails to match adjacency and long repeats in this run. This rejects neither administration nor semasiography generally: the generator intentionally lacks local dependency, and synthetic duplicate records are retained for the descriptive comparison.

### 4.3 Candidate grammar, collocations and morphology

The seed-42 empirical role grammar covers {100*g['test_exact_template_coverage']:.1f} percent of held-out sequences, versus {100*g['shuffled_test_template_coverage']:.1f} percent of a single within-text shuffle. Coarse rare/flexible classes allow substantial coverage; this is not grammatical validation. There are 163 train-selected adjacency candidates, and 47 distinct five-sign subsequences recur across distinct complete texts. Such units could be names, formulae, codes, or other combinations.

In the clean CISI subset, {fish['observed_tally_then_fish']} simple-stroke-before-fish adjacencies occur, versus mean {fish['null_mean']:.3f} under the shuffle control, with upper-tail p={fish['p_upper']:.3f}. This is compatible with constrained number-like/fish combinations. It cannot distinguish fish as stars, commodities, identity markers, or components of words. No sound value or translation follows from this test.

### 4.4 A negative result for unconstrained substitution

Ten different bijective assignments of abstract syllable labels preserve conditional entropy exactly, to numerical precision. For 637 distinct labels there are 637! possible bijections, about 10^1511.4. This is a label-invariance demonstration, not a count of historically viable languages. It establishes that frequency and adjacency statistics alone cannot select the actual label meanings. A configured numerical grammar is achievable; recovery of the historical spoken language requires additional constraints.

### 4.5 Hidden-state grammar: a negative predictive result

Validation selects {latent['selected']['states']} states, initialization seed {latent['selected']['initialization_seed']}, and {latent['selected']['iteration']} EM iterations. Its test loss is {latent['hmm_test_bits']:.3f} bits/token, compared to {latent['bigram_test_bits']:.3f} for the validation-selected bigram. HMM improvement is {latent['hmm_vs_bigram']['improvement_bits']:.3f} bits/token, with grouped bootstrap interval [{latent['hmm_vs_bigram']['bootstrap95'][0]:.3f}, {latent['hmm_vs_bigram']['bootstrap95'][1]:.3f}]. Thus the tested compact HMM family performs worse. This does not reject all latent grammars or linguistic interpretations; the parameterization, priors, training duration and short texts constrain the test. The chosen state count lies at the largest tested value, so the experiment does not establish an optimal state count. Exported emissions and posterior positional profiles are structural descriptions, not deciphered categories.

### 4.6 Near-copy robustness

In the original seed-42 split, {near['original_test_with_train_neighbour']} of {near['original_test_eligible_length_at_least_3']} test texts of length at least three ({100*near['original_test_neighbour_fraction']:.1f} percent) have a one-sign neighbour in training. The new graph has {near['components']:,} connected components; the largest contains {near['largest_component']} canonical sequences. Component splitting produces {near['train_texts']:,} training, {near['validation_texts']} validation, and {near['test_texts']} test texts.

On this new holdout, unigram loss is {near['scores']['1']['test_bits']:.3f} and bigram loss {near['scores']['2']['test_bits']:.3f} bits/token. Improvement is {near['bigram_improvement']['improvement_bits']:.3f}, with component-bootstrap interval [{near['bigram_improvement']['bootstrap95'][0]:.3f}, {near['bigram_improvement']['bootstrap95'][1]:.3f}]. Prediction gains therefore survive this conservative similarity grouping. The change from the earlier score is not a causal measurement of leakage, since holdout size and composition differ. The comparison does not remove relationships between unequal-length texts or establish actual archaeological independence.

### 4.7 Annotated allograph history: no observed predictive gain

Experiment 003 validates the custom feature vectors of all {allograph['eligible_objects']} eligible CISI objects against the source schemas. These objects contain {allograph['sign_tokens']} sign occurrences, {allograph['base_ids']} base IDs, and {allograph['variant_ids']} distinct base-ID/custom-morphology combinations. Default damage, line and uncertainty values are excluded from variant identity. The full variant inventory, integer encodings, descriptions, custom schemas and object references are exported separately; variants are not assumed to be independent graphemes.

Both prediction models target the same next base sign. The alternative uses only the preceding sign's morphology and interpolates to a base bigram when a variant history is sparse or unseen. It never uses the target's own morphology to predict that target. Base and variant strengths are validation-selected from 1/5/20/100, with exact/reversed base duplicates sharing partitions. Eligible object occurrences are retained, unlike the earlier deduplicated CISI summary.

Across five small holdouts of ten canonical groups, variant-history improvements range from {min(r['variant_improvement']['improvement_bits'] for r in allograph['runs']):.3f} to {max(r['variant_improvement']['improvement_bits'] for r in allograph['runs']):.3f} bits/token, averaging {S.mean(r['variant_improvement']['improvement_bits'] for r in allograph['runs']):.3f}. All five point estimates favour base bigrams, while four confidence intervals overlap zero. This supplies no positive predictive support for this representation. It does not prove the variants have identical meanings or sounds: variant histories are sparse, and the sample is geographically narrow. The five holdouts overlap, so they are not five independent negative discoveries. Sound assignments or sign merging would require independent epigraphic and linguistic evidence.

### 4.8 Language-proxy representation sensitivity

Experiment 004 uses ten seeded matched-length samples for each of four conditions: Tamil words, Tamil letter-plus-mark clusters, Sanskrit words, and Sanskrit letter-plus-mark clusters. Every sample contains the exact Indus length list, 2,156 snippets and 9,221 tokens. A document eligible for each length is chosen uniformly, then a contiguous window is chosen uniformly, with replacement. No window crosses a document. Tamil documents are individual verses; Vedic documents are sentence blocks, using all upstream splits for descriptive sampling rather than predictive evaluation. Word/cluster normalization and source hashes are fixed before execution. Letter clusters group a Unicode base letter with following marks; they are not full extended grapheme clusters, phonetic syllables, or Sanskrit aksharas. Word separators are omitted from the cluster stream. Translations and semantic annotations do not supply Indus values.

| Proxy and unit | Mean H conditional | Mean shuffle-minus-real | Distance to Indus H |
|---|---|---|---|
{language_rows}

All scores are in bits; Indus H conditional is {language['indus']['conditional_bits']:.3f}, and its matched 49-shuffle-minus-real value is {language['indus']['order_constraint_bits']:.3f}. Ranking by mean absolute conditional-entropy distance selects {language['nearest_proxy_by_representation']['words'].replace('_',' ')} for word units and {language['nearest_proxy_by_representation']['letter_marks'].replace('_',' ')} for letter-plus-mark units. The rank reversal is a negative result for using this single distance as a language identifier. The apparent winner depends on representation even with equal text lengths and token totals.

The sampled vocabulary sizes differ substantially: about 6,677 Tamil word types, 4,409 Sanskrit word types, 202 Tamil cluster types and 36 Sanskrit cluster types, versus 637 Indus sign types. Sparse word counts force low empirical conditional entropy even in frequency-preserving shuffles, illustrating estimator bias rather than low true language entropy. Sampling also produces duplicates: mean counts range from about 9 Tamil word windows to 363 Sanskrit cluster windows. Samples are not deduplicated because exact length matching is the declared design; overlap and document reuse remain limitations. The Vedic pool includes multiple citation texts and strata, not exclusively Rigvedic verse. The 49 shuffled trials have p-value resolution 0.02 and are descriptive controls, not decisive linguistic evidence. No language-family assignment, sign/word equivalence or phonetic key follows from the comparison.

### 4.9 Graphic stroke-count constraints and interpretive ambiguity

Experiment 005 examines described stroke counts rather than treating arbitrary sign IDs as values. We map only catalogue groups P121-P130 to one through ten short strokes, and P144/P145/P147/P150/P151 to one through five tall strokes. This represents catalogue morphology, not independently proven numeral values. Height remains distinct. The 91 complete deduplicated CISI texts contain {stroke['all_tally_slots']} such slots; 11 tally-before-tally and three terminal cases are excluded from the following-sign test, leaving {stroke['all_counts_association']['events']} events. The slot records retain object IDs, position and following-sign morphology for later epigraphic audit.

Mutual information between described count and following base-sign ID is {stroke['all_counts_association']['mutual_information_bits']:.3f} bits, compared to a mean {stroke['all_counts_association']['null_mean_bits']:.3f} under 999 count-label permutations restricted by height and coarse initial/medial position. The upper-tail p-value is {stroke['all_counts_association']['p_upper']:.3f}, or {stroke['all_counts_association']['bonferroni_two_tests_p']:.3f} after correcting the two prespecified tests. Short strokes alone yield {stroke['short_only_association']['mutual_information_bits']:.3f} bits vs null mean {stroke['short_only_association']['null_mean_bits']:.3f}, adjusted p={stroke['short_only_association']['bonferroni_two_tests_p']:.3f}. Sparse followers inflate empirical mutual information, so the excess over the matched null, rather than the raw score alone, matters. Slot-level exchangeability is assumed; this does not control every object-family or archaeological dependency.

The only three followers represented at least five times all admit multiple described counts:

| Following sign | Events | Described count: frequency |
|---|---|---|
{stroke_rows}

P004 is described as a burden-carrying person, P050 as a plain fish, and P086 as a branching tree form. These are visual descriptions, not commodity names. The observed combinations exhibit count/follower constraints under the specified null, but do not establish either unrestricted quantities or one fixed value per category. The test is motivated by competing administrative, ration and astronomical interpretations, including Mukhopadhyay's discussion of restricted number/sign combinations [10]. It does not replicate that paper's exact catalogue classes or refute a proposed reading: a verified glyph crosswalk and larger independently reviewed sample are missing.

Most importantly, no independent commodity amounts, matched weights or metrological scale are available for these objects. The experiment therefore cannot calibrate a unit, prove that three strokes mean the number three, or translate a fish sign as a star, gemstone, commodity, or personal-name element. Its contribution is an auditable morphological constraint table and specific combinations to check against independent evidence.

### 4.10 Paired-object catalogue correspondence

Experiment 006 strictly joins first-face Mohenjo-daro catalogue IDs to uniquely labeled ICIT-export objects, requiring both transcriptions to be complete single-line strings of equal length. Of 179 candidate objects, {correspondence['accepted_pairs']} pairs are accepted and {correspondence['rejected_count']} excluded: 87 Parpola-ineligible, five length mismatches and two ICIT-ineligible. Equal length does not prove equal segmentation or object/face identity. Grouping connects exact/reversed strings in either catalogue, retaining repeated texts within partitions. Seed 42 produces 67 training, nine validation and nine test objects.

On training positions, H(Parpola ID | ICIT ID) is {correspondence['orientation_train_entropy']['direct']:.3f} bits for direct alignment and {correspondence['orientation_train_entropy']['reversed']:.3f} when reversing the ICIT sequence. Reversed alignment is selected using training data alone. This is relative source-order evidence for these matched objects, not global photographic verification of reading direction. The earlier main-corpus positional results still refer to stored ICIT order, and have not been automatically reinterpreted as prefixes or suffixes.

The learned majority correspondences correctly predict {correspondence['validation']['correct_positions']}/{correspondence['validation']['positions']} validation positions and {correspondence['test']['correct_positions']}/{correspondence['test']['positions']} test positions ({100*correspondence['test']['top1_rate_all_positions']:.1f} percent including unseen-ID failures). Source-ID coverage is {100*correspondence['test']['known_coverage']:.1f} percent on test data; {correspondence['test']['whole_sequences_correct']}/9 whole test sequences are correct. Known-source-only probabilistic loss is {correspondence['test']['known_source_logloss_bits']:.3f} bits/position using fixed additive 0.5 smoothing over training targets plus UNK; unknown target IDs collapse for this score. It does not measure translations.

The shortlist contains {correspondence['review_priority_count']} training-derived review-priority correspondences, requiring at least three occurrences on two objects and >=90 percent agreement. Conflicting rows and unsuccessful objects remain in the output. Namespaces remain separate: no candidate mapping is treated as an independently glyph-verified equivalence, propagated to all inscriptions, or given a sound/meaning. Shared catalogue ancestry, source transcription errors, the face-ID assumption, small holdout and excluded segmentation disagreements limit independence. The result provides a reproducible path toward catalogue reconciliation needed before constrained interpretation.

## 5. Limitations and implications for decipherment

The main dataset is a secondary public export. No new glyph transcription, full catalogue reconciliation, artifact-family grouping, or independent translation anchor has been established. Splitting reverse/exact copies does not eliminate all near-duplicate or formula leakage. Allograph distinctions may inflate the vocabulary and hapax rate ({100*d['hapax_fraction']:.1f} percent in the main subset). The complete-only filter selects against difficult inscriptions and may bias inference. Rare sign embeddings and small CISI morphology counts are unstable.

The models establish conditional predictability under declared controls. They cannot determine whether that structure encodes phonology, names, quantities, transactions, or a mixture. Fitting an unconstrained rebus or a surname list would risk selecting the desired answer through researcher flexibility. Later Tamil and Sanskrit proxies have now been compared structurally under fixed representation choices; no Proto-Dravidian, Indo-Aryan, Austroasiatic, or isolate phonetic mapping has been tested on historically matched, independently held-out language corpora in this release.

The next useful steps are independent photo verification, allograph sensitivity, family-aware splitting, contextual prediction by object class, and constrained comparison with appropriately licensed historical corpora. A decipherment claim should require fixed values that translate unseen material and predict independent archaeological or bilingual observations. Exhaustive acquisition and genuine decipherment remain open objectives.

## 6. Reproducibility and research disclosure

All reported experiments were executed locally. Scripts use Python's standard library for acquisition and analysis; ReportLab is optional for PDF export. Source revisions, hashes, filtering decisions, split groups, sampled null entropies, learned vectors, and test outputs are committed. Run scripts/reproduce.py --check to verify source hashes, tests and regenerated analytical outputs (exact structure and values, floating-point tolerance 1e-12). Fresh acquisition is a separate optional network step. The methods ledger distinguishes executed, revised, and pending work. The PDF is generated from this Markdown source.

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
'''
    (ROOT/'docs/PAPER.md').write_text(paper)
    summary=f'''# Results snapshot

15 October 2026. No decipherment claimed.

- Corpus: {d['texts']:,} clean distinct sequences, {d['tokens']:,} tokens, {d['signs']} IDs.
- Inventory: 715 verified remote glyph references; 395 separate Parpola descriptions.
- Mean held-out scores: unigram {mean(1):.3f}, bigram {mean(2):.3f}, trigram {mean(3):.3f} bits/token (including EOS; unseen signs collapsed to UNK).
- Mask top-1: 29.0-35.5%; top-5: 52.1-57.5%; frequent-sign top-1 baseline: 9.4-11.4%.
- Entropy: {d['conditional_entropy_bits']:.3f} bits; all three permutation p-values 0.005 (199 trials each).
- Simple tally/fish adjacency: {fish['observed_tally_then_fish']} vs null mean {fish['null_mean']:.3f}, exploratory p={fish['p_upper']:.3f}.
- Role-template held-out coverage: {100*g['test_exact_template_coverage']:.1f}%; single-shuffle coverage {100*g['shuffled_test_template_coverage']:.1f}%.
- Ten abstract substitutions preserve entropy: no phonetic or semantic key identified.
- Validation-selected HMM: {latent['hmm_test_bits']:.3f} vs bigram {latent['bigram_test_bits']:.3f} bits/token; the tested HMM is worse.
- Near-copy component holdout: unigram {near['scores']['1']['test_bits']:.3f}, bigram {near['scores']['2']['test_bits']:.3f} bits/token; grouped gain {near['bigram_improvement']['improvement_bits']:.3f} with 95% interval [{near['bigram_improvement']['bootstrap95'][0]:.3f}, {near['bigram_improvement']['bootstrap95'][1]:.3f}].
- Allograph audit: {allograph['variant_ids']} morphology-coded variants of {allograph['base_ids']} base IDs in {allograph['eligible_objects']} clean annotated objects. Previous-variant histories did not improve next-base-sign prediction in five small holdouts.
- Language-proxy rank reversal: conditional-entropy distance selects Sanskrit with word units and Tamil with letter-plus-mark units under matched lengths/token totals. This method cannot justify a family identification. Opaque derived samples and attribution are packaged for offline reproduction.
- Described stroke counts depend on followers under height/position-preserving controls (two-test-adjusted p=0.004/0.008). All three followers with at least five events admit multiple counts. Graphic counts are not proven numerical values; no metrological scale or sign meaning is established.
- Paired-object catalogue integration: 85 usable pairs; training selects reversed relative alignment. Held-out majority correspondence accuracy 31/39 positions, 82.1% source-ID coverage, 29 candidate mappings for glyph review. These are catalogue labels, not sound assignments.

Full methods and limitations are in docs/PAPER.md and docs/METHODS.md. Results are structure, not translations.
'''
    (ROOT/'results/SUMMARY.md').write_text(summary)
    print('Generated paper and summary from executed outputs.')

if __name__=='__main__':main()
