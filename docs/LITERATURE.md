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

## Foundational catalogues to obtain and verify directly

## Additional sources for release 0.2

- Rao et al., [A Markov model of the Indus script, PNAS (2009)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2721819/): accessible indexed abstract/method summaries motivate grammar induction. Direct PMC page access encountered a browser check; full-text reading was not completed in this extension. Our explicit-stop HMM experiment is an independent model test rather than replication of that paper.
- Daggumati and Revesz, [A method of identifying allographs in undeciphered scripts and its application to the Indus Valley Script (2021)](https://www.nature.com/articles/s41599-021-00713-0): inspected abstract, data-source and direction/mirroring sections. The authors argue for merging certain mirrored/variant pairs using position and contextual evidence. Their proposals motivate allograph and orientation audits, but we have not adopted their proposed merges or established semantic equivalence. Visual review and independently verified crosswalks remain required.

## Foundational catalogue access

Mahadevan's 1977 concordance; Parpola and collaborators' CISI volumes; Wells's inventories and ICIT documentation. They are foundational sources behind the digitizations, but a repository's attribution does not establish photographic verification of each entry. Catalogue identity and crosswalks require epigraphic review.

## Working language hypotheses

Proto-Dravidian logo-syllabic readings, Indo-Aryan/Indo-Iranian readings, Austroasiatic proposals, a lost language family, and administrative or mixed-register systems remain alternative explanations. No family has been selected by the experiments here. Modern surnames, unconstrained rebuses, and visual resemblance to Brahmi are insufficient external anchors.
