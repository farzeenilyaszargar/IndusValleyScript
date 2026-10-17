# Candidate historical-language resources

Acquired and inspected 15 October 2026. These resources support comparative tests, not evidence identifying the language of the Indus signs. Raw candidate files are stored in ignored `.cache/languages`. URLs, pinned revisions, hashes and metadata are committed, along with opaque derived numeric samples in `data/language_samples` under their attributed licenses. Reacquire raw files with `python3 scripts/language_inventory.py`; regenerate sampling with `python3 scripts/language_compare.py --sample`. These optional network/source steps are separate from offline metric reproduction.

## Classical Tamil

Source: [Sentamizh Corpus](https://github.com/indic-corpora/sentamizh-corpus), revision `e833395c0535915e82156ac9d912836cabec9a29`. The selected Akananuru file has 400 nonempty verses and Purananuru has 388. Use only `classical_tamil` for text modeling; discard translations and interpretive annotations. The repository declares Apache 2.0 and attributes original text editions to Project Madurai and other digitizations. The selected source metadata labels the texts 300 BCE-300 CE; that label is an upstream date range, not independently established dating of each verse.

Purananuru records point to two Project Madurai editions. The selected Akananuru records have null `source_url`; exact edition provenance remains incomplete despite repository-level attribution. Source audit metadata records this gap. The corpus is a later Dravidian-language proxy, not reconstructed Proto-Dravidian or a contemporary Indus-language corpus. Changes in morphology, phonology, spelling and literary genre must be addressed before interpreting similarity.

## Vedic Sanskrit

Source: [UD Sanskrit-Vedic](https://universaldependencies.org/treebanks/sa_vedic/index.html) and [repository](https://github.com/UniversalDependencies/UD_Sanskrit-Vedic), revision `09c59eed987f28c2fd3a9972b4b5437439f46832`. License: CC BY-SA 4.0. Credit the authors and annotators identified in the upstream README, including Oliver Hellwig, Salvatore Scarlata, Elia Ackermann, Paul Widmer, Erica Biagetti and Sven Sellmer. Preserve attribution and ShareAlike obligations if redistributing adapted data; this release packages no candidate language texts.

Parsed snapshot counts: 21,477 train, 2,996 development and 2,709 test sentence blocks; 161,959/23,862/20,619 syntactic word forms. These actual snapshot counts supersede the README's older 4,000-sentence summary for acquisition purposes. CoNLL-U FORM extraction excludes multiword-range IDs and empty nodes. The treebank represents selected Vedic poetry/prose; it is not a securely contemporaneous transcription of a language known to have been written in the Indus script. Numeric derived Vedic samples retain CC BY-SA 4.0 attribution and licensing; source texts and token dictionaries are not packaged.

## Required comparison protocol

1. Fix normalization, grapheme/akshara and word segmentation separately; neither Unicode codepoints nor word counts are equivalent to Indus sign counts.
2. Match short-text lengths, sample sizes and genre where possible, without treating literary verse snippets as authentic seal texts.
3. Preserve document/poem groups, original train/dev/test partitioning where relevant, and deduplicate overlapping resources.
4. Compare multiple unit representations and frequency/position-preserving nulls. A closest entropy curve cannot identify a language family.
5. Separate structural compatibility from constrained phonetic alignment, with chronology and external lexical evidence declared before translation tests.
6. Include competing language families and nonlinguistic controls. Two available resources do not exhaust possible languages.

Acquisition hashes and coverage are in `language_resource_inventory.json`. Release 0.4 executes the representation-sensitivity experiment described in EXPERIMENT_004.md: matched word samples put Sanskrit closer to Indus conditional entropy, while matched letter-plus-mark samples put Tamil closer. This rank reversal prevents interpreting that distance as family identification. That release made no unit substitutions. Release 0.17 executes a conditional 32-unit substitution search (EXPERIMENT_017.md), with known artificial ciphers and a nonphonetic control. No historical sound assignment is validated. Attributed numeric inputs and single-unit labels are packaged in data/substitution; adapted Vedic data retain CC BY-SA 4.0.

The parsed Vedic sample pool includes 27,182 nonempty sentence documents with citation labels across many texts, including ṚV (4,352), AVŚ (2,175), AB (2,018), ŚBM (1,239), BĀU (1,044), ChU (874), and later strata such as KauśS. It is not exclusively a Rigvedic corpus. The numeric sample metadata retains these labels for future genre/stratum sensitivity. The current comparison aggregates them and cannot claim a historically uniform language stage.

Release 0.19 reuses the same 32-unit target counts for a normalized homophonic glyph channel with all training source types. Successful 64-alias artificial recovery does not remedy missing target units or historically mismatched literary sources; Indus fits lose to generic source unigram and bigram baselines. Source breadth and target phonological adequacy are separate requirements. No sound assignment is validated.

Release 0.20 adds stored/reverse-stored sensitivity with fixed target profiles and validation-only joint key/order selection. Neither Indus proxy beats the validation-directed generic sign bigram. Artificial controls recover their original order and key, but the literary proxies still do not establish historical direction or family identity. This extension does not expand the 32-unit target inventory.

Release 0.21 packages complete model-document unit counts and the same held windows in data/full_target. Global Tamil 233/Vedic 38 types become 225/37 model types plus 8/1 held-only types. Held-token coverage rises to 99.98994%/99.99978%; every original 32-unit aggregate and window matches exactly. Three Tamil-field Latin singleton letters occur only in held documents. Expanded artificial-cipher training lacks 27 Tamil/one Vedic true units, so its correct observed-training key violates the old all-target-units-occupied requirement. No expanded decoder is fitted yet; see EXPERIMENT_021.md and source attribution.
