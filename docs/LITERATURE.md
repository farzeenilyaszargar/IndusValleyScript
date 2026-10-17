# Literature review and evidence notes

Reviewed 15 October 2026. These are methodological notes, not endorsements of proposed decipherments. Reading scope is explicit. No claim is made to have surveyed every publication or read books unavailable in full text.

| Original research | Scope inspected | Idea used here | Caution |
|---|---|---|---|
| Yadav et al., *Statistical analysis of the Indus script using n-grams*, [2009 preprint](https://arxiv.org/html/0901.3017), related [2010 PLOS article](https://doi.org/10.1371/journal.pone.0009506) | Full-text corpus, modeling and evaluation sections | Deduplicate, exclude damaged/multiline texts, estimate smoothed transitions, predict hidden signs | Structural analysis does not establish semantics; our corpus and smoothing differ |
| Rao et al., *Entropic evidence for linguistic structure in the Indus script*, [Science 2009 and supplement](https://homes.cs.washington.edu/~rao/ScienceIndus.pdf) | Paper and methodological supplement | Conditional entropy, frequency-sensitive baselines | Entropy is sensitive to corpus selection, representation, and undersampling |
| Sproat, *Ancient Symbols, Computational Linguistics, and the Reviewing Practices of the General Science Journals*, [2010](https://aclanthology.org/J10-3012.pdf) | Full-text critique and counterexamples | Include structured alternatives; avoid interpreting entropy as a language detector | Neither random nor rigid extremes represent the full space of nonlinguistic systems |
| Rao et al., *Entropy, the Indus Script, and Language: A Reply to R. Sproat*, [2010](https://aclanthology.org/J10-4016.pdf) | Block-entropy and inductive-inference sections | Separate evidence of constraints from proof of language; consider higher-order models | The authors argue for cumulative evidence, not proof from entropy alone |
| Sinha et al., *Network analysis of a corpus of undeciphered Indus civilization inscriptions indicates syntactic organization*, [2010 preprint](https://arxiv.org/html/1005.4997) | Full-text introduction, data, and network methods | Directed adjacency graph and contextual sign similarity | Our implementation does not reproduce their segmentation-tree analysis; graph edges are not meanings |
| Parpola, *'Hind Leg' + 'Fish': Towards Further Understanding of the Indus Script*, [2009 author summary and paper link](https://www.harappa.com/content/hind-leg-fish-towards-further-understanding-indus-script) | Author summary, not complete PDF | Test sign combinations before assigning rebus values | The Proto-Dravidian fish/star reading is a hypothesis requiring independent lexical and archaeological anchors |
| Rao, *The Indus Script and Economics*, [2018](https://arxiv.org/abs/1812.00049) | Abstract and bibliographic record | Alternative ration/transaction interpretation of numeral-like combinations | This project has not reannotated the archaeological tablet sample |
| Palaniappan and Adhikari, *Deep Learning the Indus Script*, [2017](https://arxiv.org/abs/1702.00523) | Abstract and bibliographic record | Image recognition is a separate acquisition task from decipherment | OCR performance is not translation accuracy; no OCR experiment is reported here |
| Nair, *How Non-Linguistic Is the Indus Sign System? A Synthetic-Baseline Scorecard*, [2026 preprint](https://arxiv.org/html/2604.17828) | Full-text data, baseline, results and limitations sections | Multiple controls and sensitivity to allographs/duplicates | Preliminary preprint; its raw/deduplicated counts vary between passages. We compute our own counts and do not treat its numerical claims as validation |

## Additional sources for release 0.2

- Rao et al., [A Markov model of the Indus script, PNAS (2009), author-hosted PDF](https://raw.githubusercontent.com/ronojoy/indus/cab6c2d881307825f24d7ed28f7ad62de800ae13/papers/MarkovModelIndusScript.pdf): PMC access encountered a browser check; the author's repository supplied the paper and supplement. Inspected abstract, rationale, corpus and missing-sign prediction passages. The authors use an EBUDS subset excluding ambiguous/multiline/repeated texts and discuss predicting missing signs through a most-probable completion. Our explicit-stop HMM is an independent extension, not a replication of that paper. The inspected author repository contains papers but no machine-readable transcription dataset.
- Daggumati and Revesz, [A method of identifying allographs in undeciphered scripts and its application to the Indus Valley Script (2021)](https://www.nature.com/articles/s41599-021-00713-0): inspected abstract, data-source and direction/mirroring sections. The authors argue for merging certain mirrored/variant pairs using position and contextual evidence. Their proposals motivate allograph and orientation audits, but we have not adopted their proposed merges or established semantic equivalence. Visual review and independently verified crosswalks remain required.

## Representation references for release 0.4

- [Universal Dependencies CoNLL-U format](https://universaldependencies.org/format.html): inspected the token/word/empty-node conventions. Integer-ID rows supply syntactic word forms; multiword ranges and decimal empty nodes are different representations. Our extraction deliberately selects integer-ID non-punctuation FORM fields.
- [Unicode Text Segmentation, UAX #29](https://www.unicode.org/reports/tr29/): consulted the distinction between Unicode codepoints and grapheme segmentation. Our experiment uses a declared simpler letter-plus-mark scheme, not a claim of full UAX #29 conformance or phonetic syllabification. These are format/representation references, not decipherment evidence.

## Administrative interpretation reviewed for release 0.5

- Mukhopadhyay, [administrative interpretation of Indus inscriptions (2023)](https://www.nature.com/articles/s41599-023-02320-7): inspected the numerical notation, transaction-specific quantity and tax/license-rate argument passages. The author argues that restricted number/sign combinations and sealing contexts favour regulatory uses over individual-transaction quantities. This is a published interpretation, not an established translation. We test graphic-count/follower dependencies in a small annotated corpus; we do not reproduce the exact proposed sign classes or validate commodity meanings. Our count table lacks independent amounts/weights, and some frequently sampled followers admit several counts.

## Fish-rebus sources inspected for release 0.9

- Parpola, [A Dravidian solution to the Indus script problem (2010)](https://www.harappa.com/sites/default/files/pdf/Parpola-2010-Coimbatore.pdf): inspected preparation, fish/star and named H-9/M-112 example passages. The author proposes astronomical rebus readings with Old Tamil lexical parallels. Our named-example checks match one graphic sequence and expose a transcription subtype disagreement in another; they do not verify proposed phonetic values or astronomical semantics.
- Mahadevan, [The Indus Fish Swam in the Great Bath (2011)](https://www.harappa.com/content/indus-fish-swam-great-bath): inspected the constellation-extension and critique passages (PDF pp.9-11), where broader number/sign patterns and modified-fish difficulties motivate reappraisal. No alternative meaning from this work is adopted. Direct PDF downloads returned HTTP 403; web-tool document access supplied the inspected text. No complete full-text reading or original-object image review is claimed.

## Foundational catalogue access and limits

Mahadevan's 1977 concordance; Parpola and collaborators' CISI volumes; Wells's inventories and ICIT documentation. They are foundational sources behind the digitizations, but a repository's attribution does not establish photographic verification of each entry. Catalogue identity and crosswalks require epigraphic review.

## Working language hypotheses

Proto-Dravidian logo-syllabic readings, Indo-Aryan/Indo-Iranian readings, Austroasiatic proposals, a lost language family, and administrative or mixed-register systems remain alternative explanations. No family has been selected by the experiments here. Modern surnames, unconstrained rebuses, and visual resemblance to Brahmi are insufficient external anchors.

Experiment 011 implements an independent exact one/two-sign synthetic-gap benchmark motivated by the previously inspected Markov missing-sign passages. It uses different source data and smoothing, includes all training glyphs as candidates, and retains unseen truths as failures. It does not replicate any published completion of an original damaged object.

- Raghavendra, [On the Non-Specificity of Statistical Measures Used in Script Decipherment](https://arxiv.org/html/2608.02999v1), 2026 preprint: selected construction, prediction, lexical-stress and limitations passages inspected. Motivates our independently authored administrative control; reported outcomes are not replicated. See RECENT_RESEARCH_AUDIT.md for retrieval attempts and limits.

- Mahadevan, *The Indus Script: Texts, Concordance and Tables* (ASI 1977): printed code/sign-list pages 30-35 visually inspected in the [public original scan](https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan). Verified side/line and direction code definitions and 417 sign-list page references, not original-object photographs or readings. The [official Indus Research Centre application](https://indusscript.in) supplied the frozen neutral numerical snapshot for Experiment 013.

- Joshi and Parpola (eds.), *Corpus of Indus Seals and Inscriptions 1: Collections in India* (1987): inspected printed metadata pp.365-366 and original/impression photographs pp.1-3 in the public source scan. The FC/Mahadevan-number caution motivates Experiment015's tentative status; the photographic screening is explicitly unblinded and incomplete, not an expert transcription.

- Mahadevan (1977), introduction §11.4 and postscript §16.3-16.4, plus the complete graphic-variant appendix pp.785-792: read the source-defined distinction between sign and graphic form, variant occurrence examples and postscript additions. Experiment016 indexes the complete drawn-form list with explicit manual-transcription limits; source grouping is attributed rather than adopted as proven sound equivalence.

- Knight et al., [Unsupervised Analysis for Decipherment Problems](https://aclanthology.org/P06-2065/), 2006: inspected selected sections 2/3/5, including letter substitution, noisy-channel modeling and a known Spanish phonetic calibration. Their EM/Viterbi procedure is not replicated. Experiment017 independently uses a small bijective bigram search and explicit known-key calibration.

- Luo, Cao and Barzilay, [Neural Decipherment via Minimum-Cost Flow: From Ugaritic to Linear B](https://aclanthology.org/P19-1303/), 2019: inspected selected sections 2-3 and stated cognate, related-language and correspondence assumptions. Those anchors are absent here; our conditional writing-unit search is not their neural/cognate alignment method or a replication of its outcomes.
