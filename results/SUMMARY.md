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
- Described stroke counts depend on followers under height/position-preserving controls (two-test-adjusted p=0.004/0.008). All three followers with at least five events admit multiple counts. Graphic counts are not proven numerical values; no metrological scale or sign meaning is established.
- Paired-object catalogue integration: 85 usable pairs; training selects reversed relative alignment. Held-out majority correspondence accuracy 31/39 positions, 82.1% source-ID coverage, 29 candidate mappings for glyph review. These are catalogue labels, not sound assignments.
- Reference-glyph screening: all 29 candidate drawings broadly fit source descriptions, with unresolved variant/conflict cases. Scalar morphology records cover 715 cached reference images; no original-object photos, numerical values or phonetic readings are validated.
- Metadata-conditioned models: site-plus-type shows a small aggregate gain, but matched-smoothing type/site-plus-type intervals overlap zero. No robust independent metadata contribution or decoded object-class formula is established.
- Fish-rebus audit: H-9's graphic pattern matches a published witness; M-112 exposes plain/modified-fish and filter disagreement. Counts 3/6/7 are enriched in the queried subset, but three competing H-9 interpretations remain observationally indistinguishable; no phonetic value is accepted.
- Uncertainty sensitivity: adding 25/62 annotated objects gives small fixed-clean-holdout gains with intervals overlapping zero. Source audit finds 43/733 alias-absence positions, 38 with zero annotation codes; filters do not certify transcriptions or a phonetic grammar.

- Exact two-sign gap reconstruction: bigram top1 12.7%, top5 25.0%; candidate coverage 96.1%. Known-length synthetic restoration supplies no phonetics or validated original-object completion.

Full methods and limitations are in docs/PAPER.md and docs/METHODS.md. Results are structure, not translations.
