# Research continuation state

15 October 2026. Active user goal: investigate decipherment with all useful methods, acquire signs, encode/model them, review papers, record all trials and produce a paper, push incrementally to the requested GitHub repository.

## Completed release 0.1

Pinned data, verified 715 glyph file references, separate 395-entry Parpola catalogue, numeric encodings, 2,156 complete unique ICIT sequences, descriptive measures, three permutation controls, five held-out n-gram runs, mask prediction, site holds, positional controls, synthetic slots, embeddings, finite grammar, collocations, graph, tally/fish test, substitution invariance, sensitivity descriptions, methods ledger, literature notes and five-page PDF paper.

`python3 scripts/reproduce.py --check` passed. Paper pages rendered with Poppler and visually reviewed. No decipherment, language-family identification or phonetic assignment achieved. Goal remains active.

## Completed release 0.2 extension

Experiment 002 was committed before execution. An explicit-stop HMM tested 18 configurations selected on validation; chosen 8-state model scores 5.919 vs bigram 5.461 bits/token, a negative result. One-substitution near-copy components yield unigram/bigram scores 6.527/5.606; grouped gain 0.922 with interval [0.755,1.077]. 57/169 original length>=3 test texts have training neighbours. Three new numerical/grouping tests pass. Posterior parameters and component assignments are exported. Paper and ledger incorporate both results.

## Next substantive work

1. Obtain historically appropriate, licensed language corpora and explicit sign/grapheme segmentation standards; compare competing families without speculative upstream translations.
2. Extend artifact-type controls and unequal-length/verified-family leakage audits; one-substitution component holdout is executed.
3. Test Parpola allograph feature representations against base IDs on the annotated subset; retain morphology and uncertainty.
4. Expand hidden-state grammar size/families and inspect train-only posterior roles; compact HMMs tested so far are worse than bigrams.
5. Expand metrology/number-like evidence with independently annotated context, and obtain primary catalogue/photo verification.

Do not equate stored-order initial/final positions with linguistic prefixes/suffixes. Do not treat a sign's integer ID as its value. `xlits.csv` is contaminated with proposed readings and conflations. Main sequence scoring maps novel IDs to UNK; mask accuracy requires exact known IDs. Current shuffled and morphology results are exploratory.

All authored code and outputs reside in this repository. Raw snapshots permit offline reproduction. External glyph images are linked rather than packaged. Update paper and ledger after each substantive result and push incremental verified commits without force-pushing.
