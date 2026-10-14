# Research continuation state

15 October 2026. Active user goal: investigate decipherment with all useful methods, acquire signs, encode/model them, review papers, record all trials and produce a paper, push incrementally to the requested GitHub repository.

## Completed release 0.1

Pinned data, verified 715 glyph file references, separate 395-entry Parpola catalogue, numeric encodings, 2,156 complete unique ICIT sequences, descriptive measures, three permutation controls, five held-out n-gram runs, mask prediction, site holds, positional controls, synthetic slots, embeddings, finite grammar, collocations, graph, tally/fish test, substitution invariance, sensitivity descriptions, methods ledger, literature notes and five-page PDF paper.

`python3 scripts/reproduce.py --check` passed. Paper pages rendered with Poppler and visually reviewed. No decipherment, language-family identification or phonetic assignment achieved. Goal remains active.

## Completed release 0.2 extension

Experiment 002 was committed before execution. An explicit-stop HMM tested 18 configurations selected on validation; chosen 8-state model scores 5.919 vs bigram 5.461 bits/token, a negative result. One-substitution near-copy components yield unigram/bigram scores 6.527/5.606; grouped gain 0.922 with interval [0.755,1.077]. 57/169 original length>=3 test texts have training neighbours. Three new numerical/grouping tests pass. Posterior parameters and component assignments are exported. Paper and ledger incorporate both results. Local reproduction and Linux GitHub CI passed, including all nine correctness checks. The updated six-page PDF was rendered and visually reviewed.

The author-hosted PNAS Markov paper and supplement are available in ronojoy/indus at commit cab6c2d881307825f24d7ed28f7ad62de800ae13; abstract/rationale/corpus/missing-sign passages were inspected. That repository contains no machine-readable transcriptions. A local untracked copy is in .cache/MarkovModelIndusScript.pdf. The paper's most-probable completion approach is useful for future multi-damage restoration tests, which must be validated by masking untouched texts before use on genuinely damaged objects.

## Completed release 0.3 extension

Experiment 003 audits all 455 morphology vectors across 92 eligible CISI objects and exports 210 morphology-coded variants of 133 base IDs, with schemas, descriptions, integers and per-object sequences. Previous-variant history prediction targets the same next base sign as baseline, excludes target morphology, and keeps exact/reverse base copies together. All five small holds favour base bigrams; mean change -0.080 bits/token, four intervals overlap zero. No grounds for assigning distinct sounds or merging variants were established.

Candidate historical-language resources are now cached locally through scripts/language_inventory.py: Akananuru (400 verses), Purananuru (388 verses), UD Vedic Sanskrit (27,182 sentence blocks across train/dev/test). URLs, revisions, license metadata and raw hashes are in docs/language_resource_inventory.json; the texts themselves are not committed. Akananuru edition links are null and source provenance needs review. UD README counts are outdated relative to the downloaded snapshot. See LANGUAGE_RESOURCES.md for extraction and chronology limits.

Thirteen correctness checks and offline numerical reproduction pass. Paper version 0.3 incorporates the allograph experiment; the research goal remains active and no decipherment is claimed.

Upload history: two release-0.3 push attempts timed out connecting to github.com port 443. On the release-0.4 continuation, push succeeded and uploaded 8c32783, f7aacf2 and cb40365; the Experiment 004 design was also committed and pushed before execution. Inspect current remote/CI state before asserting validation of any newer commit.

## Completed release 0.4 extension

Experiment 004 creates 40 matched-length numeric samples across Tamil/Sanskrit and word/letter-plus-mark representations (seeds 17-26). Each sample has 2,156 snippets, exactly 9,221 tokens and the original Indus length list; frequency-preserving controls use 49 shuffles. Nearest mean conditional-entropy distance selects Sanskrit for words, Tamil for letter-plus-mark units. This rank reversal rejects that metric as a justified family identification in this setup. It supplies no phonetic assignment. Vocabulary sizes, duplicate windows, chronology and genre limitations are reported.

