# Methods and experiment ledger

Started 15 October 2026 (Asia/Kolkata). This file distinguishes completed experiments from planned work. Every reported result must be reproducible from pinned sources and linked output.

## Completed preparation

- Inspected the empty local repository and verified access to the requested GitHub repository.
- Located CISI/Parpola digitization and a larger ICIT-derived CSV export.
- Inspected direction conventions, damage annotations, allograph features, and proposed-translation contamination.
- Identified that `xlits.csv` contains speculative sound assignments and canonical sign conflations; excluded it from analytical input.
- Began reading original research on n-grams, entropy, networks, rebus interpretation, and critiques of linguistic inference.

## Executed experiments (release 0.1)

| Method | Output | Finding |
|---|---|---|
| Literature review | LITERATURE.md | Nine sources inspected at explicitly stated scope |
| Pinned acquisition and source hashes | data/raw/manifest.json | 5,679 ICIT-derived rows, 179 annotated CISI sides; proposed readings excluded |
| Conservative filtering and deduplication | data/processed/audit.json | 2,156 complete distinct sequences, 9,221 tokens, 637 clean-subset IDs; 91 clean distinct CISI sequences |
| Icon coverage and separate catalogues | SIGN_CATALOGUE.html; data/raw/glyph_reference_validation.json | 715 verified remote image files cover all 712 raw observed IDs; 395 separate Parpola descriptions |
| Integer encoding | data/processed/encodings.json; numeric_inscriptions.json | Per-namespace dense integers; PAD/UNK/BOS/EOS reserved; no phonetic values |
| Frequency, lengths, hapax, repeated phrases | results/descriptive.json | Mean length 4.277, hapax fraction 36.1%; 47 repeated five-sign subsequences |
| Conditional entropy, three shuffle controls | results/entropy_nulls.json | 3.892 observed vs null means 4.593/4.757/4.958 bits; p=0.005 each, 199 trials; Bonferroni-adjusted p=0.015 for three tests |
| Unigram, bigram, trigram prediction | results/sequence_models.json | Five reverse/exact-group splits; validation-selected smoothing; mean test scores 6.450/5.452/5.453 bits/token including EOS; no consistent trigram gain |
| Paired bootstrap uncertainty | sequence_models.json | 500 resamples per split; all unigram-to-bigram intervals exclude zero; conditional on corpus |
| Hidden-sign prediction | sequence_models.json | 29.0-35.5% top-1, 52.1-57.5% top-5; frequent-sign baseline 9.4-11.4%; synthetic masking only |
| Reading-order sensitivity | results/reverse_models.json | Reversed texts remain predictable; no reading direction established by models alone |
| Cross-site transfer | results/site_transfer.json | Bigram gains on Harappa and Mohenjo-daro holds; target-attested sequences and reversals excluded from training |
| Independent positional slot predictor | results/slot_control.json | Sign-only unigram/slot/bigram scores 7.085/6.829/6.111 bits; positions explain part of predictability |
| Synthetic administrative slots | results/synthetic_slots.json | Entropy 5.109 bits; generator does not match observed local order and long repeats; richer administrative systems remain viable |
| Context embeddings and neighbours | results/embeddings_sparse_ppmi.json; embeddings_32d.json; context_neighbours.json | Training-only directional PPMI, deterministic 32D projection, exact sparse cosine; no semantic values assigned |
| Finite template grammar | results/grammar.json; position_profiles.json | Held-out coverage 66.8% vs 32.3% in one shuffle; operational positions, not parts of speech |
| Candidate segmentation | results/segmentation_candidates.json | 163 train-selected pairs with count >=5 and PMI >=1; collocations, not confirmed words |
| Directed transition graph | results/transition_network.json | Adjacency edges and degrees; no semantic classification or recursive-tree replication |
| Conservative tally/fish adjacency | results/numeral_fish.json | 17 adjacencies vs null mean 5.902, exploratory p=0.002, 499 trials; no sound or numerical value established |
| Substitution identifiability | results/substitution_identifiability.json | Ten abstract syllable relabelings preserve entropy; structure alone cannot choose meanings |
| Filtering sensitivity | results/sensitivity.json | Descriptive subsets: length>=3, R/L metadata only, eligible rows retaining duplicate occurrences |
| Correctness and repeatability checks | scripts/test_pipeline.py; scripts/reproduce.py | Damage handling, exact/reverse split isolation, probability normalization, shuffle invariants, relabel invariance; exact JSON structure/labels/counts with float tolerance 1e-12 |
| Research paper | PAPER.md; output/pdf/indus_structural_research.pdf | Generated from executed outputs; PDF rendered and visually reviewed |
| Hidden-state stochastic grammar | results/latent_grammar.json; latent_grammar_parameters.json | 18 validation-selected candidates; selected 8-state model scores 5.919 bits/token vs bigram 5.461. HMM gain -0.457, grouped interval [-0.583,-0.343]; negative result for this tested family |
| Near-copy overlap audit and component holdout | results/near_copy.json; near_copy_groups.json | 57/169 original eligible test texts have training neighbours. Grouped holdout retains 0.922-bit bigram gain, component interval [0.755,1.077]; similarity groups are not verified artifact families |
| HMM numerical validation | scripts/test_latent.py | Three tests compare likelihood/posteriors against exhaustive path enumeration, verify parameter mass after EM, and verify near-copy grouping |

