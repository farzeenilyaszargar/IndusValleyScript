# Experiment 010: uncertainty-sensitive training on fixed clean holdouts

Recorded before model execution, 15 October 2026. Test whether adding annotated but uncertain/damaged sign readings changes structural prediction on the same clean holdouts. This does not validate the added readings or produce a decipherment.

Use eligible zero-damage/zero-uncertainty CISI objects to fix seed-42 exact/reverse-group train/validation/test partitions, matching Experiment 003. Never change clean validation/test objects between conditions. Broader objects must have nonempty single-line text, no P000 unknown stretch, and no short/default-vector problem. Do not infer how many signs an unknown stretch represents.

Compare (1) clean training only, (2) added objects whose literal raw damage code and uncertainty code are both <=25 at every position, and (3) all broader objects whose remaining exclusion is damage_or_uncertainty. The <=25 condition is a literal annotation-code filter, not a calibrated percentage: source damage fields can encode locations in higher digits. Keep raw values and reasons available. Added objects must be absent from clean validation/test by object ID and by canonical exact/reversed base sequence.

Fit a base-sign bigram per condition with strength 1/5/20/100 chosen from the same clean validation set. Evaluate the same clean test objects, including EOS and collapsed UNK, and group-bootstrap differences (1,000 resamples). Report train size, added object IDs, unknown test tokens and selected strength. Changes may reflect increased training coverage or different smoothing; no damaged reading is thereby proved correct.

Export an added-object uncertainty ledger and, as a separate source-consistency audit, examine equal-length uniquely identified ICIT/CISI pairs that pass all requirements except annotated damage/uncertainty. Compare reversed aligned numeric IDs to supplied Wells alias fields, reporting alias absence rather than calling it an error. Original glyphs, face equivalence and independent transcription are still unverified. This post-source-disagreement audit cannot automatically correct either corpus.
