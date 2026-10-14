# Experiment 003: allograph-aware history prediction

Design recorded before execution, 15 October 2026. Prior corpus summaries are already known; this is prospective analysis of an explored dataset.

Use every eligible annotated CISI side (zero damage/uncertainty, single line). Validate custom-vector lengths against the source feature schemas. Define a variant as Parpola base ID plus its custom morphology vector, excluding default damage, line and uncertainty fields. Export an integer variant inventory and per-side integer sequences without equating variants with independent graphemes.

Group identical and reversed base sequences in all splits. Retain eligible object occurrences, including base-identical variants, but keep them in the same partition. Use seeds 42-46, approximately 80/10/10 percent of base-sequence groups.

Predict the same next **base sign** in both models. The baseline is a base-ID bigram. The alternative conditions on the previous sign's observed morphology, interpolating to the base bigram for sparse or unseen variant histories. The target sign's own morphology must never be supplied to the predictor. Include EOS, collapse unseen base IDs to UNK identically, and select both base smoothing and variant-context smoothing from strengths 1/5/20/100 by validation loss only.

Report per-split scores, train/test variant coverage, paired exact/reverse-group bootstrap intervals, inventory sizes and all annotated descriptions/features. Small holds cannot confirm variant semantics. A gain would show extra predictive information in this representation; a failure would not establish that all variants are equivalent.

Historical language comparison source discovery proceeds separately; no historical language mapping is claimed by this test.
