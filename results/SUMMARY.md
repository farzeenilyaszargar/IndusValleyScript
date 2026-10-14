# Results snapshot

15 October 2026. No decipherment claimed.

- Corpus: 2,156 clean distinct sequences, 9,221 tokens, 637 IDs.
- Inventory: 715 verified remote glyph references; 395 separate Parpola descriptions.
- Mean held-out scores: unigram 6.450, bigram 5.452, trigram 5.453 bits/token (including EOS; unseen signs collapsed to UNK).
- Mask top-1: 29.0-35.5%; top-5: 52.1-57.5%; frequent-sign top-1 baseline: 9.4-11.4%.
- Entropy: 3.892 bits; all three permutation p-values 0.005 (199 trials each).
- Simple tally/fish adjacency: 17 vs null mean 5.902, exploratory p=0.002.
- Role-template held-out coverage: 66.8%; single-shuffle coverage 32.3%.
- Ten abstract substitutions preserve entropy: no phonetic or semantic key identified.
- Validation-selected HMM: 5.919 vs bigram 5.461 bits/token; the tested HMM is worse.
- Near-copy component holdout: unigram 6.527, bigram 5.606 bits/token; grouped gain 0.922 with 95% interval [0.755, 1.077].
- Allograph audit: 210 morphology-coded variants of 133 base IDs in 92 clean annotated objects. Previous-variant histories did not improve next-base-sign prediction in five small holdouts.
- Language-proxy rank reversal: conditional-entropy distance selects Sanskrit with word units and Tamil with letter-plus-mark units under matched lengths/token totals. This method cannot justify a family identification. Opaque derived samples and attribution are packaged for offline reproduction.

Full methods and limitations are in docs/PAPER.md and docs/METHODS.md. Results are structure, not translations.
