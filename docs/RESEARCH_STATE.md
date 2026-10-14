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

## Next substantive work

1. Use the acquired candidate corpora for controlled unit/genre/short-text structural comparison; explicitly test the effect of representation and avoid interpreting a nearest curve as a language identification. Establish chronology, document grouping, and normalization before constrained alignment.
2. Extend artifact-type controls and unequal-length/verified-family leakage audits; one-substitution component holdout is executed.
3. Expand annotated graphic variant data and blind epigraphic review; the initial previous-variant prediction experiment is executed and gives no gain. Preserve morphology and uncertainty.
4. Expand hidden-state grammar size/families and inspect train-only posterior roles; compact HMMs tested so far are worse than bigrams.
5. Expand metrology/number-like evidence with independently annotated context, and obtain primary catalogue/photo verification.

Do not equate stored-order initial/final positions with linguistic prefixes/suffixes. Do not treat a sign's integer ID as its value. `xlits.csv` is contaminated with proposed readings and conflations. Main sequence scoring maps novel IDs to UNK; mask accuracy requires exact known IDs. Current shuffled and morphology results are exploratory.

All authored code and outputs reside in this repository. Raw snapshots permit offline reproduction. External glyph images are linked rather than packaged. Update paper and ledger after each substantive result and push incremental verified commits without force-pushing.
