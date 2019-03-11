import argparse
from nltk import word_tokenize
from nltk.translate.nist_score import sentence_nist
from nltk.translate.bleu_score import sentence_bleu
from nltk.metrics.distance import edit_distance
from scipy.stats import pearsonr

def lcs(X, Y): 
    # find the length of the strings 
    m = len(X) 
    n = len(Y) 
  
    # declaring the array for storing the dp values 
    L = [[None]*(n + 1) for i in range(m + 1)] 
    result = 0
  
    """Following steps build L[m + 1][n + 1] in bottom up fashion 
    Note: L[i][j] contains length of LCS of X[0..i-1] 
    and Y[0..j-1]"""
    for i in range(m + 1): 
        for j in range(n + 1): 
            if i == 0 or j == 0 : 
                L[i][j] = 0
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1]+1
                result = max(result, L[i][j])
            else: 
                L[i][j] = 0
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1] 
    return result

def main(sts_data, output_file):
    """Calculate pearson correlation between semantic similarity scores and string similarity metrics.
    Data is formatted as in the STS benchmark"""

    # score_types = ["NIST", "BLEU", "Word Error Rate", "Longest common substring", "Levenshtein distance"]

    # read the dataset
    texts = []
    labels = []

    with open(sts_data, 'r', encoding = 'utf8') as dd:
        for line in dd:
            fields = line.strip().split("\t")
            labels.append(float(fields[4]))
            t1 = fields[5].lower()
            t2 = fields[6].lower()
            texts.append((t1, t2))

    print(f"Found {len(texts)} STS pairs")

    NIST = []
    BLEU = []
    WER = []
    LCS = []
    LD = []
    for i, pair in enumerate(texts):
        t1, t2 = pair
        t1_token = word_tokenize(t1)
        t2_token = word_tokenize(t2)
        # print(f"Sentences: {t1}\t{t2}")
        # calculate the scores
        ed = edit_distance(t1_token, t2_token)
        WER.append(ed/len(t1_token)+ed/len(t2_token))
        try:
            NIST.append(sentence_nist([t1_token],t2_token)+sentence_nist([t2_token],t1_token))           
        except ZeroDivisionError:
            NIST.append(0)
        BLEU.append(sentence_bleu([t1_token],t2_token)+sentence_bleu([t2_token],t1_token))
        LCS.append(lcs(t1, t2))
        LD.append(edit_distance(t1, t2))

    result = dict()
    result['NIST correlation'] = round(pearsonr(labels, NIST)[0], 3)
    result['BLEU correlation'] = round(pearsonr(labels, BLEU)[0], 3)
    result['Word Error Rate correlation'] = round(pearsonr(labels, WER)[0], 3)
    result['Longest common substring correlation'] = round(pearsonr(labels, LCS)[0], 3)
    result['Levenshtein distance correlation'] = round(pearsonr(labels, LD)[0], 3)

    with open(output_file, 'w') as out:
        out.write(f"Semantic textual similarity for {sts_data}\n")
        # TODO: write scores. See example output for formatting
        for metric, corr in result.items():
            out.write(f'{metric}: {corr}\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sts_data", type=str, default="stsbenchmark/sts-test.csv",
                        help="tab separated sts data in benchmark format")
    parser.add_argument("--output_file", type=str, default="test_output.txt",
                        help="report on string similarity ")
    args = parser.parse_args()

    main(args.sts_data, args.output_file)
