from agent import Agent
import csv
import math
from random import randint, uniform

def get_ngram_frequency(filename):
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

def generate_ngrams(word, n):
    ngrams = [word[i:i+n] for i in range(len(word)-n+1)]

    processed_ngrams = []
    for ngram in ngrams:
        if ngram.isalpha():
            ngram_upper = ngram.upper()
            processed_ngrams.append(ngram_upper)

    return processed_ngrams

def decrypt(key):
    letter_mapping = {}

    for i in range(26):
        k = letters[i]
        v = key.upper()[i]

        letter_mapping[k] = v

    decrypted_text = ''
    for character in ciphertext:
        if character not in letters:
            decrypted_text += character
        else:
            decrypted_text += letter_mapping[character]

    return decrypted_text

def calculate_key_fitness(text):
    bigrams = generate_ngrams(text, 2) 
    trigrams = generate_ngrams(text, 3)
    
    bigram_fitness = 0
    if bigram_weight > 0:
        for bigram in bigrams:
            if bigram in bigram_frequency:
                frequency = int(bigram_frequency[bigram])
                bigram_fitness += math.log2(frequency)
    
    trigram_fitness = 0
    if trigram_weight > 0:    
        for trigram in trigrams:
            if trigram in trigram_frequency:
                frequency = int(trigram_frequency[trigram])
                trigram_fitness += math.log2(frequency)
        
    fitness = (bigram_fitness * bigram_weight) + (trigram_fitness * trigram_weight)
    return fitness

def merge_keys(one, two):
    offspring = [None]*26
    count = 0
    while count < crossover_points_count:
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

def mutate_key(key):
    a = randint(0, len(key)-1)
    b = randint(0, len(key)-1)

    key = list(key)
    temp = key[a]
    key[a] = key[b]
    key[b] = temp

    return ''.join(key)

def initialization():
    population = []
    
    for _ in range(population_size):
        key = ''

        while len(key) < 26:
            r = randint(0, len(letters)-1)
            
            if letters[r] not in key:
                key += letters[r]

        population.append(key)
    
    return population

def evaluation(population):
    fitness = []

    for key in population:
        decrypted_text = decrypt(key)
        key_fitness = calculate_key_fitness(decrypted_text)
        fitness.append(key_fitness)

    return fitness

def elitism(population, fitness):
    population_fitness = {}
    
    for i in range(population_size):
        key = population[i]
        value = fitness[i]

        population_fitness[key] = value

    population_fitness = {k: v for k, v in sorted(population_fitness.items(), key=lambda item: item[1])}
    sorted_population = list(population_fitness.keys())

    elitist_population = sorted_population[-elitism_count:]

    return elitist_population

def roulette_wheel_selection(fitness):
    index = -1
    highest_probability = max(fitness)
        
    selected = False
    while not selected:
        index = randint(0, population_size-1)
        probability = fitness[index]

        r = uniform(0, highest_probability)
        selected = (r < probability)
    
    return index

def tournament_selection(population, fitness):
    population_copy = population.copy()
    selected_keys = []

    for a in range(2):
        tournament_population = {}
        
        for _ in range(tournament_size):
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
            index = randint(0, tournament_size-1)
            probability = tournament_probabilities[index]

            r = uniform(0, tournament_winner_probability)
            selected = (r < probability)
    
        selected_keys.append(tournament_keys[index])

    return selected_keys[0], selected_keys[1]

def reproduction(population, fitness):
    crossover_population = []

    while len(crossover_population) < crossover_count:
        parent_one, parent_two = None, None

        if selection_method == 'RWS':
            parent_one_index = roulette_wheel_selection(fitness)
            parent_two_index = roulette_wheel_selection(fitness)

            parent_one = population[parent_one_index]
            parent_two = population[parent_two_index]
        elif selection_method == 'TS':
            parent_one, parent_two = tournament_selection(population, fitness)

        offspring_one = merge_keys(parent_one, parent_two)
        offspring_two = merge_keys(parent_two, parent_one)

        crossover_population += [offspring_one, offspring_two]
    
    crossover_population = mutation(crossover_population, crossover_count)

    return crossover_population
    
def mutation(population, population_size):
    for i in range(population_size):
        r = uniform(0, 1)

        if r < mutation_probability:
            key = population[i]
            mutated_key = mutate_key(key)

            population[i] = mutated_key

    return population

# Genetic Algorithm Parameters
generations = 500
population_size = 500
tournament_size = 20
tournament_winner_probability = 0.75
crossover_probability = 0.65
crossover_points_count = 5
mutation_probability = 0.2
elitism_percentage = 0.15
selection_method = 'TS'

# Other parameters
bigram_weight = 0.0
trigram_weight = 1.0

# Default variables
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
elitism_count = int(elitism_percentage * population_size)
crossover_count = population_size - elitism_count

tournament_probabilities = [tournament_winner_probability]

for i in range(1, tournament_size):
    probability = tournament_probabilities[i-1] * (1.0 - tournament_winner_probability)
    tournament_probabilities.append(probability)

# Defining the substitution cipher
ciphertext = "Zmw, zugvi ylzhgrmt gsrh dzb lu nb glovizmxv, R xlnv gl gsv zwnrhhrlm gszg rg szh z ornrg. Xlmwfxg nzb yv ulfmwvw lm gsv sziw ilxp li gsv dvg nzihsvh yfg zugvi z xvigzrm klrmg R wlm'g xziv dszg rg'h ulfmwvw lm. Dsvm R xznv yzxp uiln gsv Vzhg ozhg zfgfnm R uvog gszg R dzmgvw gsv dliow gl yv rm fmrulin zmw zg z hlig lu nlizo zggvmgrlm ulivevi; R dzmgvw ml nliv irlglfh vcxfihrlmh drgs kirerovtvw tornkhvh rmgl gsv sfnzm svzig."
plaintext = ''
key = ''

ciphertext = ciphertext.upper()

# Getting pre-computed ngram frequency
bigram_filename = 'bi-ngramFrequency.csv'
bigram_frequency = get_ngram_frequency(bigram_filename)

trigram_filename = 'tri-ngramFrequency.csv'
trigram_frequency = get_ngram_frequency(trigram_filename)

# Main Program
if __name__== "__main__":
    population = initialization()
    
    for _ in range(generations):
        fitness = evaluation(population)
        elitist_population = elitism(population, fitness)
        crossover_population = reproduction(population, fitness)

        population = elitist_population + crossover_population

        highest_fitness = max(fitness)
        average_fitness = sum(fitness) / population_size

        index = fitness.index(highest_fitness)
        key = population[index]
        decrypted_text = decrypt(key)

        print('Average Fitness:', average_fitness)
        print('Max Fitness:', highest_fitness)
        print('Key:', key)
        print('Decrypted Text:', decrypted_text)
        print('-'*50)