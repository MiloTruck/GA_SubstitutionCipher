import config
import csv
import math
from random import randint, uniform

class GeneticSolver:
    def __init__(self):
        # Genetic Algorithm Parameters
        self.generations = 500
        self.population_size = 500
        self.tournament_size = 20
        self.tournament_winner_probability = 0.75
        self.crossover_probability = 0.65
        self.crossover_points_count = 5
        self.mutation_probability = 0.2
        self.elitism_percentage = 0.15
        self.selection_method = 'TS'
        self.terminate = 100

        # Other parameters
        self.bigram_weight = 0.0
        self.trigram_weight = 1.0
        
        # Usage parameters
        self.verbose = False

        # Default variables
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.elitism_count = int(self.elitism_percentage * self.population_size)
        self.crossover_count = self.population_size - self.elitism_count

        self.tournament_probabilities = [self.tournament_winner_probability]

        for i in range(1, self.tournament_size):
            probability = self.tournament_probabilities[i-1] * (1.0 - self.tournament_winner_probability)
            self.tournament_probabilities.append(probability)

    def get_ngram_frequency(self, filename):
        ngram_frequency = {}
        
        file = open(filename, 'r')
        reader = csv.reader(file)

        headerRead = False
        for key, value in reader:
            if headerRead == False:
                headerRead = True
                continue
                
            ngram_frequency[key] = value

        return ngram_frequency

    def generate_ngrams(self, word, n):
        ngrams = [word[i:i+n] for i in range(len(word)-n+1)]

        processed_ngrams = []
        for ngram in ngrams:
            if ngram.isalpha():
                ngram_upper = ngram.upper()
                processed_ngrams.append(ngram_upper)

        return processed_ngrams

    def decrypt(self, key):
        letter_mapping = {}

        for i in range(26):
            k = self.letters[i]
            v = key.upper()[i]

            letter_mapping[k] = v

        decrypted_text = ''
        for character in self.ciphertext:
            if character not in self.letters:
                decrypted_text += character
            else:
                decrypted_text += letter_mapping[character]

        return decrypted_text

    def calculate_key_fitness(self, text):
        bigrams = self.generate_ngrams(text, 2) 
        trigrams = self.generate_ngrams(text, 3)
        
        bigram_fitness = 0
        if self.bigram_weight > 0:
            for bigram in bigrams:
                if bigram in self.bigram_frequency:
                    frequency = int(self.bigram_frequency[bigram])
                    bigram_fitness += math.log2(frequency)
        
        trigram_fitness = 0
        if self.trigram_weight > 0:    
            for trigram in trigrams:
                if trigram in self.trigram_frequency:
                    frequency = int(self.trigram_frequency[trigram])
                    trigram_fitness += math.log2(frequency)
            
        fitness = (bigram_fitness * self.bigram_weight) + (trigram_fitness * self.trigram_weight)
        return fitness

    def merge_keys(self, one, two):
        offspring = [None]*26
        count = 0
        while count < self.crossover_points_count:
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

        return ''.join(offspring)

    def mutate_key(self, key):
        a = randint(0, len(key)-1)
        b = randint(0, len(key)-1)

        key = list(key)
        temp = key[a]
        key[a] = key[b]
        key[b] = temp

        return ''.join(key)

    def initialization(self):
        population = []
        
        for _ in range(self.population_size):
            key = ''

            while len(key) < 26:
                r = randint(0, len(self.letters)-1)
                
                if self.letters[r] not in key:
                    key += self.letters[r]

            population.append(key)
        
        return population

    def evaluation(self, population):
        fitness = []

        for key in population:
            decrypted_text = self.decrypt(key)
            key_fitness = self.calculate_key_fitness(decrypted_text)
            fitness.append(key_fitness)

        return fitness

    def elitism(self, population, fitness):
        population_fitness = {}
        
        for i in range(self.population_size):
            key = population[i]
            value = fitness[i]

            population_fitness[key] = value

        population_fitness = {k: v for k, v in sorted(population_fitness.items(), key=lambda item: item[1])}
        sorted_population = list(population_fitness.keys())

        elitist_population = sorted_population[-self.elitism_count:]

        return elitist_population

    def roulette_wheel_selection(self, fitness):
        index = -1
        highest_probability = max(fitness)
            
        selected = False
        while not selected:
            index = randint(0, self.population_size-1)
            probability = fitness[index]

            r = uniform(0, highest_probability)
            selected = (r < probability)
        
        return index

    def tournament_selection(self, population, fitness):
        population_copy = population.copy()
        selected_keys = []

        for a in range(2):
            tournament_population = {}
            
            for _ in range(self.tournament_size):
                r = randint(0, len(population_copy)-1)
                key = population_copy[r]
                key_fitness = fitness[r]

                tournament_population[key] = key_fitness
                population_copy.pop(r)

            sorted_tournament_population = {k: v for k, v in sorted(tournament_population.items(), key=lambda item: item[1], reverse=True)}
            tournament_keys = list(sorted_tournament_population.keys())
            
            index = -1
            selected = False
            while not selected:
                index = randint(0, self.tournament_size-1)
                probability = self.tournament_probabilities[index]

                r = uniform(0, self.tournament_winner_probability)
                selected = (r < probability)
        
            selected_keys.append(tournament_keys[index])

        return selected_keys[0], selected_keys[1]

    def reproduction(self, population, fitness):
        crossover_population = []

        while len(crossover_population) < self.crossover_count:
            parent_one, parent_two = None, None

            if self.selection_method == 'RWS':
                parent_one_index = self.roulette_wheel_selection(fitness)
                parent_two_index = self.roulette_wheel_selection(fitness)

                parent_one = population[parent_one_index]
                parent_two = population[parent_two_index]
            else:
                parent_one, parent_two = self.tournament_selection(population, fitness)

            offspring_one = self.merge_keys(parent_one, parent_two)
            offspring_two = self.merge_keys(parent_two, parent_one)

            crossover_population += [offspring_one, offspring_two]
        
        crossover_population = self.mutation(crossover_population, self.crossover_count)

        return crossover_population
        
    def mutation(self, population, population_size):
        for i in range(population_size):
            r = uniform(0, 1)

            if r < self.mutation_probability:
                key = population[i]
                mutated_key = self.mutate_key(key)

                population[i] = mutated_key

        return population

    def convert_to_plaintext(self, decrypted_text):
        plaintext = list(decrypted_text)
        for i in range(len(plaintext)):
            if self.lettercase[i]:
                plaintext[i] = plaintext[i].lower()
        plaintext = ''.join(plaintext)
        
        return plaintext

    def solve(self, ciphertext = ''):
        # Defining ciphertext
        self.ciphertext = ciphertext
        
        # Checking if ciphertext is valid
        if self.ciphertext == '':
            message = (
                '\n(GeneticSolver) Ciphertext invalid. Use solve() as such:\n'
                '\tsolver = GeneticSolver()\n'
                '\tsolver.solve("Example ciphertext")'
            )
            print(message)
            return

        # Formatting ciphertext
        self.lettercase = [ch.islower() and ch.isalpha() for ch in self.ciphertext]
        self.ciphertext = self.ciphertext.upper()

        # Getting pre-computed ngram frequency
        bigram_filename = 'data/bi-ngramFrequency.csv'
        self.bigram_frequency = self.get_ngram_frequency(bigram_filename)

        trigram_filename = 'data/tri-ngramFrequency.csv'
        self.trigram_frequency = self.get_ngram_frequency(trigram_filename)
        
        # Main Program
        population = self.initialization()
        
        highest_fitness = 0
        stuck_counter = 0
        for no in range(self.generations + 1):
            fitness = self.evaluation(population)
            elitist_population = self.elitism(population, fitness)
            crossover_population = self.reproduction(population, fitness)

            population = elitist_population + crossover_population

            # Terminate if highest_fitness not increasing
            if highest_fitness == max(fitness):
                stuck_counter += 1 
            else:
                stuck_counter = 0
            
            if stuck_counter >= self.terminate:
                break
            
            highest_fitness = max(fitness)
            average_fitness = sum(fitness) / self.population_size

            index = fitness.index(highest_fitness)
            key = population[index]
            decrypted_text = self.decrypt(key)

            if self.verbose:
                plaintext = self.convert_to_plaintext(decrypted_text)

                print('[Generation ' + str(no) + ']',)
                print('Average Fitness:', average_fitness)
                print('Max Fitness:', highest_fitness)
                print('Key:', key)
                print('Decrypted Text:\n' + plaintext + '\n')

        plaintext = self.convert_to_plaintext(decrypted_text)
        return plaintext
        

