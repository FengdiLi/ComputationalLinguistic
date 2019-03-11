#!/usr/bin/env python
import argparse
import numpy as np

def load_function_words(resource_path):
    """load a newline separated text file of function words.
    Return a list"""
    f_words = []
    with open(resource_path, 'r') as f:
        for line in f:
            if line.strip():
                f_words.append(line.lower().strip())
    return f_words


# TODO: write this function
def split_dataset(X, y, hold_out_percent):
    """shuffle and split the dataset. Returns two tuples:
    (X_train, y_train, train_indices): train inputs
    (X_val, y_val, val_indices): validation inputs"""
    split = round(X.shape[0]*hold_out_percent)
    temp = np.column_stack((X,y,np.arange(X.shape[0])))
    np.random.seed(0) # the random seed can be removed if different results are requested
    np.random.shuffle(temp)
    X_train, y_train, train_indices = temp[:split,:-2], temp[:split,-2], temp[:split,-1]
    X_val, y_val, val_indices = temp[split:,:-2], temp[split:,-2], temp[split:,-1]
    return ((X_train, y_train, train_indices), (X_val, y_val, val_indices))



def main(data_file, vocab_path):
    """extract function word features from a text file"""
    
    # load resources and text file
#    data_file, vocab_path=args.path, args.function_words_path
    function_words = load_function_words(vocab_path)
    
    reviews = []
    with open(data_file, 'r') as df:
        for line in df:
            fields = line.strip().split("\t")
            reviews.append(fields[-1])
    
    
    # TODO: fill this matrix
    review_features = np.zeros((len(reviews),len(function_words)), dtype=np.int64)
    # row is which review
    # column is which word
    print(f"Numpy array has shape {review_features.shape} and dtype {review_features.dtype}")
    # TODO: Calculate these from review_features
    for i,review in enumerate(reviews): 
        review_tokens = review.lower().split(" ")
        for j,function_word in enumerate(function_words):
            review_features[i,j] = len([w for w in review_tokens if w == function_word])
    
    cnt = review_features.sum(axis = 0)
    most_common_count = cnt.max()
    most_common_word = function_words[cnt.argmax()]
    print(f"Most common word: {most_common_word}, count: {most_common_count}")
    
    # TODO: Find any features that weren't in the data (i.e. columns that sum to 0)
    zero_inds, = np.where(cnt == 0)
    if len(zero_inds)>0:
        print("No instances found for: ")
        for ind in zero_inds:
            print(f"  {function_words[ind]}")
    else:
        print("All function words found")
    
    
    matrix_sum = review_features.sum()
    print(f"Sum of raw count matrix: {matrix_sum}")
    
    # TODO: make a binary feature vector from your count vector
    word_binary = (review_features > 0).astype(int)
    word_binary_sum = word_binary.sum()
    print(f"Sum of binary matrix: {word_binary_sum}")
    
    # TODO: normalize features by review length (divide rows by length of review)
    review_len = []
    for review in reviews:
        review_len.append(len(review))
    norm_reviews = np.copy(review_features)/np.asarray(review_len)[:,np.newaxis]
    norm_reviews_sum = norm_reviews.sum()
    print(f"Sum of normed matrix: {norm_reviews_sum}")
    
    # TODO: remove features from <review_features> that occur less than min_count times
    min_count = 100
    min_matrix = np.copy(review_features)[:,~(cnt <= min_count)]
    min_matrix_shape = min_matrix.shape
    print(f"Shape after removing features that occur < {min_count} times: {min_matrix_shape}")
    
    
    # TODO: load author data into a label array, assigning a class index per unique author (see lab)
    #  Author ID's are index 1 in the file
    authors = []
    with open(data_file, 'r') as df:
        for line in df:
            fields = line.strip().split("\t")
            authors.append(fields[1])
            
    author_classes = {author_str: i for i,author_str in enumerate(set(authors))}
    labels = np.asarray([author_classes[author_str] for author_str in authors])
    
    #TODO: split the dataset by updating the function above
    train, val = split_dataset(review_features, labels, 0.9)
    
    # Code below that all your data has been retained in your splits; do not edit.
    # Must all print True
    
    # check X
    train_X = train[0]
    val_X = val[0]
    same_x = (train_X.sum()+val_X.sum()) == review_features.sum()
    print(f"Same X sum {same_x}")
    # check y
    train_y = train[1]
    val_y = val[1]
    same_y = (train_y.sum()+val_y.sum()) == labels.sum()
    print(f"Same y sum {same_y}")
    # check that all labels are assigned
    all_indexes = list(train[2]) + list(val[2])
    indexes_there = sorted(all_indexes) == list(np.arange(review_features.shape[0]))
    print(f"all indexes retained: {indexes_there}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='feature vector homework')
    parser.add_argument('--path', type=str, default="imdb_grade.txt",
                        help='path to the menu to update')
    parser.add_argument('--function_words_path', type=str, default="ewl_function_words.txt",
                        help='path to the list of words to use as features')
    args = parser.parse_args()
    
    main(args.path, args.function_words_path)
