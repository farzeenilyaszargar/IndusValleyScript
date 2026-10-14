# Experiment 002: hidden-state grammar and near-copy robustness

Design recorded before executing these experiments, 15 October 2026. This is a prospective extension of an already explored corpus, not independent preregistration or fresh archaeological evidence.

## Hidden-state grammar

Fit generative hidden Markov models (HMMs) to the existing seed-42 train split, retaining exact/reverse grouping. Use 2, 4, or 8 hidden states; random initialization seeds 17 and 29; checkpoints at 5, 10, and 20 EM iterations. Select state count, initialization and checkpoint using validation loss only. Test the selected model once on the same held-out inscriptions used by the bigram benchmark.

Include explicit stop probabilities so variable-length likelihood is comparable to EOS-inclusive n-gram loss. Use all training sign IDs plus an unknown event, with unseen test IDs collapsed to unknown as in the baseline. Emission prior strength 5, start and transition/stop pseudo-count 0.5. Export the selected parameters and training posterior profiles. Hidden states are abstract roles; they do not denote sounds, words, or semantic classes.

Success for predictive modeling means positive improvement over a validation-selected bigram and a paired exact/reverse-group bootstrap interval excluding zero. Failure is informative: a tested compact latent grammar need not improve short-text prediction. Neither outcome constitutes decipherment.

## Near-copy leakage sensitivity

Create connected components over canonical exact/reversed sequences with minimum length 3, linking equal-length strings that differ by one sign in either orientation. Do not join different-length or singleton/two-sign texts through this criterion. Split components approximately 80/10/10 by number of components using seed 42, report actual text proportions, and compare validation-selected unigram/bigram models. Report component sizes and the fraction of conventional seed-42 test texts with a one-sign neighbour in training.

This intentionally groups similarity, not archaeologically verified molds or object families. It may group genuinely distinct linguistic forms. Compare within the new split and do not interpret differences from the old split as a causal estimate of leakage. Preserve the component assignment for auditing.

## Reference motivation

Rao et al., [A Markov model of the Indus script (PNAS, 2009)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2721819/), motivates statistical grammar induction while maintaining a distinction between constraints and decipherment. [A method of identifying allographs in undeciphered scripts and its application to the Indus Valley Script (2021)](https://www.nature.com/articles/s41599-021-00713-0) motivates caution about sign variants and writing direction; contextual similarity alone will not be used to merge signs here.
