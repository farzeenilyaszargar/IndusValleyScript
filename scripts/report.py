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
    glyph=json.loads((ROOT/'data/processed/glyph_morphology.json').read_text())
    meta=read('metadata_conditioning')
    fish_audit=read('fish_rebus_audit')
    uncertainty=read('uncertainty_sensitivity')
    gaps=read('gap_reconstruction')
    administrative=read('administrative_control')
    mahadevan=read('mahadevan_primary_audit')
    motif=read('motif_prediction')
    refs=read('reference_candidates')
    graphic=read('graphic_variant_audit')
    motif_rows='\n'.join(f'| {name} | {m["bits_per_row"]:.3f} | {100*m["accuracy"]:.1f}% | {100*m["macro_recall_present_classes"]:.1f}% |'
        for name,m in (("metadata baseline",motif['baseline']),("metadata plus signs",motif['sign_augmented'])))
    admin_rows='\n'.join(f'| {seed} | {r["description"]["signs"]} | {r["within_text_null"]["observed_bits"]:.3f} | '+
        f'{r["evaluation"]["order_1"]["test_bits_per_token_including_EOS"]:.3f} | {r["evaluation"]["order_2"]["test_bits_per_token_including_EOS"]:.3f} | '+
        f'{100*r["evaluation"]["mask_prediction"]["top1_rate"]:.1f}% |'
        for seed,r in administrative['realizations'].items())
    gap_rows='\n'.join(f'| {length} / {name} | {m["summary"]["masks"]} | {100*m["summary"]["whole_top1"]:.1f}% | {100*m["summary"]["whole_top5"]:.1f}% |'
        for length,r in gaps['lengths'].items() for name,m in r['models'].items())
    two_gap=gaps['lengths']['2']
    two_summary=two_gap['models']['bigram']['summary']
    two_gain=two_gap['paired_top1_gain']
    uncertainty_rows='\n'.join(f'| {name} | {r["training_objects"]} | {r["test_bits"]:.3f} | '+
        f'{r["clean_baseline_improvement"]["improvement_bits"]:.3f} |'
        for name,r in uncertainty['conditions'].items())
    meta_rows='\n'.join(f'| {kind} | {m["test_bits"]:.3f} | {m["paired_improvement"]["improvement_bits"]:.3f} | '+
        f'{m["matched_smoothing_ablation"]["metadata_increment"]["improvement_bits"]:.3f} |'
        for kind,m in meta['models'].items())
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

Research draft, version 0.16 | 17 October 2026 | Not peer reviewed

Prepared with Codex for the IndusValleyScript research repository. This draft reports executed exploratory analyses. It is not a claim of decipherment or a human author's approved publication.

## Abstract

We investigate whether public Indus transcription data support reproducible constraints useful for eventual decipherment. A pinned ICIT-derived export supplies {audit['icit_raw_rows']:,} records, reduced to {d['texts']:,} distinct complete single-line sequences, {d['tokens']:,} tokens and {d['signs']} sign IDs. A separate annotated CISI subset supports morphology and correspondence audits. We index 715 glyph-reference files and acquire 3,916 official Mahadevan records with raw uncertainty/layout metadata and 417 separate sign-list references, supplemented by 641 original graphic forms and two postscript signs. Of 2,742 secondary sequences matching primary base codes, 265 strip doubtful readings and 92 concatenate lines. Methods include entropy controls, held-out sequence models, masked reconstruction, positional/context representations and controlled language/administrative comparisons. Bigrams average {mean(2):.3f} bits/token versus {mean(1):.3f} for unigrams across five splits; synthetic two-sign gaps are recovered at top1 in 12.7%. A richer explicitly non-phonetic administrative generator also supports masked prediction and bigram gains. These results establish structural constraints and source-quality limits, without identifying a language family, sound values or translations. Independent semantic and archaeological anchors remain necessary for decipherment.

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

### 4.11 Reference-glyph screening and numerical morphology

