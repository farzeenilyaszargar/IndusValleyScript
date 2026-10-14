# Experiment 008: metadata-conditioned formula models

Recorded before model execution, 15 October 2026, after inspecting source type/site counts. Test whether observed archaeological metadata adds prediction beyond pooled sign-order constraints. This is not a language-identity or translation test.

Use all 3,591 eligible complete single-line ICIT-export rows. Retain duplicate artifact occurrences and their metadata, but group exact/reversed sign strings in the same partition. Use seed 42 and approximately 80/10/10 percent of text groups. Report actual row counts and per-type held-out results. This differs from the deduplicated main benchmark; compare models only within this new split.

Define coarse type as the source `type` prefix before the colon (e.g., SEAL, TAB, POT); do not infer meanings for suffix codes. Compare pooled bigram and three alternatives conditioning previous-sign counts on (1) coarse type, (2) site, (3) site plus coarse type. Interpolate sparse metadata contexts to the pooled bigram. Select pooled and metadata smoothing strengths independently from 1/5/20/100 by validation loss only. Metadata is supplied at prediction time, as it would be observable from an excavated object's record. Target signs and interpretive translations/classes are not supplied as metadata.

Score signs plus EOS with training-only vocabulary and collapsed UNK, identical across model conditions. Report all-position token loss and unknown test tokens; do not interpret this as translation accuracy. Paired bootstrap resamples whole exact/reversed groups 1,000 times. Report both 95% intervals and 98.33% intervals as a three-comparison Bonferroni sensitivity. The overlapping models and archaeological dependencies are not independent discoveries.

A positive gain would support metadata-conditioned formulas or usage differences, not noun/verb categories, commodity names, sound values, dialects, or language families. Exact grouping does not remove all mold, family or near-copy relationships. Duplicate weighting, uneven sites, and uncertain source type annotations remain limitations.
