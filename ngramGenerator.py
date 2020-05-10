from nltk import FreqDist
import csv
import collections

# Function to generate n-grams from a word
def generate_ngrams(word, n):            
    ngrams = [word[i:i+n] for i in range(len(word)-n+1)]
    return ngrams

# Define csv name and n-gram length
filename = input("Name of CSV file to output result: ")
n = input("Length of n-grams: ")

# Setting up training text
file = open('data/TheGreatGatsby.txt', 'r')
text = file.read()
words = text.split()

# Generating n-grams from training text
ngrams = []
for word in words:
    ngrams += generate_ngrams(word, n)

# Processing n-grams to 1. Remove non-alphabetic words 2. Convert n-grams to uppercase
processed_ngrams = []
for ngram in ngrams:
    if ngram.isalpha():
        ngram_upper = ngram.upper()
        processed_ngrams.append(ngram_upper)

# Counting the frequency of n-gram
frequency = FreqDist(processed_ngrams)

# Sorting n-grams descending based on frequency
sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
frequency = collections.OrderedDict(sorted_frequency)

# Writing n-grams and its frequency into a csv
headers = ['n-gram', 'Frequency']
with open('data/' + filename, 'w', newline="") as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow(headers)
    for key, value in frequency.items():
       writer.writerow([key, value])