## Revisions, errors corrected, and negative results

- Initial icon indexing used the explorer's numeric list and missed seven observed IDs. A pinned image-tree audit recovered those seven plus two other image IDs, and found nine non-placeholder listed IDs with no file. The corrected catalogue uses verified paths and records the discrepancy.
- A broad description search for vertical strokes included complex decorated signs, including fish with strokes. It was unsuitable as a numeral proxy. The final morphology test uses conservative explicit catalogue sets (fish P048-P065; simple strokes P121-P130, P144, P145, P147, P150, P151). This refinement followed exploratory inspection; its p-value is not preregistered confirmation.
- The initial masked-prediction baseline chose EOS. It was corrected to choose the most frequent actual training sign and results regenerated before committing them.
- Trigrams gave no consistent predictive gain over bigrams. Independent slot generation did not reproduce the observed local dependence or five-sign repeats in this run. Abstract syllable relabeling did not identify a unique key.
- Upstream xlits.csv contains speculative phonetic values and conflations; it was inspected but excluded from acquisition and modeling.
- A guessed ACL URL resolved to an unrelated article and was excluded; the actual critique and reply were retrieved by title.
- Local byte-identical reproduction passed. Linux CI showed floating-point serialization differences in four result files. The cross-platform check now requires exact structure, IDs, labels and counts, and numerical equality within 1e-12; it fails with a precise location for larger drift. Source snapshots still require exact SHA-256 equality.
- Bootstrap resampling was tightened to exact/reverse groups rather than individual sequences, keeping mirrored texts together in confidence intervals as well as dataset splits. The small interval changes do not alter the reported prediction conclusions.
- Experiment 002 was designed and committed before its execution, on an already explored corpus. Tested 2/4/8 HMM states, seeds 17/29 and 5/10/20 EM checkpoints. Validation selects the largest tested state count; the experiment does not establish an optimal number of states. All tested configurations and the selected model are preserved, including the worse-than-bigram result.
- Near-copy confidence intervals resample whole similarity components. Transitive one-substitution groups are a leakage sensitivity test, not a replacement for archaeological family annotation. Different-length neighbours remain a resource gap.

## Pending methods and resource gaps

1. Independent photographic verification, orientation review, complete inventory acquisition and catalogue crosswalk validation.
2. Blind allograph split/merge experiments and uncertainty propagation.
3. Verified artifact/mold/family splits, unequal-length near-duplicate analysis and metadata-conditioned models; one-substitution sensitivity is now executed.
4. Expanded latent grammar families and state-count range, nonlocal dependency tests, richer administrative baselines; compact HMM experiment is now executed.
5. Licensed historical corpora and matched grapheme comparisons for Dravidian, Indo-Aryan, Austroasiatic and other hypotheses.
6. Constrained multilingual/rebus alignment with external lexical anchors, chronology and equal-complexity alternative mappings.
7. Number/quantity reconstruction using stroke counts, metrology and independently identified archaeological contexts.
8. OCR and glyph-shape models using appropriately licensed labeled images.
9. Secure bilingual/name anchors if identified, independent specialist review and prospective predictions.

These are planned, not claimed as tried. The goal remains active: exhaustive acquisition and genuine decipherment have not been achieved. “Any and all methods” is an open research objective, not a finite procedure completed in this release.

## Evidence policy

Structure is not meaning. A successful sign predictor does not establish a language family. A fitted mapping is not a decipherment unless independent evidence and held-out predictions distinguish it from alternatives. Null results and unavailable resources must be recorded.