Experiment 007 screens the 29 shortlisted reference glyphs against their supplied Parpola shape descriptions. This is Codex-assisted review of standardized catalogue drawings, not blinded expert review or examination of original-object photographs. Broad shapes are compatible with the descriptions, while the 002 short/tall-stroke conflict, the rounded/angular 817/861 variants grouped under P385, and the uncertain asymmetric-animal label remain unresolved. No candidate is promoted to an independently verified equivalence or assigned a sound or semantic value.

All {glyph['images']} pinned reference images were acquired into private local cache. Source URLs and SHA-256 hashes are preserved. Scalar numeric descriptors encode thresholded ink bounding-box aspect, ink density, centroid, second moments and eight-connected component counts. Image assets, fonts and reconstructible pixel grids are not packaged. These features describe rendering morphology; cropping, antialiasing, stylistic choices, crossings and gaps can affect them. They are not learned linguistic or semantic embeddings.

The six already screened simple-stroke examples produce component counts 1, 2, 3, 4, 1 and 3 for IDs 001, 002, 003, 004, 031 and 033, matching their described shapes. Two independent synthetic-mask tests check connectivity and translation invariance. The source-derived matches validate extraction only, not discovery of numerical values. Optional Pillow-based production can reacquire/hash-check the images; default offline reproduction validates the committed numerical snapshot's hash and arithmetic invariants rather than regenerating image features. Original-object and catalogue provenance verification remains necessary before interpretation.

### 4.12 Metadata-conditioned formula models and smoothing sensitivity

Experiment 008 retains all {meta['eligible_rows']} eligible artifact rows with their metadata, grouping exact/reversed texts before partitioning. Seed 42 yields {meta['train_rows']} training, {meta['validation_rows']} validation and {meta['test_rows']} test rows. Duplicates remain weighted as observed occurrences, so these scores are not directly comparable to the earlier deduplicated benchmark. Metadata conditions use the literal type prefix, site, or their combination, and back off to pooled bigrams. Both smoothing strengths are selected on validation data from 1/5/20/100. Target signs, speculative translations and interpretive classes are excluded from metadata.

| Metadata condition | Test bits/token | Gain vs selected pool | Gain at matched smoothing |
|---|---|---|---|
{meta_rows}

The validation-selected pooled benchmark scores {meta['pooled']['test_bits']:.3f} bits/token. Site-plus-type gains 0.079 bits/token, with grouped 98.33 percent interval [0.013, 0.151] as a three-comparison sensitivity. However, the metadata models select pooled strength 100 while the pooled benchmark selects 20. An exploratory matched-strength ablation, added after initial scores without reselecting models, reduces the type and site-plus-type increments to 0.015 and 0.034 bits/token. Their 95 percent intervals [-0.059, 0.081] and [-0.020, 0.088] overlap zero. Site-only conditioning is worse at matched smoothing (increment -0.079, interval [-0.149, -0.021]). Thus the nominal aggregate gain is partly attributable to smoothing differences; this test does not establish a robust independent metadata contribution.

Confidence intervals resample whole exact/reversed groups (1,000 draws); related molds, near copies and uncertain type annotations are not fully controlled. Test rows are dominated by 159 seals and 94 tablets, with other categories much smaller. Archaeological usage differences remain plausible, but these fitted formulas do not decode commodities, names, dialects or grammatical parts of speech. Metadata and transcription quality require further review before interpreting a single reconstructed grammar across object classes.

### 4.13 Published fish-rebus witnesses and conditional readings

Experiment 009 examines selected published astronomical proposals [11] and their critique [12]. H-9's exported stored string is 220-017: a plain-fish reference followed by seven-stroke morphology, matching the graphic example named by Parpola. M-112 contains 220-016 in the export, but its annotated CISI transcription contains P126 followed by P056, a modified fish rather than P050. Damage/uncertainty elsewhere excludes this object from the earlier clean CISI subset. Thus the absence of six/plain-fish there cannot be used to reject the published example; eligibility and sign-subtype disagreement must be reported first. These are retrospective named-witness checks, not independent discoveries or original-object photo verification.