Opaque samples are committed under attributed Tamil Apache-2.0 and Vedic CC BY-SA 4.0 terms. Scripts can regenerate samples from hash-verified cached sources; normal reproduction recomputes results from numeric samples without network. Original candidate documents and dictionaries are not packaged. Three new independent parsing/normalization/windowing checks bring the total to 16. Local reproduction and Linux CI (run 38627526061, result commit 61833d1) pass. The seven-page paper version 0.4 was rendered and visually reviewed; the full decipherment goal remains active.

## Completed release 0.5 extension

Experiment 005 was committed and pushed before execution. A conservative catalogue mapping assigns described visible stroke counts, keeping short/tall height distinct. Of 79 stroke slots in 91 clean distinct CISI texts, 65 have eligible non-tally followers; exclusions are 11 tally-before-tally and three terminal cases. Count/follower MI is 1.619 bits vs stratified-null mean 1.408, adjusted p=0.004. Short-only: 1.535 vs 1.296, adjusted p=0.008. The null shuffles count labels within height and initial/medial strata (999 trials). These conditional exploratory results assume slot exchangeability, not full archaeological independence.

All three followers with >=5 examples admit multiple counts: P004 [3,4], P050 [1,2,3,4], P086 [3,4,6,8]. No numerical values, metrological scale, commodity labels or linguistic readings are established. Source object IDs and follower morphology are retained for audit. Three new checks bring the total to 19; local offline reproduction passes for all 35 analytical JSON artifacts. Methods and the visually reviewed eight-page paper version 0.5 incorporate both constraints and independent-quantity evidence gaps. The administrative paper's relevant numerical/rate passages were read; exact published glyph classes are not replicated.

## Completed release 0.6 extension

Experiment 006 joins 85 equal-length complete uniquely labeled object pairs and audits 94 exclusions (87 Parpola-ineligible, five unequal-length, two ICIT-ineligible). Copies linked through either catalogue share groups; seed 42 yields 67 train, nine validation and nine test objects. Training alignment entropy is 1.947 bits direct vs 0.087 reversed; reverse ICIT order is selected relative to normalized Parpola transcriptions.

Held-out test: 31/39 correct positions, 32/39 source-ID coverage and two fully correct objects. Known-source-only log loss is 3.485 bits/position with additive 0.5 smoothing and collapsed unknown targets. Twenty-nine review-priority correspondences meet training support/purity thresholds; source Wells aliases agree, but this is shared-metadata consistency, not independent glyph verification. No namespace merge or sound/meaning propagation occurs. Four new checks bring the total to 23. Paper version 0.6 reports catalogue reconciliation as a prerequisite, not decipherment.

## Next substantive work

1. Constrain prospective phonetic/rebus alignments through independent lexical or archaeological anchors; controlled representation comparison is now executed and rank reversal confirms that nearest entropy alone cannot select a family. Investigate matching vocabulary/sparse-estimator controls and other language families before alignment claims.
2. Extend artifact-type controls and unequal-length/verified-family leakage audits; one-substitution component holdout is executed.
3. Independently review the 29 candidate catalogue correspondences against glyphs and original object/face records, expand annotated variants, and investigate length-mismatch/alias conflicts. The initial previous-variant prediction gives no gain; preserve morphology and uncertainty.
4. Expand hidden-state grammar size/families and inspect train-only posterior roles; compact HMMs tested so far are worse than bigrams.
5. Expand graphic count/follower evidence beyond this small selected subset; obtain independently measured quantities, metrological contexts and verified glyph crosswalks before any numerical decoding. Current stroke-count experiment has no such external calibration.

Do not equate stored-order initial/final positions with linguistic prefixes/suffixes. Do not treat a sign's integer ID as its value. `xlits.csv` is contaminated with proposed readings and conflations. Main sequence scoring maps novel IDs to UNK; mask accuracy requires exact known IDs. Current shuffled and morphology results are exploratory.

All authored code and outputs reside in this repository. Raw snapshots permit offline reproduction. External glyph images are linked rather than packaged. Update paper and ledger after each substantive result and push incremental verified commits without force-pushing.
