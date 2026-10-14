# Research continuation state

15 October 2026. Active user goal: investigate decipherment with all useful methods, acquire signs, encode/model them, review papers, record all trials and produce a paper, push incrementally to the requested GitHub repository.

## Completed release 0.1

Pinned data, verified 715 glyph file references, separate 395-entry Parpola catalogue, numeric encodings, 2,156 complete unique ICIT sequences, descriptive measures, three permutation controls, five held-out n-gram runs, mask prediction, site holds, positional controls, synthetic slots, embeddings, finite grammar, collocations, graph, tally/fish test, substitution invariance, sensitivity descriptions, methods ledger, literature notes and five-page PDF paper.

`python3 scripts/reproduce.py --check` passed. Paper pages rendered with Poppler and visually reviewed. No decipherment, language-family identification or phonetic assignment achieved. Goal remains active.

## Next substantive work

1. Fit HMM/latent-role models and compare to bigrams/slots using identical training groups and validation-selected complexity.
2. Extend artifact-type controls and near-duplicate/family leakage audit before interpreting grammar strongly.
3. Test Parpola allograph feature representations against base IDs on the annotated subset; retain morphology and uncertainty.
4. Find appropriately licensed historical language corpora and explicit grapheme segmentation standards; compare competing hypotheses without using speculative upstream translations.
5. Expand metrology/number-like evidence with independently annotated context, and obtain primary catalogue/photo verification.

Do not equate stored-order initial/final positions with linguistic prefixes/suffixes. Do not treat a sign's integer ID as its value. `xlits.csv` is contaminated with proposed readings and conflations. Main sequence scoring maps novel IDs to UNK; mask accuracy requires exact known IDs. Current shuffled and morphology results are exploratory.

All authored code and outputs reside in this repository. Raw snapshots permit offline reproduction. External glyph images are linked rather than packaged. Update paper and ledger after each substantive result and push incremental verified commits without force-pushing.