For the larger complete unique diagnostic subset, provisional short-stroke reference aliases yield {fish_audit['complete_unique_diagnostic']['fish_slots']} plain-fish/stroke slots. Their described counts are 1 (2), 2 (10), 3 (14), 4 (6), 6 (10), and 7 (1). The published-example count set 3/6/7 occurs in {fish_audit['complete_unique_diagnostic']['fish_3_6_7_slots']}/43 fish slots versus {fish_audit['complete_unique_diagnostic']['other_3_6_7_slots']}/{fish_audit['complete_unique_diagnostic']['other_slots']} other-follower slots. An exploratory count-label permutation gives upper-tail p={fish_audit['complete_unique_diagnostic']['p_upper']:.3f}; opposite stored adjacency gives p={fish_audit['opposite_order_diagnostic']['p_upper']:.3f}. This diagnostic assumes slot exchangeability, provisional reference-code correspondences and a declared stored-order convention. The count-set enrichment is our operational extension, not a claim that the published theory restricts every fish sequence to those counts. It supports a restricted graphic combination, not a constellation, number value or language family.

The audit includes an explicit conditional rendering of H-9 under Parpola's proposed fish/star rebus: if the strokes mean seven and the fish sign represents proposed miin/star, the author's eZu-miin reading refers to seven stars/Ursa Major [11]. This is a published hypothetical phonetic/semantic assignment, not a deciphered value adopted by this project. An unknown quantity/classifier template and an unknown category/rate template admit precisely the same two graphic tokens. No independent semantic label, measurement or bilingual identifies which interpretation is correct. The alternatives remain unresolved, and a plausible lexical parallel alone is insufficient to translate the inscription.

### 4.14 Uncertainty-sensitive training and source-agreement limits

Experiment 010 keeps the clean seed-42 validation/test objects fixed and varies only training eligibility. All broader objects have nonempty single-line transcriptions and no P000 unknown stretch; exact/reversed clean holdout copies and object IDs are excluded from additions. The intermediate condition limits each literal raw damage and uncertainty code to 25. This is not a calibrated percentage: damage codes can encode locations in higher digits. The broad condition retains all remaining damage/uncertainty-marked readings as transcription hypotheses, not known truths. Bigram smoothing is selected on the same clean validation set.

| Training condition | Objects | Clean-test bits | Gain vs clean |
|---|---|---|---|
{uncertainty_rows}

Adding 25 intermediate-filter objects gives a 0.052-bit improvement with grouped 95 percent interval [-0.095, 0.230]. Adding 62 broader objects gives 0.047 bits, interval [-0.234, 0.329]. Both intervals overlap zero, and unseen clean-test token counts decrease from seven to five. The modest point gains may reflect coverage rather than correctness of uncertain readings. Ten canonical test groups are too few for strong conclusions, and guessed/damaged transcriptions cannot be promoted to accepted data merely because a predictor uses them.

A separate equal-length paired-source audit accepts {uncertainty['source_consistency']['accepted_pairs']} objects and examines {uncertainty['source_consistency']['aligned_positions']} reversed aligned positions against supplied Wells alias lists. It finds {uncertainty['source_consistency']['alias_absences']} alias-absence positions; {uncertainty['source_consistency']['zero_annotation_alias_absences']} have zero local damage and uncertainty codes. M-112's plain/modified fish disagreement is among these unmarked positions. Alias absence can reflect incomplete crosswalks, variant splitting or transcription differences; it is not automatically an error. The result shows that annotation filters alone do not establish cross-corpus agreement. Original-object/face and glyph verification remains an independent requirement before assigning phonetic values or interpreting inferred grammar.

### 4.15 Exact reconstruction of contiguous sign gaps

Experiment 011 extends synthetic masking to every contiguous one- or two-sign span of complete seed-42 held-out ICIT strings. Exact/reverse copies share partitions. Ordinary validation sequence loss selects bigram smoothing {gaps['bigram_strength']}; neither masked targets nor test-neighbor strings inform candidate selection. Every actual training sign is allowed, excluding EOS/UNK. Exhaustive fillings are scored with left, internal and right transitions and normalized over that closed inventory. The unigram baseline has the same inventory and gap lengths. One-sign results exactly reproduce the earlier diagnostic. This follows the missing-sign prediction rationale reviewed in the Markov literature [13]; it is an independent benchmark, not a replication of published restoration claims.

