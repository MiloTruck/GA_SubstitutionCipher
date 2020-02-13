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
    ngrams = generate_ngrams(text, 3)
    
    fitness = 0
    for ngram in ngrams:
        if ngram in ngram_frequency:
            frequency = int(ngram_frequency[ngram])
            fitness += math.log2(frequency)

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

def rejection_sampling(fitness):
    index = -1
    highest_probability = max(fitness)
        
    selected = False
    while not selected:
        index = randint(0, population_size-1)
        probability = fitness[index]

        r = uniform(0, highest_probability)
        selected = (r < probability)
    
    return index

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

def reproduction_RWS(population, fitness):
    crossover_population = []

    while len(crossover_population) < crossover_count:
        parent_one_index = rejection_sampling(fitness)
        parent_two_index = rejection_sampling(fitness)

        parent_one = population[parent_one_index]
        parent_two = population[parent_two_index]

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
seeding = True

# Default variables
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
elitism_count = int(elitism_percentage * population_size)
crossover_count = population_size - elitism_count

# Defining the substitution cipher
ciphertext = 'Hrovmxv rm gsv xlfig! Xsziovh Wzimzb szw bvhgviwzb kovzwvw Mlg Tfrogb gl zm rmwrxgnvmg wvmlfmxrmt srn (drgs rmurmrgv qrmtov zmw qzmtov) uli gszg sv dzh z uzohv gizrgli gl lfi hvivmv, roofhgirlfh, vcxvoovmg, zmw hl uligs, kirmxv, lfi Oliw gsv Prmt, yb ivzhlm lu srh szermt, lm wrevih lxxzhrlmh, zmw yb wrevih nvzmh zmw dzbh, zhhrhgvw Ovdrh, gsv Uivmxs Prmt, rm srh dzih ztzrmhg lfi hzrw hvivmv, roofhgirlfh, vcxvoovmg, zmw hl uligs; gszg dzh gl hzb, yb xlnrmt zmw tlrmt, yvgdvvm gsv wlnrmrlmh lu lfi hzrw hvivmv, roofhgirlfh, vcxvoovmg, zmw hl uligs, zmw gslhv lu gsv hzrw Uivmxs Ovdrh, zmw drxpvwob, uzohvob, gizrglilfhob, zmw lgsvidrhv vero-zweviyrlfhob, ivevzormt gl gsv hzrw Uivmxs Ovdrh dszg ulixvh lfi hzrw hvivmv, roofhgirlfh, vcxvoovmg, zmw hl uligs, szw rm kivkzizgrlm gl hvmw gl Xzmzwz zmw Mligs Znvirxz. Gsrh nfxs, Qviib, drgs srh svzw yvxlnrmt nliv zmw nliv hkrpb zh gsv ozd gvinh yirhgovw rg, nzwv lfg drgs sftv hzgrhuzxgrlm, zmw hl ziirevw xrixfrglfhob zg gsv fmwvihgzmwrmt gszg gsv zulivhzrw, zmw levi zmw levi ztzrm zulivhzrw, Xsziovh Wzimzb, hgllw gsviv yvuliv srn fklm srh girzo; gszg gsv qfib dviv hdvzirmt rm; zmw gszg Ni. Zgglimvb-Tvmvizo dzh nzprmt ivzwb gl hkvzp.'
plaintext = ''
key = ''

ciphertext = ciphertext.upper()

# Getting pre-computed ngram frequency
filename = 'ngramFrequency.csv'
ngram_frequency = get_ngram_frequency(filename)

# Main Program
if __name__== "__main__":
    population = initialization()
    
    for _ in range(generations):
        fitness = evaluation(population)
        elitist_population = elitism(population, fitness)
        crossover_population = reproduction_RWS(population, fitness)

        population = elitist_population + crossover_population
        #population = mutation()

        highest_fitness = max(fitness)
        average_fitness = sum(fitness) / population_size

        index = fitness.index(highest_fitness)
        key = population[index]
        decrypted_text = decrypt(key)

        print('Average Fitness:', average_fitness)
        print('Max Fitness:', highest_fitness)
        print('Decrypted Text:', decrypted_text)
        print('-'*50)


# TODO
# Population Size is 501 for some reason
# Tournament Selection