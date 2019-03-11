Semantic textual similarity using string similarity
---------------------------------------------------

This project examines string similarity metrics for semantic textual similarity.
Though semantics go beyond the surface representations seen in strings, some of these
metrics constitute a good benchmark system for detecting STS.


Data is from the [STS benchmark](http://ixa2.si.ehu.es/stswiki/index.php/STSbenchmark).


## sts_pearson.py

`sts_pearson.py` reads the STS test dataset by default, and extracts its sentence pairs and corresponding labels. 
For each sentence pair in the STS dataset, `sts_pearson.py` implements basic string pre-processing, and uses built-in functions in `nltk` and self-defined functions to calculate:
 * NIST score: Precision based arithmetic mean of n-gram overlap, weighted by frequency, penalized if hypothesis string is short 
 * BLEU score: Precision based geometric mean of n-gram overlap, penalized if hypothesis string is short
 * Word Error Rate (WER): Levenshtein distance divided by Number of words in reference string
 * Longest Common Subsequence (LCS): Length of the longest common substring between strings
 * Levenshtein distance: Minimum edit distance between strings

Then, it uses `scipy` to calculate the Pearson Correlation between the label score and these five types of scores, and writes the result to file. 

Example usage:

`python sts_pearson.py --data stsbenchmark/sts-test.csv --output_file test_output.txt`

## test_output.txt

`test_output.txt` contains the semantic textual similarity correlation results for stsbenchmark/sts-test.csv. 
For each type of string similarity metrics, the lower-tail Pearson Correlation Coefficient with the corresponding label score was reported.