| Gap length / model | Masks | Whole-gap top1 | Whole-gap top5 |
|---|---|---|---|
{gap_rows}

For two-sign gaps, the best bigram filling has {100*two_summary['top1_token_accuracy']:.1f}% token accuracy; the entire true gap is in the training inventory in {100*two_summary['whole_truth_in_training_vocabulary']:.1f}% of masks. The whole-gap top1 advantage over unigrams is {100*two_gain['difference']:.1f} percentage points, grouped 95 percent interval [{100*two_gain['interval95'][0]:.1f}, {100*two_gain['interval95'][1]:.1f}]. Bootstrap resampling keeps overlapping masks within each of {two_gain['groups']} canonical inscription groups. All test targets, including unseen signs, remain in the accuracy denominator.

Mean top1 conditional probability for two-sign bigram fillings is {100*two_summary['mean_top1_conditional_probability']:.1f}%. Fixed posterior-bin observed accuracies and per-mask top-five candidates are exported for audit. These probabilities assume a known gap length and a closed candidate inventory; they omit unseen glyph possibilities and must not be interpreted as archaeological certainty. Synthetic masked truth is a secondary transcription, not independently verified glyph evidence. No completion of 000 unknown stretches is produced because their cardinality is unknown, and no recovered integer code acquires a phonetic or semantic value.

### 4.16 Richer administrative compatibility control

A recent preprint describes a purpose-built non-phonetic emblem system and stresses the specificity limits of structural measures [14]. We inspected selected construction, prediction and limitations passages, but could not retrieve its corpus from the checked article/source archive and repository searches. Its published results are not reproduced here. Experiment 012 is an independently authored control with declared parameters.

Our fictional inventory has 160 institutions, 96 guilds, 160 commodities, eight quantity emblems, four ranks and five validators. Optional institution, guild/rank, quantity/commodity and validation blocks match the exact Indus length list. Fixed institution/guild and guild/commodity licenses and preferred rank/quantity pairs induce dependencies; every token retains its semantic role and value. Only lengths are empirically matched: no Indus sign frequencies or transitions tune this generator, and no sounds or dictionary enter generation. Three seeds produce 2,156 records and 9,221 tokens each. Generated duplicates remain weighted, with exact/reversed copies kept within split groups; model smoothing is validation-selected using our established EOS/UNK benchmark.

| Seed | Types | Conditional bits | Unigram bits | Bigram bits | Mask top1 |
|---|---|---|---|---|---|
{admin_rows}

Every realization rejects its own within-text shuffle at the minimum possible p=0.010 with 99 trials, and every grouped unigram-to-bigram gain interval excludes zero. Mask prediction also exceeds each realization's frequent-sign baseline. Thus conditional predictability and shuffle rejection occur in a notation generated without phonetic values. The richer control repairs a limitation of the earlier independent-slot simulation: institutional licenses create local dependencies rather than merely different positional frequencies.

This is a compatibility demonstration, not a calibrated linguistic/non-linguistic classifier or a reconstruction of Harappan administration. Its vocabulary and duplicate frequencies differ from the real corpus; near-copy families are not separated, and three seeds sample one chosen architecture rather than all plausible alternatives. It does not show that Indus signs are non-linguistic, nor assign an institution, commodity, quantity or sound to any Indus ID. Structural gains alone remain insufficient to configure a historically justified spoken-language reading.

### 4.17 Primary Mahadevan acquisition, signs and annotation preservation

Experiment 013 acquires the official Indus Research Centre/RMRL application's public archaeological collection through paginated reads. The frozen whitelist snapshot contains {mahadevan['primary_rows']} records, including {mahadevan['text_rows']} nonempty text rows. Raw S1-S14 strings, doubtful asterisks, gaps, combined side/line codes, directions, object/field-symbol codes and locus/level metadata are retained with source update times and page hashes. Pagination is not an atomic historical database snapshot; offline results refer only to the committed frozen copy. No proposed sound mappings enter acquisition.

