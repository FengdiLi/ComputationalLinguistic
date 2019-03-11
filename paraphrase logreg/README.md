Paraphrase Identification using string similarity
---------------------------------------------------

This project examines string similarity metrics for paraphrase identification.
It converts semantic textual similarity data to paraphrase identification data using threshholds.
Though semantics go beyond the surface representations seen in strings, some of these
metrics constitute a good benchmark system for detecting paraphrase.


Data is from the [STS benchmark](http://ixa2.si.ehu.es/stswiki/index.php/STSbenchmark).

Instructor repository at <https://github.com/emmerkhofer/paraphrase_logreg> . 

## pi_logreg.py

`pi_logreg.py` converts a STS train and dev datasets to PI feature and label pairs, those features include: 

* NIST score: Precision based arithmetic mean of n-gram overlap, weighted by frequency, penalized if hypothesis string is short
* BLEU score: Precision based geometric mean of n-gram overlap, penalized if hypothesis string is short
* Word Error Rate (WER): Levenshtein distance divided by Number of words in reference string
* Longest Common Subsequence (LCS): Length of the longest common substring between strings
* Levenshtein distance: Minimum edit distance between strings

Then it builds a logistic regression model on converted train dataset using `sklearn` 
and reports the model accuracy score testing on converted dev dataset.

Example usage:

`python pi_logreg.py --sts_train_file stsbenchmark/sts-train.csv --sts_dev_file stsbenchmark/sts-dev.csv`

## Results

This system scores 0.852 (85.2%) accuracy on dev dataset, which indicates the basic logistic regression model has a good performance. 
