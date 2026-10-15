# Methods and experiment ledger

Started 15 October 2026 (Asia/Kolkata). Current release 0.13. This file distinguishes completed experiments from planned work. Every reported result must be reproducible from pinned sources and linked output.

## Completed preparation

- Inspected the empty local repository and verified access to the requested GitHub repository.
- Located CISI/Parpola digitization and a larger ICIT-derived CSV export.
- Inspected direction conventions, damage annotations, allograph features, and proposed-translation contamination.
- Identified that `xlits.csv` contains speculative sound assignments and canonical sign conflations; excluded it from analytical input.
- Began reading original research on n-grams, entropy, networks, rebus interpretation, and critiques of linguistic inference.

## Executed experiments

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
| Allograph schema audit and integer inventory | data/processed/parpola_variant_catalog.json; parpola_variant_sequences.json | All 455 vectors match source schemas; 92 eligible objects contain 133 base IDs and 210 morphology-coded variants, excluding confidence/layout defaults |
| Previous-allograph-history prediction | results/allograph_history.json | Same next-base-sign target; validation-selected strengths; five exact/reverse-group holds. Mean change -0.080 bits/token, all point estimates worse; four intervals overlap zero. No evidence to assign distinct sounds or merge variants |
| Allograph model checks | scripts/test_allographs.py | Four checks: variant identity excludes layout/confidence, probabilities normalize, unseen histories back off, base duplicates share splits, and target morphology does not predict its own target |
| Historical-language resource acquisition | scripts/language_inventory.py; docs/language_resource_inventory.json | Pinned Tamil and Vedic Sanskrit candidates downloaded into ignored local cache; file hashes and coverage audited. No alignment or language identification experiment reported yet |
| Controlled language-proxy representation comparison | results/language_representation.json; data/language_samples | 40 numeric samples, ten seeds for each of two languages/two units; exact Indus lengths and 9,221 tokens per sample; 49 matched-frequency permutations per sample. Entropy distance ranks Sanskrit nearer for words, Tamil nearer for letter-plus-mark units. No family inference |
| Source normalization and sampling validation | scripts/test_language_compare.py | Three tests verify canonical/mark normalization including Tamil spacing marks, CoNLL-U ranges/empty-node/punctuation exclusions, exact lengths and no document crossing |
| Licensed opaque sample packaging | data/language_samples/ATTRIBUTION.md; manifest.json | Numeric samples, source-document metadata and window offsets are committed with Tamil Apache-2.0 and Vedic CC BY-SA 4.0 attribution. Token dictionaries and original text documents stay local; metric recomputation is network-free |
| Graphic stroke-count / follower constraint test | results/stroke_count_constraints.json | 79 catalogue-described stroke slots; 65 usable follower events. Count/follower MI exceeds height/position-preserving controls; two-test-adjusted p=0.004 overall, 0.008 short-only. All three followers with >=5 examples have multiple counts; no numerical meaning or scale established |
| Stroke-count correctness tests | scripts/test_stroke_counts.py | Three checks establish known independent/perfect-dependence MI values, permutation preservation of count/height/position marginals and follower identities, and separate tall/short mappings excluding decorated counts |
| Paired-object catalogue correspondence | results/catalogue_correspondence.json | 85 accepted pairs, 94 audited exclusions; copies in either catalogue grouped. Training selects reversed ICIT alignment. Test accuracy 31/39 positions; source-ID coverage 32/39. Twenty-nine training-derived review candidates; no semantic/sound mapping |
| Crosswalk consistency and errors | catalogue_correspondence.json | Candidate distributions, held-out failures and known-source-only smoothed log loss preserved. Exploratory comparison finds review candidates consistent with supplied Wells aliases; shared ancestry means this is not independent glyph verification |
| Correspondence correctness checks | scripts/test_correspondence.py | Four checks: ambiguous/unequal-length joins rejected, alignment does not mutate sources, copies in both catalogues share splits, and unknown source IDs count as failures |
| Reference-glyph visual screening | docs/glyph_screening.json | 29 standardized references broadly fit supplied descriptions. Codex-assisted, unblinded screen; no original-object photos reviewed, no independent crosswalk validation or meanings assigned |
| Scalar glyph morphology encoding | data/processed/glyph_morphology.json | All 715 images acquired into ignored cache; source hashes and scalar ink/aspect/moment/component descriptors exported. No raster assets or reconstructible grids packaged |
| Optional image-extractor checks | scripts/test_glyph_morphology.py | Two synthetic-mask tests verify eight-connectivity, component counts and translation invariance; six already-viewed simple-stroke matches validate implementation only |
| Offline numeric glyph snapshot validation | scripts/validate_glyph_snapshot.py | File hash, inventory/link consistency, bounds, component mass and scalar arithmetic invariants checked without Pillow/network; image-derived input is not regenerated by the default analytical pipeline |
| Metadata-conditioned formula prediction | results/metadata_conditioning.json | All 3,591 eligible rows, duplicate groups kept together; site/type/site+type histories with validation-selected smoothing. Site+type nominal gain 0.079 bits; matched-strength metadata gain 0.034 with interval crossing zero. No robust independent metadata effect established |
| Smoothing ablation and uncertainty | metadata_conditioning.json | Post-initial-score diagnostic holds each metadata model's base strength fixed. Type gain 0.015, site+type 0.034 (both 95% intervals include zero); site alone is worse. Group bootstrap uses 1,000 resamples and three-comparison 98.33% sensitivity intervals |
| Metadata-model checks | scripts/test_metadata_models.py | Three checks verify literal type-prefix handling, normalized probability/unseen-metadata backoff, and exact/reverse copies sharing partitions despite different metadata |
| Published fish-rebus witness audit | results/fish_rebus_audit.json | H-9 matches the published two-glyph pattern; M-112 uses plain fish in ICIT but modified fish in annotated CISI and is excluded by damage elsewhere. Named witnesses are retrospective checks, not independent discoveries |
| Larger diagnostic fish/count query | fish_rebus_audit.json | 43 complete unique fish/stroke slots, 25 with described counts 3/6/7 vs 162/770 other followers. Exploratory enrichment p=0.001; opposite adjacency p=0.149. Shape aliases/orientation and slot exchangeability are assumptions, not verified semantics |
| Conditional semantic/phonetic templates | fish_rebus_audit.json | H-9 admits the published hypothetical eZu-miin/star reading, an unknown quantity/classifier reading, and an unknown category/rate reading with identical graphics. No independent anchor selects one; no proposed value adopted |
| Fish-audit checks | scripts/test_fish_rebus.py | Two checks verify explicit direction, absence of cross-artifact adjacency and exclusion of tally-as-head combinations |
| Uncertainty-sensitive training | results/uncertainty_sensitivity.json | Same clean validation/test objects; add 25/62 hypothesis-transcribed objects without unknown stretches or holdout copies. Gains 0.052/0.047 bits have 95% intervals crossing zero; no reading promoted to truth |
| Broader paired-source consistency | uncertainty_sensitivity.json | 136 equal-length uniquely identified pairs, 733 positions, 43 supplied-alias absences; 38 locally unmarked. No automatic error label or correction; annotation zeroes do not establish source agreement |
| Uncertainty-filter checks | scripts/test_uncertainty_sensitivity.py | Three checks reject unknown/multiline stretches, forbid holdout objects/reversed copies in additions, and preserve literal raw code filtering without misreading encoded location digits as calibrated percentages |

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
- Experiment 004 changes its nearest-proxy ranking when only representation changes: word distances favour Sanskrit, letter-plus-mark distances favour Tamil. Vocabulary/sparse-estimator and duplicate-window effects remain visible. This is a failed family-identification criterion, not positive evidence for either candidate.
- Experiment 005 records morphological counts only. Dependency significance is conditional on slot-exchangeability and specified height/position strata, not archaeological independence. It neither calibrates weights nor establishes tax/ration/star/name semantics. Repeated or related artifact contexts may affect slot exchangeability; independent metrological fields are absent.
- Experiment 006 provides catalogue label correspondences rather than decipherment. Relative reversal is selected without test data. Fixed known-ID log-loss smoothing was specified after the initial accuracy run and does not alter selection. Wells alias checking is post-inference source consistency, not independent validation; candidate mappings remain provisional and are not propagated.