The original printed code tables and four sign-list pages were visually checked in the 1977 source [15]. Codes 4/5/9 denote vertical/symmetric/doubtful arrangements, respectively; a secondary codebook shifts those labels. The 417 original sign-list IDs now have separate integer tokens and page-linked glyph references. They are not merged into Parpola or Wells IDs, and raster book pages are not redistributed. A zero denotes an illegible stretch of unknown cardinality, mapped to a reserved unknown slot rather than a sign or padding; doubtful readings retain both base ID and uncertainty flag.

All {mahadevan['secondary_comparison']['counts']['same_base_sequence']} secondary sequences [16] match a side-specific reconstruction of primary base IDs. However, {mahadevan['secondary_comparison']['rows_with_stripped_doubtful_tokens']} lose doubtful marks and {mahadevan['secondary_comparison']['rows_concatenating_primary_lines']} concatenate multiple primary lines. Primary records contain {mahadevan['doubtful_tokens']} doubtful tokens in total. Thus matching base codes does not certify clean text or preserve layout. The secondary export remains an audit comparator, not ground truth.

A declared strict screen retains {mahadevan['strict_singleline_rows']} single-line rows with {mahadevan['strict_observed_ids']} IDs and {mahadevan['strict_canonical_texts']} distinct exact/reverse canonical strings. It excludes gaps, doubtful signs, nonhorizontal/uncertain arrangements, count inconsistencies and unresolved layouts. All 417 IDs occur somewhere in the raw snapshot. This is acquisition and numerical encoding, not a new modeling result, face-verified crosswalk or semantic anchor. Original-object verification and controlled tests of the new corpus remain separate work.

### 4.18 Face-preserving field-symbol prediction

Experiment 014 uses strictly screened primary lines with their own field-symbol metadata. Before target filtering, rows sharing a source object number or exact/reversed sign string form connected components. This links all faces, including rows later excluded for target codes 0/999. There are {motif['all_components']} components among 2,391 strict rows. Component-count splitting yields 1,427/787/177 rows; the largest component has 592 rows and lies wholly in validation, contributing 96 target rows. This large transitive group makes validation composition uneven and is retained rather than split to improve the score.

After literal target-code exclusions, training/validation/test have {motif['split_rows']['train']}/{motif['split_rows']['validation']}/{motif['split_rows']['test']} rows. Exact codes with at least 20 distinct training objects remain separate; others become RARE. Target classes are raw codes, not animal-name glosses. The baseline interpolates site/object-type/length-bin class counts to pooled class priors. Validation selects strength {motif['selected_baseline_strength']}; this stays fixed when training-only distinct-sign likelihoods are added. Validation chooses sign weight {motif['selected_sign_weight']}, with zero weight available as an ablation. No hidden target field enters the sign predictor.

| Model | Test bits/row | Accuracy | Macro recall |
|---|---|---|---|
{motif_rows}

The paired log-loss gain is {motif['paired_gain']['improvement_bits_per_row']:.3f} bits per archaeological row, with connected-component 95 percent interval [{motif['paired_gain']['interval95'][0]:.3f}, {motif['paired_gain']['interval95'][1]:.3f}] across {motif['paired_gain']['groups']} test groups. The interval includes zero, while accuracy and macro recall both decrease. Always selecting the training-majority code scores {100*motif['majority_accuracy']:.1f}% accuracy. Code 13 supplies 67/99 test rows; neither model correctly predicts any of the four other individually retained codes in this small test set. Five test metadata strata are unseen and {motif['unknown_test_sign_tokens']}/{motif['test_sign_tokens']} sign tokens are outside the training inventory.

This tested predictor does not establish an independent iconographic/semantic anchor or disprove all sign/motif associations. RARE combines heterogeneous targets, class imbalance is strong, one large group influences validation, and near-copy/mold-family independence remains unresolved. Connected splits, class-wise confusions, probability vectors and all validation candidates are exported. A sign could covary with motif through institutional or production conventions rather than name the depicted entity; no phonetic or lexical assignment follows.

### 4.19 Reference-number candidates and original photographs

