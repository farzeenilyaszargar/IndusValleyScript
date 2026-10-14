# Indus script research workbench

An ongoing, reproducible investigation of Indus sign structure and decipherment hypotheses. **No decipherment is claimed.** Numeric sign identifiers and statistical embeddings are representations, not phonetic values or translations.

The research separates catalogues, uncertain transcriptions, structural patterns, and semantic hypotheses. It excludes proposed translations from computational input. Progress, failures, and pending methods are recorded in `docs/METHODS.md`; the evolving research paper is in `docs/PAPER.md`.

## Research milestones

1. Pin and audit public transcription sources and sign inventories.
2. Export numeric encodings and annotated sign catalogue.
3. Evaluate sequence models with deduplication, held-out data, and null controls.
4. Learn distributional sign representations and propose structural classes.
5. Test constrained language and administrative hypotheses against external evidence.
6. Maintain the paper and incrementally push results.

Complete acquisition of every excavated sign and successful decipherment are open objectives; available public digitizations do not establish exhaustive coverage.

## Results and artifacts

- [Results snapshot](results/SUMMARY.md)
- [Research paper](docs/PAPER.md) and [PDF](output/pdf/indus_structural_research.pdf)
- [Methods and failures](docs/METHODS.md)
- [Searchable catalogue](docs/SIGN_CATALOGUE.html) (download and open locally; remote images require network access)
- [Data audit](docs/DATA.md), [literature](docs/LITERATURE.md), [remaining hypotheses](docs/HYPOTHESES.md)

Release 0.2: 2,156 complete distinct sequences, 9,221 tokens, 637 clean-subset IDs; 715 verified glyph references cover all 712 raw observed IDs. Separate Parpola catalogue: 395 descriptions. Namespaces are not merged.

Mean held-out loss improves from 6.450 unigram to 5.452 bigram bits/token, including EOS and a collapsed unknown-sign event. This measures sequence predictability, not translation. No phonetic key or language family has been identified.

The [hidden-state and near-copy extension](docs/EXPERIMENT_002.md) finds that a validation-selected 8-state HMM is worse than bigrams (5.919 vs 5.461 bits/token). Grouping one-substitution neighbours preserves a 0.922-bit bigram advantage over unigrams. These are predictive constraints and negative model results, not decipherments.

## Reproduce

Python 3.14 was used; analytical scripts require only the standard library.

```sh
python3 scripts/reproduce.py --check
```

This verifies snapshot hashes, runs correctness tests, rebuilds artifacts and checks equivalent JSON. Counts, IDs, labels and structure must match exactly; floating-point values use absolute/relative tolerance 1e-12 across platforms. Fresh network acquisition uses `python3 scripts/acquire.py`, followed by `python3 scripts/reproduce.py`. Git is needed for reacquisition of the pinned CISI source.

For optional PDF export, install ReportLab and run `python3 scripts/paper_pdf.py`. The Markdown paper is generated from result files by `scripts/report.py`. Review PDF layout after substantive changes.

Attribution and inherited-material limits are documented in DATA.md. Proposed translations are excluded from training. Externally hosted image/font assets are not bundled.
