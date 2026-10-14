# Experiment 006: paired-object catalogue correspondence

Recorded before running sign-correspondence inference, 15 October 2026, after inspecting a few object-ID join examples. This experiment establishes candidate **catalogue correspondences**, not phonetic values.

Join eligible first-face CISI IDs matching `M-numberA` to ICIT-export object label `M-number`, restricted to Mohenjo-daro. Require exactly one source row for that label, a complete single-line transcription in each source and equal token lengths. Exclude missing, ambiguous, damaged and unequal-length pairs; retain a rejection ledger. This does not independently verify face equivalence, object identification, copying, segmentation or glyphs.

Group pairs connected by exact/reversed text identity in either catalogue. Split the connected groups 80/10/10 by group count using seed 42. Use training pairs only to select direct versus reversed ICIT alignment by lower conditional entropy H(Parpola ID | ICIT ID) over aligned positions; break ties deterministically in favour of direct. Validation data are reserved for reporting, not used to select individual exceptions or mappings. Fit empirical ICIT-to-Parpola candidate distributions on training pairs. Evaluate known-ID coverage, majority top-1 accuracy and probabilistic log loss on unused validation/test objects; unknown IDs remain explicit failures, not guessed mappings.

An initial “review-priority” mapping may be listed only if it has at least three training occurrences on at least two objects and >=90% agreement on a single Parpola ID. This is a shortlist for independent glyph review, not a verified crosswalk. Conflicts, allograph-specific distinctions, and unsuccessful objects remain visible. No source `xlits` canonical or sound assignments may be used.

Preserve object IDs, aligned positions, morphology and candidate support. Do not merge namespaces automatically or propagate descriptions to the full ICIT inventory based solely on a training fit. High held-out correspondence would support data integration only; shared catalogue ancestry and local transcription errors limit independence.