Experiment 015 reads the original CISI 1 metadata page for M-1 through M-100 [17]. The book warns that Finnish concordance (FC) and Mahadevan reference numbers are not uniformly interchangeable. Consequently a matching FC/Mahadevan number is used only to generate a candidate transcription pair, not to establish an independently verified object identity. One uncertain numeric reading is flagged; no supplied sign alias selects or filters the pairs. An M-1 pilot and its aliases were inspected before design, so its whole duplicate group is forced into training.

Eligibility requires a unique Parpola A-face transcription and a strict primary Mahadevan side-0/line-0 record with the same candidate number and length. Of 100 references, {refs['accepted_numeric_candidates']} survive; exclusions are 45 Parpola-ineligible, 14 outside the supported reference range, four unequal lengths, two missing/ambiguous Parpola faces and one uncertain number. Exact/reverse copies in either namespace share groups. The 27/3/4 train/validation/test candidate split selects direct relative alignment by training correspondence entropy ({refs['training_alignment_entropy']['direct']:.3f} vs {refs['training_alignment_entropy']['reversed']:.3f} bits reversed).

A training-majority Parpola-to-Mahadevan mapper predicts {refs['test']['correct']}/{refs['test']['positions']} test positions, with {refs['test']['known_source_positions']}/{refs['test']['positions']} source-sign coverage and no fully correct test inscription. Every covered test position agrees, while unseen source signs remain failures. Fourteen training mappings reach the declared review threshold. These are conditional consistency results on unverified reference candidates, with only four test objects, not validation of all FC identities or sound values. No crosswalk is automatically propagated.

Original seal/impression photographs were actually inspected for M-1, M-3 and M-4 (printed pp. 1-3), rather than standardized drawings alone. M-1's HR 2406 edge marking matches its catalogue metadata; A-face and lowercase-a impression are visibly mirrored. M-3 shows three main graphic groups, with a broken lower/right body. M-4 has a longer mirrored sequence and textured/damaged surface, but its uncertain reference remains excluded. The record explicitly distinguishes this unblinded Codex-assisted screening from an expert transcription or complete allograph verification. The scans are cached privately, not redistributed. Further object-reference resolution and independent glyph review remain necessary.

### 4.20 Original graphic variants and postscript signs

Experiment 016 manually indexes every drawn form in the original variant appendix (printed pp.785-792) and inspects the sign-list postscript (printed p.25) [15]. The appendix count reconciles with the introduction only when the separate variant-addendum column is included:

| Section | Source families | Drawn forms |
|---|---|---|
| Main appendix | 167 | 615 |
| Variant addendum | 12 | 26 |
| Combined | {graphic['families']} | {graphic['forms']} |

All 641 forms have a source page/column, a literal example citation and a separate research ordinal/integer. Continuations of one family across columns preserve ordinal order. These are source-defined graphic families, may include the normal form and are not 641 additional independent signs or sounds. The catalogue adds two postscript base-sign references, M418/M419, while keeping the existing 417-ID benchmark and its integer assignments unchanged. The cited postscript inscriptions 8401/9222 are absent from the frozen application snapshot.

The occurrence lookup finds {graphic['lookup_counts']['unique_base_occurrence']} citations with one matching base-sign occurrence, {graphic['lookup_counts']['multiple_base_occurrences']} with repeated matching occurrences, five with no matching base ID and two unresolved parenthetical suffixes. Of the unique candidates, {graphic['unique_candidates_in_flagged_context']} are in rows flagged by the earlier source screen. No variant is automatically assigned even when the lookup is unique. The five remaining base-absence cases are MV254-main-07/1467, MV331-main-03/4592, MV347-main-04/7047, MV348-main-02/2055 and MV278-addendum-01/4595; enlarged page checks retained those printed citations rather than substituting convenient corpus matches.

An initial citation audit prompted thirteen visually confirmed digit corrections, all recorded with before/after values and source pages. Count agreement and successful lookups do not independently certify every manual digit or the editor's allograph judgements. Original rasters remain in private cache; the repository publishes numeric metadata and page-linked glyph references. Graphic distinctions are preserved as evidence for later review, without new phonetic values, language identification or changes to historical transcriptions.