## Pending methods and resource gaps

1. Independent photographic verification, orientation review, complete inventory acquisition and catalogue crosswalk validation.
2. Blind epigraphic allograph split/merge review and uncertainty propagation; representation/history sensitivity is now executed.
3. Verified artifact/mold/family splits, unequal-length near-duplicate analysis and metadata-conditioned models; one-substitution sensitivity is now executed.
4. Expanded latent grammar families and state-count range, nonlocal dependency tests, richer administrative baselines; compact HMM experiment is now executed.
5. Historically matched grapheme comparisons for Dravidian, Indo-Aryan, Austroasiatic and other hypotheses; initial Tamil/Vedic resource acquisition is executed, but chronology, genre and phonological reconstruction remain unresolved.
6. Constrained multilingual/rebus alignment with external lexical anchors, chronology and equal-complexity alternative mappings.
7. Number/quantity reconstruction using stroke counts, metrology and independently identified archaeological contexts.
8. OCR and glyph-shape models using appropriately licensed labeled images.
9. Secure bilingual/name anchors if identified, independent specialist review and prospective predictions.

These are planned, not claimed as tried. The goal remains active: exhaustive acquisition and genuine decipherment have not been achieved. “Any and all methods” is an open research objective, not a finite procedure completed in this release.

## Evidence policy

