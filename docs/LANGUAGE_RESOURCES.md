# Candidate historical-language resources

Acquired and inspected 15 October 2026. This is preparation for comparative tests, not evidence identifying the language of the Indus signs. Raw candidate files are stored in ignored `.cache/languages`; only URLs, pinned revisions, hashes and metadata are committed. Reacquire with `python3 scripts/language_inventory.py`. This optional network operation is separate from offline Indus experiment reproduction.

## Classical Tamil

Source: [Sentamizh Corpus](https://github.com/indic-corpora/sentamizh-corpus), revision `e833395c0535915e82156ac9d912836cabec9a29`. The selected Akananuru file has 400 nonempty verses and Purananuru has 388. Use only `classical_tamil` for text modeling; discard translations and interpretive annotations. The repository declares Apache 2.0 and attributes original text editions to Project Madurai and other digitizations. The selected source metadata labels the texts 300 BCE-300 CE; that label is an upstream date range, not independently established dating of each verse.

Purananuru records point to two Project Madurai editions. The selected Akananuru records have null `source_url`; exact edition provenance remains incomplete despite repository-level attribution. Source audit metadata records this gap. The corpus is a later Dravidian-language proxy, not reconstructed Proto-Dravidian or a contemporary Indus-language corpus. Changes in morphology, phonology, spelling and literary genre must be addressed before interpreting similarity.

## Vedic Sanskrit

Source: [UD Sanskrit-Vedic](https://universaldependencies.org/treebanks/sa_vedic/index.html) and [repository](https://github.com/UniversalDependencies/UD_Sanskrit-Vedic), revision `09c59eed987f28c2fd3a9972b4b5437439f46832`. License: CC BY-SA 4.0. Credit the authors and annotators identified in the upstream README, including Oliver Hellwig, Salvatore Scarlata, Elia Ackermann, Paul Widmer, Erica Biagetti and Sven Sellmer. Preserve attribution and ShareAlike obligations if redistributing adapted data; this release packages no candidate language texts.

Parsed snapshot counts: 21,477 train, 2,996 development and 2,709 test sentence blocks; 161,959/23,862/20,619 syntactic word forms. These actual snapshot counts supersede the README's older 4,000-sentence summary for acquisition purposes. CoNLL-U FORM extraction excludes multiword-range IDs and empty nodes. The treebank represents selected Vedic poetry/prose; it is not a securely contemporaneous transcription of a language known to have been written in the Indus script.

## Required comparison protocol

1. Fix normalization, grapheme/akshara and word segmentation separately; neither Unicode codepoints nor word counts are equivalent to Indus sign counts.
2. Match short-text lengths, sample sizes and genre where possible, without treating literary verse snippets as authentic seal texts.
3. Preserve document/poem groups, original train/dev/test partitioning where relevant, and deduplicate overlapping resources.
4. Compare multiple unit representations and frequency/position-preserving nulls. A closest entropy curve cannot identify a language family.
5. Separate structural compatibility from constrained phonetic alignment, with chronology and external lexical evidence declared before translation tests.
6. Include competing language families and nonlinguistic controls. Two available resources do not exhaust possible languages.

Acquisition hashes and coverage are in `language_resource_inventory.json`. No cross-script alignment or phonetic assignments have been executed with these resources in release 0.3.
