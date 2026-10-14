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

The public glyph index has 715 non-placeholder IDs. The raw ICIT export contains 712 observed non-placeholder IDs, with seven not in that index. The Parpola description catalogue contains 395 non-damage entries. These counts describe these sources, not the number of distinct signs in the civilization. Lists differ in how they split allographs and compound signs. Cross-reference fields are attributed source proposals, not a validated merge table. Do not equate a Wells W-ID, ICIT numeric ID, and Parpola P-ID without checking actual glyphs.

## Limits on inferred independence

Exact and reversed texts are grouped in train/validation/test splits. This prevents one obvious leakage mode but does not group every artifact family, shared mold, copied formula, or near duplicate. Site holds exclude sequences attested in the target site, using all eligible raw rows rather than only the first deduplicated record.
