# Sources, representation and coverage

See `data/raw/manifest.json` for pinned revisions, file URLs, and SHA-256 hashes. Run `python3 scripts/acquire.py` to recreate the source snapshots. Proposed Sanskrit readings, translations, interpretive classes, and notes are not retained in analytical input.

## Corpora

- **ICIT-derived export:** `field-cady/indus_valley_script_corpus`, commit `30308260d8da50151a79185c9e98404db9da331a`, `inscriptions.csv`. Upstream describes a derivation through Yajnadevam's Lipi repository from ICIT/Mahadevan. This is a secondary transcription, not a directly verified ICIT database release. The accompanying MIT notice is preserved. Rights to inherited third-party catalog material are not independently established by that notice.
- **CISI digitization:** `mayig/indus-valley-script-corpus`, commit `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`. MIT-licensed source credited to Michael Carlson; includes descriptions and cross-references to Parpola, Wells, and Mahadevan. All source vectors and feature descriptions are retained.
- **Glyph reference index:** `tejesh-raut/indus-valley-script`, commit `8dc5837469bc6694c05f9b310eee90b08399df9e`. Numeric inventory and external image links only. Images and fonts are not redistributed because no explicit asset license was found. The local catalogue can display remote references when network access is available.

## Filtering

ICIT eligible strings must match `+DDD(-DDD)*+`, without `000` or `999`. This conservatively excludes damaged/open boundaries and multi-line strings. It cannot remove unmarked transcription errors or ambiguity. Original text and rejection reasons remain available. Rows with identical sign strings are represented once; genuine repeat objects remain in the raw metadata.

CISI eligibility requires a nonempty single-line sequence, no `P000`, and zero damage and uncertainty in the default feature vector. The 179 available objects are a selected Mohenjo-daro subset, not the full CISI. Allograph information remains attached to the objects even though main sequence analysis uses Parpola sign IDs.

## Direction

ICIT sequences retain the export's stored order. Metadata includes R/L, L/R, and unclear entries; this does not document whether the exporter has already normalized reading order. We do not reverse strings based solely on this metadata. Initial/final in ICIT results means the first/last stored token, not a verified linguistic prefix/suffix. Reversed-order and R/L-metadata sensitivity experiments are supplied.

CISI source explicitly describes visual left-to-right transcription of sealings intended to read right-to-left. Its sequences are reversed for the morphology experiment. Across-line order is never guessed.

## Numbers and embeddings

`data/processed/encodings.json` assigns dense integers from 4 upward independently for each namespace; 0=PAD, 1=UNK, 2=BOS, 3=EOS. ID 740 is not a phonetic or numerical value. No arithmetic similarity between IDs is meaningful. `numeric_inscriptions.json` supplies integer sequences.

`results/embeddings_sparse_ppmi.json` stores training-only directional context PPMI vectors. `embeddings_32d.json` projects them into 32 deterministic dimensions. These are distributional representations, not semantic embeddings validated against translations. Rare signs have unstable contexts. Signs unseen in training receive no learned embedding. Embeddings use stored ICIT order.

## Catalogue completeness

The verified image directory has 715 non-placeholder IDs, covering all 712 observed non-placeholder IDs in the raw export. Initially, the explorer's numeric sign list omitted seven observed IDs while listing nine IDs with no image file. The tree-based acquisition fixes the catalogue and preserves the discrepancy in `data/raw/glyph_reference_validation.json`. The Parpola description catalogue contains 395 non-damage entries. These counts describe these sources, not the number of distinct signs in the civilization. Lists differ in how they split allographs and compound signs. Cross-reference fields are attributed source proposals, not a validated merge table. Do not equate a Wells W-ID, ICIT numeric ID, and Parpola P-ID without checking actual glyphs.

## Annotated variants (release 0.3)

The allograph experiment retains all 92 eligible clean object occurrences, including one repeated base sequence; exact/reversed base copies share splits. Their 455 tokens contain 133 base IDs and 210 distinct base-ID/custom-vector combinations. Every vector length matches the source schema. `parpola_variant_catalog.json` exports custom values, source schema, description, counts, object references and separate dense integers. Default damage/line/uncertainty fields are excluded from identity. An integer variant is a graphic representation, not proof of a distinct historical grapheme or sound value.

The prediction experiment compares the same next base-sign target while adding only the preceding sign's morphology. Target morphology is unavailable to its own prediction. It cannot establish allographic equivalence from a failed predictive gain.

## Paired-object candidate crosswalk (release 0.6)

`results/catalogue_correspondence.json` joins 85 uniquely labeled equal-length complete Mohenjo-daro object pairs. It retains all 94 rejected pairs, source positions, morphology, candidate distributions and held-out errors. Exact/reversed text copies in either catalogue share partitions. Training selects reversed relative ICIT alignment; this is evidence about matched source orders, not a blanket normalization rule for every object/site.

Twenty-nine correspondences meet the declared review-priority thresholds; their target labels also agree with the supplied Wells alias fields. Alias agreement is source consistency, not independent confirmation. Face equivalence, glyph shape and shared catalogue ancestry still require review. Candidate mappings are never automatically substituted into analytical corpora or treated as phonetic values.

## Scalar reference-glyph descriptors (release 0.7)