## 5. Limitations and implications for decipherment

The main dataset is a secondary public export. No new glyph transcription, full catalogue reconciliation, artifact-family grouping, or independent translation anchor has been established. Splitting reverse/exact copies does not eliminate all near-duplicate or formula leakage. Allograph distinctions may inflate the vocabulary and hapax rate ({100*d['hapax_fraction']:.1f} percent in the main subset). The complete-only filter selects against difficult inscriptions and may bias inference. Rare sign embeddings and small CISI morphology counts are unstable.

The models establish conditional predictability under declared controls. They cannot determine whether that structure encodes phonology, names, quantities, transactions, or a mixture. Fitting an unconstrained rebus or a surname list would risk selecting the desired answer through researcher flexibility. Later Tamil and Sanskrit proxies have now been compared structurally under fixed representation choices; no Proto-Dravidian, Indo-Aryan, Austroasiatic, or isolate phonetic mapping has been tested on historically matched, independently held-out language corpora in this release.

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
'''
    (ROOT/'docs/PAPER.md').write_text(paper)
    summary=f'''# Results snapshot

17 October 2026. No decipherment claimed.

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
- Reference-glyph screening: all 29 candidate drawings broadly fit source descriptions, with unresolved variant/conflict cases. Scalar morphology records cover 715 cached reference images; no original-object photos, numerical values or phonetic readings are validated.
- Metadata-conditioned models: site-plus-type shows a small aggregate gain, but matched-smoothing type/site-plus-type intervals overlap zero. No robust independent metadata contribution or decoded object-class formula is established.
- Fish-rebus audit: H-9's graphic pattern matches a published witness; M-112 exposes plain/modified-fish and filter disagreement. Counts 3/6/7 are enriched in the queried subset, but three competing H-9 interpretations remain observationally indistinguishable; no phonetic value is accepted.
- Uncertainty sensitivity: adding 25/62 annotated objects gives small fixed-clean-holdout gains with intervals overlapping zero. Source audit finds 43/733 alias-absence positions, 38 with zero annotation codes; filters do not certify transcriptions or a phonetic grammar.

- Exact two-sign gap reconstruction: bigram top1 {100*two_summary['whole_top1']:.1f}%, top5 {100*two_summary['whole_top5']:.1f}%; candidate coverage {100*two_summary['whole_truth_in_training_vocabulary']:.1f}%. Known-length synthetic restoration supplies no phonetics or validated original-object completion.

- Richer non-phonetic administrative control: all three fixed-seed realizations show bigram gains, masked-sign prediction and within-text shuffle rejection. These features are compatible with known non-phonetic generation and cannot select Indus sound values. Full semantic records are exported; this is not a replication of SIGIL or a model classification.

- Primary Mahadevan acquisition: 3,916 official records, 417 sign-list references and separate integer encodings; 2,391 rows pass the declared strict single-line screen. All secondary base sequences agree, but 265 strip doubtful marks and 92 concatenate lines. No new phonetic value or namespace merger.

- Face-preserving field-code prediction: metadata baseline 1.647 vs sign-augmented 1.629 bits/row; gain interval crosses zero, accuracy/macro recall decline. Majority code dominates the 99-row test. No independent semantic anchor established; giant-component validation imbalance is disclosed.

- FC-reference candidate audit: 34 strict tentative pairs; 10/21 test positions covered and predicted correctly, with all other source signs unseen. Original/impression photos of M-1/M-3/M-4 reviewed. FC/Mahadevan identity remains unresolved, so mappings are not propagated.

- Original variant inventory: 641 drawn forms in 179 source families (615/167 main plus 26/12 addendum), with page references and separate integer ordinals. M418/M419 postscript signs added as references; old benchmark unchanged. Lookup: 613 unique, 21 repeated, five base-absence cases, two unresolved suffixes; no automatic assignments.

Full methods and limitations are in docs/PAPER.md and docs/METHODS.md. Results are structure, not translations.
'''
    (ROOT/'results/SUMMARY.md').write_text(summary)
    print('Generated paper and summary from executed outputs.')

if __name__=='__main__':main()
