This homework practices:
* numpy arrays
* operations on arrays - entire array and only certain axes
* count vectors as features, binary vectors, normalized count vectors
* slicing arrays
* loading labels (see lab part 2)
* splitting off a percent of random held-out data. Some good solutions for numpy shuffling:
https://stackoverflow.com/questions/4601373/better-way-to-shuffle-two-numpy-arrays-in-unison
#############################################################################################################

The `feature_extraction.py` reads a text file 'imdb_practice.txt' by default, which contains 500 IMDB reviews and associated author ID. Then, 176 target keywords will be searched, counted by review and stored in a numpy matrix. 
Few further steps will be implemented including: printing the most common words and associated counts, the keywords not found in reviews, total keywords counts, etc. 
Besides, the input dataset will be shuffled and splitted into training and validation sets, where the training/validation ratio is given (90% by default). 
