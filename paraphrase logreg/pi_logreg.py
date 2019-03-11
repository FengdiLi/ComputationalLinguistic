import argparse
import numpy as np
from nltk import word_tokenize
from nltk.translate.nist_score import sentence_nist
from nltk.translate.bleu_score import sentence_bleu
from nltk.metrics.distance import edit_distance
from sklearn.linear_model import LogisticRegression


def load_sts(sts_data):
    """Read a dataset from a file in STS benchmark format"""
    # read the dataset
    texts = []
    labels = []

    with open(sts_data, 'r', encoding = 'utf8') as dd:
        for line in dd:
            fields = line.strip().split("\t")
            labels.append(float(fields[4]))
            t1 = fields[5].lower()
            t2 = fields[6].lower()
            texts.append((t1,t2))

    labels = np.asarray(labels)

    return texts, labels


def sts_to_pi(texts, labels, min_paraphrase=4.0, max_nonparaphrase=3.0):
    """Convert a dataset from semantic textual similarity to paraphrase.
    Remove any examples that are > max_nonparaphrase and < min_nonparaphrase.
    labels must have shape [m,1] for sklearn models, where m is the number of examples"""
    # get an array of the rows where the labels are in the right interval
    # I like this numpy
    pi_rows = np.where(np.logical_or(labels>=min_paraphrase, labels<=max_nonparaphrase))[0]
    # here's a loop if you don't like numpy
    # pi_rows = [i for i,label in enumerate(labels) if label >=min_paraphrase or label<=max_nonparaphrase]
    pi_texts = [texts[i] for i in pi_rows]

    # print(f"{len(pi_texts)} sentence pairs kept")
    # using indexing to get the right rows out of labels
    pi_y = labels[pi_rows]
    # convert to binary using threshold (1/0 integers)
    pi_y = (pi_y > max_nonparaphrase).astype(int)

    return pi_texts, pi_y


def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None] * (n + 1) for i in range(m + 1)]
    result = 0

    """Following steps build L[m + 1][n + 1] in bottom up fashion 
    Note: L[i][j] contains length of LCS of X[0..i-1] 
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
                result = max(result, L[i][j])
            else:
                L[i][j] = 0
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return result


def load_X(sent_pairs):
    """Create a matrix where every row is a pair of sentences and every column in a feature.
    Feature (column) order is not important to the algorithm."""

    features = ["NIST", "BLEU", "Word Error Rate", "Longest common substring", "Levenshtein distance"]
    X = np.zeros((len(sent_pairs), len(features)))
    NIST = 0
    BLEU = 1
    WER = 2
    LCS = 3
    LD = 4
    for i, pair in enumerate(sent_pairs):
        t1, t2 = pair
        t1_token = word_tokenize(t1)
        t2_token = word_tokenize(t2)
        # print(f"Sentences: {t1}\t{t2}")
        # calculate the scores
        ed = edit_distance(t1_token, t2_token)
        X[i, WER] = ed / len(t1_token) + ed / len(t2_token)
        try:
            X[i, NIST] = sentence_nist([t1_token], t2_token) + sentence_nist([t2_token], t1_token)
        except ZeroDivisionError:
            X[i, NIST] = 0
        X[i, BLEU] = sentence_bleu([t1_token], t2_token) + sentence_bleu([t2_token], t1_token)
        X[i, LCS] = lcs(t1, t2)
        X[i, LD] = edit_distance(t1, t2)

    return X


def main(sts_train_file, sts_dev_file):
    """Fits a logistic regression for paraphrase identification, using string similarity metrics as features.
    Prints accuracy on held-out data. Data is formatted as in the STS benchmark"""

    min_paraphrase = 4.0
    max_nonparaphrase = 3.0

    # loading train
    train_texts_sts, train_y_sts = load_sts(sts_train_file)
    train_texts, train_y = sts_to_pi(train_texts_sts, train_y_sts,
      min_paraphrase=min_paraphrase, max_nonparaphrase=max_nonparaphrase)

    train_X = load_X(train_texts)

    # loading dev
    dev_texts_sts, dev_y_sts = load_sts(sts_dev_file)
    dev_texts, dev_y = sts_to_pi(dev_texts_sts, dev_y_sts,
      min_paraphrase=min_paraphrase, max_nonparaphrase=max_nonparaphrase)

    dev_X = load_X(dev_texts)

    print(f"Found {len(train_texts)} training pairs")
    print(f"Found {len(dev_texts)} dev pairs")

    print("Fitting and evaluating model")
    clf = LogisticRegression().fit(train_X, train_y)
    pred = clf.predict(dev_X)
    print(f'Model accuracy on dev: {np.mean(pred == dev_y)}')
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sts_train_file", type=str, default="stsbenchmark/sts-train.csv",
                        help="train file")
    parser.add_argument("--sts_dev_file", type=str, default="stsbenchmark/sts-dev.csv",
                        help="dev file")
    args = parser.parse_args()

    main(args.sts_train_file, args.sts_dev_file)