All 715 pinned JPEG references are acquired into ignored `.cache/glyph-reference`. `glyph_morphology.json` records each source URL/hash, canvas/ink bounds and scalar shape measures; raw pixels and fonts are not packaged. `glyph_morphology_manifest.json` fixes the numerical input snapshot's digest. Optional Pillow-based production recomputes features and checks cached source hashes. Default network-free reproduction checks this snapshot and arithmetic invariants; it does not claim to regenerate image features without the optional producer/images.

`docs/glyph_screening.json` records Codex-assisted screening of 29 standardized references. Broad description agreement is not original-object photo review or independent epigraphic verification. The 002 conflict and 817/861 variant equivalence remain open. No sound/semantic assignment follows from the screen or descriptors.

## Limits on inferred independence

Exact and reversed texts are grouped in train/validation/test splits. This prevents one obvious leakage mode but does not group every artifact family, shared mold, copied formula, or near duplicate. Site holds exclude sequences attested in the target site, using all eligible raw rows rather than only the first deduplicated record.

## Primary Mahadevan snapshot

Optional online acquisition: `python3 scripts/acquire_mahadevan.py`. Default offline audit: `python3 scripts/mahadevan_primary.py`. The public RMRL/Indus Research Centre application collection is frozen in data/raw/mahadevan_primary.json with a separate manifest of neutral field whitelist, page hashes, source update times and acquisition timestamps. Raw response pages remain in ignored cache; public numerical records retain original annotations. Paginated reads are not atomic; no refresh occurs during reproduction.

The separate secondary export is pinned at gkarun876/IVS revision 7c0273f544998178a4e4f71b80407c52d1ac2f24 with its MIT attribution retained in MAHADEVAN_SECONDARY_LICENSE.txt. It is an audit comparator only. No proposed phonetic anchors are ingested. Source page review and primary-vs-secondary code differences are recorded in docs/mahadevan_source_review.json. The original 1977 book scan stays local; catalogue links point to its sign-list pages. Numeric namespace M001-M417 has reserved PAD/UNK/BOS/EOS states and is not a crosswalk. Unknown-span slots do not imply one missing sign.

## Original CISI reference and photograph audit

The first M1-100 reference page of CISI 1 (printed p.366, PDF page402 in the frozen scan) is manually encoded in data/raw/cisi1_fc_candidates.json with hash/page and uncertain digits. data/raw/cisi1_fc_manifest.json fixes the numeric snapshot. These are literal FC numbers, not verified Mahadevan IDs; source text cautions against universal interchange. Candidate rejection and split ledgers remain in results/reference_candidates.json. Actual original/impression pages viewed are logged in docs/original_photo_review.json; scans and rendered pages remain private cache. No sign aliases select the candidates, and no correspondence is automatically propagated.

## Original Mahadevan graphic appendix and postscript

Frozen manual numeric transcription: data/raw/mahadevan_graphic_variants.json, with source PDF hash, printed/PDF pages, columns, source-family IDs, 641 literal example references and thirteen before/after digit corrections confirmed through enlarged source views. Separate manifest fixes its digest. The source's main615 forms/167 families plus addendum26/12 reproduce combined641/179. These source forms may include normal forms and are not extra independent signs.

Generated data/processed/mahadevan_graphic_catalog.json uses research IDs MV###-main-## or MV###-addendum-## and integers4..644 in the separate MahadevanGraphic1977 namespace. Postscript M418/M419 have codes421/422 under a distinct postscript reference namespace; existing 417-ID benchmark codes are unchanged. Always retain namespace with integer ID. Source-page links locate the drawn forms; raw raster pages are not redistributed.

results/graphic_variant_audit.json retains every citation lookup, candidate document/side/line/slot and original uncertainty. Unique lookup does not establish the drawn variant at that slot; all automatic_assignment flags are false. Repeated candidates, two parenthetical suffixes and five base-absence references remain unresolved. Count agreement is not independent proof of manual digit accuracy, allograph equivalence or phonetic value.

## Conditional-substitution inputs

data/substitution/inputs.json.gz freezes selected single writing-unit Unicode labels, 33-state unigram/bigram counts, exact/reverse document partition identities and opaque calibration-window ciphers/provenance. The uncompressed hash is checked before analysis; manifest also records the pinned source-inventory hash. Source texts and complete word dictionaries are not added. ATTRIBUTION.md preserves Tamil Apache-2.0 and adapted Vedic CC BY-SA4.0 credit/licenses. Units are normalization products, not historical phonemes. These artifacts support Experiment017; optional prepare_substitution.py reads already cached, hash-verified language sources. Default offline reproduction uses the frozen inputs.

## Full-source homophonic representation

Experiment 019 gives every distinct training glyph its own dense source index, then learns a conditional many-to-one key to the frozen 32-unit target inventory. ICIT split has 584 training types from 637 total; all 53 unseen types are explicitly listed without assigned values. Each exported key row carries the literal source ID and training count, never an asserted historical sound. Split source strings/component identities and per-test scores are retained. Normalized emissions account for the distinct glyphs; outputs are not equivalent to the earlier top32 recodings. Artificial 64-alias calibrations are derived from attributed input units/windows, not new ancient inscriptions; Vedic-derived adaptations retain the source ShareAlike terms documented in data/substitution/ATTRIBUTION.md.
