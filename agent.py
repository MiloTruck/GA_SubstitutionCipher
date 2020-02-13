import csv
import math
from random import randint

def generate_ngrams(word, n):            
    ngrams = [word[i:i+n] for i in range(len(word)-n+1)]

    processed_ngrams = []
    for ngram in ngrams:
        if ngram.isalpha():
            ngram_upper = ngram.upper()
            processed_ngrams.append(ngram_upper)

    return processed_ngrams

class Agent():
    def define_cipher(self, plaintext, ciphertext, key):
        self.plaintext = plaintext.upper()
        self.ciphertext = ciphertext.upper()
        self.key = key.upper()

    def get_ngram_frequency(self, filename):
        ngram_frequency = {}
        
        file = open(filename, 'r')
        reader = csv.reader(file)

        for key, value in reader:
            ngram_frequency[key] = value

        self.ngram_frequency = ngram_frequency
        return ngram_frequency

    def decrypt(self, key):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letter_mapping = {}

        for i in range(26):
            k = letters[i]
            v = key.upper()[i]

            letter_mapping[k] = v

        decrypted_text = ''
        for character in self.ciphertext:
            if character not in letters:
                decrypted_text += character
            else:
                decrypted_text += letter_mapping[character]

        return decrypted_text

    def calculate_fitness(self, text):
        ngrams = generate_ngrams(text, 3)
        
        fitness = 0
        for ngram in ngrams:
            frequency = int(self.ngram_frequency[ngram])
            fitness += math.log2(frequency)

        return fitness

    def mutate_key(self, key):
        a = randint(0, len(key))
        b = randint(0, len(key))

        temp = key[a]
        key[a] = key[b]
        key[b] = temp

        return key

    def merge_keys(self, one, two, crossover_points_count):
        offspring = [None]*26
        count = 0
        while count < k:
            r = randint(0, len(one)-1)

            if offspring[r] == None:
                offspring[r] = one[r]
                count += 1
        
        for ch in two:
            if ch not in offspring:
                for i in range(len(offspring)):
                    if offspring[i] == None:
                        offspring[i] = ch
                        break

        return offspring

    


    
