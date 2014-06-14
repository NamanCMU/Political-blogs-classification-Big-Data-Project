import sys
from collections import defaultdict, Counter
import math

## Reading the arguements 
train_file = sys.argv[1] # split.train
test_file = sys.argv[2] # split.test

### Reading the train file to get all the filenames
with open(train_file) as f1:
	filenames = []
	conservative_files_train = []
	liberal_files_train = []
	for line in f1:
		line = line.replace("\n","")
		filenames.append(line)
		if "con" in line:
			conservative_files_train.append(line) # Conservative filenames
		else:
			liberal_files_train.append(line) # Liberal filenames
###	

### Calculating Class Prior Probabilities
Prob_conservative = math.log(len(conservative_files_train)) - (math.log(len(liberal_files_train) + len(conservative_files_train)))
Prob_liberal = math.log(len(liberal_files_train)) - (math.log(len(liberal_files_train) + len(conservative_files_train)))
###


### Generating the vocabulary
vocabulary = []
conservative_vocabulary = []
liberal_vocabulary = []
for train_file_name in filenames:
	ftrain = open(train_file_name)
	for line in ftrain:
		line = line.replace("\n","")
		line = line.lower() # Ignoring Case
		if "con" in train_file_name:
			conservative_vocabulary.append(line) # Conservative Vocabulary
		else:
			liberal_vocabulary.append(line) # Liberal Vocabulary
		vocabulary.append(line)
###

distinct_vocabulary = set(vocabulary) # Distinct Vocabulary
Total_distinct_words = len(distinct_vocabulary) # Total distinct words in the vocabulary

### Creating default Dictionaries for 1. words and their total occurences
## 2. words and their Probabilities

## Liberal Class
Prob_words_dict_liberal = defaultdict(int)
nliberal = len(liberal_vocabulary)

## Conservative Class
Prob_words_dict_conservative = defaultdict(int)
nconservative = len(conservative_vocabulary)
###

### Filling the data in both the above dictionaries ---------------- Table 6.2 Tom Mitchell Book

## Liberal Class

# Count
Distinct_words_dict_liberal = Counter(liberal_vocabulary)

# Probability
for word in distinct_vocabulary:
	Prob_words_dict_liberal[word] = ((math.log(Distinct_words_dict_liberal[word] + 1)) - \
							math.log(nliberal + Total_distinct_words))

## Conservative Class

# Count
Distinct_words_dict_conservative = Counter(conservative_vocabulary)

# Probability
for word in distinct_vocabulary:
	Prob_words_dict_conservative[word] = ((math.log(Distinct_words_dict_conservative[word] + 1)) - \
							math.log(nconservative + Total_distinct_words))
###	


## Testing Documents

# Opening the file with all the testing file names
with open(test_file) as f2:
	filenames_test = []
	for line in f2:
		line = line.replace("\n","")
		filenames_test.append(line)

accuracy = 0.0
# Reading words from each file
for test_file_name in filenames_test:
	Pconservative = 0 
	Pliberal = 0
	ftest = open(test_file_name)
	for line in ftest:
		line = line.replace("\n","")
		line = line.lower()
		Pconservative = Pconservative + (Prob_words_dict_conservative[line]) # Conservative Probability
		Pliberal = Pliberal + (Prob_words_dict_liberal[line]) # Liberal Probability
  	
  	# Adding Prior Probabilities
	Pliberal = Pliberal + Prob_liberal
	Pconservative = Pconservative + Prob_conservative
	
	if Pliberal < Pconservative:
		print "C" # Predicting Conservative
	if Pliberal > Pconservative:
		print "L" # Predicting Liberal
	
	## Finding number of correct predictions
	if "con" in test_file_name and Pliberal < Pconservative:
		accuracy += 1
	elif "lib" in test_file_name and Pliberal > Pconservative:
		accuracy += 1
	else:
		continue

accuracy = accuracy/len(filenames_test)
print "Accuracy:", round(accuracy,4)