Structure is not meaning. A successful sign predictor does not establish a language family. A fitted mapping is not a decipherment unless independent evidence and held-out predictions distinguish it from alternatives. Null results and unavailable resources must be recorded.

## Contiguous-gap reconstruction (Experiment 011)

Design committed before execution. Exact one/two-sign candidate enumeration conditions on known gap length and uses all training glyph IDs, with EOS/UNK excluded from proposed fillings. Complete validation loss selects smoothing; held-out overlapping masks are grouped by canonical inscription for uncertainty. Toy exhaustive-path normalization, unknown-neighbor behavior and unigram context invariance checks pass. Of 709 two-sign masks, 12.7% are recovered at top1 and 25.0% at top5; the entire truth is in the training vocabulary in 96.1%. The unigram whole-gap top1 baseline is 0%; the paired gain interval is [9.7,15.7] percentage points across 202 inscription groups. Top-filling token accuracy is 25.2%. Most gaps remain unresolved. Results and model-confidence diagnostics are recorded in `results/gap_reconstruction.json` and the paper; the original one-sign benchmark must match exactly. No 000 unknown stretch receives a guessed cardinality or translation.

## Richer administrative control (Experiment 012)

Design committed/pushed before execution. Separate fictional notation with explicit institution/guild licenses, commodity/quantity preferences, rank and validation conventions; no phonetic values. Three seeds each match only the Indus length list, not observed sign frequencies/transitions. All show conditional entropy about 2.91 bits vs within-text null about 4.43 (99 trials; p=0.010), held-out bigram improvement about 2.22-2.26 bits with grouped intervals excluding zero, and single-mask top1 33.1-34.5% vs 3.8-5.7% frequent-sign baselines. Generated duplicates stay weighted but canonical reverse/exact groups do not cross splits. This shows compatibility with non-phonetic generation, not an Indus administrative decipherment, a likelihood ratio, or SIGIL replication. Full semantic records and licenses are in results/administrative_control.json. Three new checks verify determinism, length/role constraints and detection of a corrupted semantic record.

The scoped recent-source/retrieval audit is in RECENT_RESEARCH_AUDIT.md. The SIGIL corpus was not retrieved from checked sources; no reported SIGIL results are adopted as independently executed here. New proposed-readings repositories are leads and remain outside neutral analytical input.

## Primary Mahadevan acquisition (Experiment 013)

Design committed/pushed before bulk acquisition. Official public collection paginated into 3,916 frozen whitelisted records, retaining raw annotations and update times; no unrelated collections or proposed readings. Printed code/sign-list pages 30-35 visually reviewed in the original 1977 scan. Separate 417-ID numerical catalogue and page-linked glyph references exported. Full line-level exclusion ledgers distinguish 2,391 strictly eligible rows/1,534 canonical strings/375 IDs from all raw records. Raw snapshot has all 417 IDs and 504 doubtful tokens. Source signnum agrees with nongap positions and posnum with all serialized slots throughout; unknown spans are not expanded.

Secondary export pinned with MIT attribution; every one of its 2,742 base sequences matches the official side-specific reconstruction, but 265 remove doubtful marks and 92 join multiple lines. Primary codebook shows direction labels 4/5/9 differ from the secondary definitions. No motif association, reading-order correction, phonetic key or cross-namespace propagation is attempted. Four tests check doubt/gap preservation, face isolation and multiline reconstruction, corrupted slots/counts and scanned sign-page boundaries. This is acquisition/encoding, not model fitting.
