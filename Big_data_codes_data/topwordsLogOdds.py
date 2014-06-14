import sys
from collections import defaultdict, Counter
import math

## Reading the arguements 
train_file = sys.argv[1] # split.train

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
	Prob_words_dict_liberal[word] = math.exp((math.log(Distinct_words_dict_liberal[word] + 1)) - \
							math.log(nliberal + Total_distinct_words))

## Conservative Class

# Count
Distinct_words_dict_conservative = Counter(conservative_vocabulary)

# Probability
for word in distinct_vocabulary:
	Prob_words_dict_conservative[word] = math.exp((math.log(Distinct_words_dict_conservative[word] + 1)) - \
							math.log(nconservative + Total_distinct_words))
###	

# Finding log-odds ratio
lib_cons = {} # lib/cons
cons_lib = {} # cons/lib

for word in distinct_vocabulary:
	lib_cons[word]  = math.log(Prob_words_dict_liberal[word]/Prob_words_dict_conservative[word])
	cons_lib[word] = math.log(Prob_words_dict_conservative[word]/Prob_words_dict_liberal[word])

count = 0
# similar to topwords.py but instead of probabilities, we have log odd ratio
# Printing top 20 words for both the classes

# lib_cons
for w in sorted(lib_cons, key = lib_cons.get,reverse=True):
	print w , round(lib_cons[w],4) # Printing
	count += 1
	if count == 20:
		break

print ""

count = 0

# cons_lib
for w in sorted(cons_lib, key = cons_lib.get,reverse=True):
	print w ,round(cons_lib[w],4) # Printing
	count += 1
	if count == 20:
		break