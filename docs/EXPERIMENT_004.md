# Experiment 004: controlled representation sensitivity across language proxies

Recorded before running this comparison, 15 October 2026. Indus corpus statistics and resource coverage are already known; this is not independent preregistration or a decipherment test.

## Question

Does a language proxy's apparent closeness to Indus conditional entropy depend on the written unit? Compare Classical Tamil and Vedic Sanskrit as (1) word-form sequences and (2) conservative letter-plus-mark clusters. Neither unit is assumed equivalent to an Indus sign. Do not fit phonetic values or use semantic translations in this experiment.

## Inputs and normalization

Verify cached candidate files against docs/language_resource_inventory.json hashes. Tamil uses only original classical_tamil from Akananuru/Purananuru, each verse a separate document. Vedic Sanskrit uses integer-ID CoNLL-U FORM fields, excluding empty nodes, multiword-range IDs and punctuation; each sentence remains a separate document. Preserve upstream split and citation metadata in the audit, but use all splits for this descriptive sampling test, not predictive training/test evaluation. Treat corpus transcription and later chronology as limitations.

Normalize to NFC, lowercase alphabetic text, retain marks attached to letters, discard formatting characters and punctuation. Word tokens are runs of Unicode letters/marks. Cluster tokens consist of an NFD base letter with following Unicode category-M marks, recomposed to NFC. This deliberately simple representation is not full Unicode extended grapheme segmentation, phonetic syllabification, or Sanskrit akshara parsing. Spaces separate words but are omitted from the cluster stream; never join documents.

## Sampling and controls

Match the complete unique Indus sample's exact ordered inscription length list, hence 2,156 texts and 9,221 tokens per sample. For each requested length, uniformly select an eligible source document and uniformly select a contiguous window. Sampling uses replacement; report duplicate windows and represented documents. Execute seeds 17-26 for all four language/unit combinations. No deduplication after sampling, since this would invalidate exact length matching; report an equal-sized source-frequency shuffle control and 49 global frequency-preserving permutations per sample.

Calculate raw empirical conditional entropy, unigram entropy, vocabulary size, hapax fraction, and difference from mean shuffled conditional entropy. Report distance from observed Indus conditional entropy, and compare ordering of Tamil versus Sanskrit within each representation. A nearest curve is a descriptive distance, not a language-family classification. Use matching 49-permutation controls for Indus as a separate comparison; sparse plug-in bias differs with vocabulary and remains a limitation.

## Reproducibility and evidence boundaries

Store sampled **opaque numeric sequences**, an ID-to-token map, document IDs, offsets, normalizations, counts and checksums in local cache for independent audit. Commit derived samples only if their license/attribution terms are carried with them. Keep this resource-dependent experiment separate from the network-free main pipeline until adequate licensed reproducibility inputs are packaged. Full candidate documents and translations must not be copied into analytical output.

Success means determining whether representational choices materially alter apparent structural similarity; it does not mean identifying the Indus language. If both representations agree, still do not infer ancestry or a phonetic key from entropy. Future constrained alignment requires external anchors and competing-family/null tests.
