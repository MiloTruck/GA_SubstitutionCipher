# Decrypting Substitution Ciphers with Genetic Algorithms

This project uses Genetic Algorithms to decrypt substitution ciphers by frequency analysis.

In the English language, some sequences of letters appear more often than others, such as "AND". By analysing the frequency of bi-grams (2 letters) and tri-grams (3 letters) in English text, we are able to observe a pattern in letter frequencies in the English language. In this project, I obtained the letter frequencies using **The Great Gatsby** as training text.

The algorithm repeatedly generates random keys and decrypts the ciphertext using these keys. Each key is assigned a fitness value based on how much the letter frequencies of the decrypted text matches the letter frequencies from the training text. Over numerous generations, the keys' fitness improves, which increases the chance of the key decrypting the ciphertext correctly.

Thus, frequency analysis can be used to break substitution ciphers although individual letters are substituted with others. The plaintext, after decryption with a generated key, which matches the frequency of ngrams in English the most, has the highest probability of being the correct key.

## Demo
![Demo](Demo%20Files/Demo.gif)  
The plaintext used is from the opening line of **The Great Gatsby**:
```
In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since. Whenever you feel like criticizing anyone, he told me, just remember that all the people in this world haven't had the advantages that you've had.
```

The ciphertext is obtained by encrypting the plaintext using substitution cipher with the key `ZY
XWVUTSRQPONMLKJIHGFEDCBA`:
```
Rm nb blfmtvi zmw nliv efomvizyov bvzih nb uzgsvi tzev nv hlnv zwerxv gszg R'ev yvvm gfimrmt levi rm nb nrmw vevi hrmxv. Dsvmvevi blf uvvo orpv xirgrxrarmt zmblmv, sv glow nv, qfhg ivnvnyvi gszg zoo gsv kvlkov rm gsrh dliow szevm'g szw gsv zwezmgztvh gszg blf'ev szw.
```

After running the example decryption program `example.py`, we obtain the original plaintext without knowing the decryption key:
```
[Generation 329]
Average Fitness: 409.2687963265419
Max Fitness: 774.6525013478013
Key: ZYXWVUTSRQPONMLKJIHGFEDCBA
Decrypted Text:
In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since. Whenever you feel like criticizing anyone, he told me, just remember that all the people in this world haven't had the advantages that you've had.
```

## Usage

### Obtaining n-gram frequency
Note that this is not mandatory, the n-gram frequency have been generated.  
`ngramGenerator.py` is used to generate the frequencies of n-grams in the training text. The result is stored in the `data/` directory as a CSV file.

To obtain n-gram frequency, run `ngramGenerator.py` in a terminal using python3:
```
python3 ngramGenerator.py
```

The script will ask for 2 parameters, *filename* and *n-gram length* :
```
Name of CSV file to output result: 
Length of n-grams: 
```
* *filename* refers to the name of the CSV file where the n-gram frequency will be stored.
* *n-gram length* refers to the length of n-grams to extract. I recommend using a length of 2 as it provided the best results.

### Substitution Cipher Decryption 
The decryption program can be used by importing `GASolver.py`, and using the `GeneticSolver` class. An example has been provided in `example.py`:
```python
# Importing the GeneticSolver object from GASolver.py
from GASolver import GeneticSolver

# Initializing GeneticSolver object
solver = GeneticSolver()

# Changing parameters in the GeneticSolver object, if needed.
solver.verbose = True

ciphertext = "Rm nb blfmtvi zmw nliv efomvizyov bvzih nb uzgsvi tzev nv hlnv zwerxv gszg R'ev yvvm gfimrmt levi rm nb nrmw vevi hrmxv. Dsvmvevi blf uvvo orpv xirgrxrarmt zmblmv, sv glow nv, qfhg ivnvnyvi gszg zoo gsv kvlkov rm gsrh dliow szevm'g szw gsv zwezmgztvh gszg blf'ev szw."

# The function solve() requires the ciphertext as an argument, and returns the plaintext.
plaintext = solver.solve(ciphertext)
print(plaintext)
```

The `solve()` function of the **GeneticSolver** class runs the decryption program on the given ciphertext and returns the plaintext with the highest fitness. 

The default parameters of the genetic algorithm is shown below:
```python
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
```

If you wish to tweak the genetic algorithm parameters, they can be accessed through referencing the **GeneticSolver** class:
```python
solver = GeneticSolver()
solver.generations = 2000
solver.verbose = True
```

Below is an explanation of each paramter. I recommend reading the paper **Decrypting Substitution Ciphers with Genetic Algorithms** (referenced below) to understand how the genetic algorithm parameters work.

| Parameter                     | Type                              | Explanation                                                                     |
|-------------------------------|-----------------------------------|---------------------------------------------------------------------------------|
| Generations                   | Int                               | Number of generations before the genetic algorithm terminates                   |
| Population Size               | Int                               | Size of population                                                              |
| Tournament Size               | Int                               | Size of the tournament population in selection                                  |
| Tournament Winner Probability | Float between 0 and 1             | Probability of chromosomes being selected in tournament selection               |
| Crossover Probability         | Float between 0 and 1             | Probability of crossover occuring                                               |
| Crossover Points Count        | Int                               | Number of crossover points between 2 chromosomes                                |
| Mutation Probability          | Float between 0 and 1             | Probability of mutation of a chromosome in the population                      |
| Elitism Percentage            | Float between 0 and 1             | Percentage of population to copy over to the next population                    |
| Selection Method              | 'TS' or 'RWS'                     | Tournament Selection (TS) or Roulette Wheel Selection (RWS), the selection method.|
| Terminate                     | Int                               | Number of iterations where *highest_fitness* does not increase before terminating |
| Bigram Weight                 | Float between 0 and 1 (inclusive) | How dependent fitness is on bigrams                                             |
| Trigram Weight                | Float between 0 and 1 (inclusive) | How dependent fitness is on trigrams                                            |
| Verbose                       | Boolean                           | Output information at every iteration                                           |



## References

To obtain the frequency of ngrams, the novel "The Great Gatsby" was used. The training text `TheGreatGatsby.txt` was obtained from Project Gutenberg:  
http://gutenberg.net.au/ebooks02/0200041.txt 

This project was heavily inspired by the paper **Decrypting Substitution Ciphers with Genetic Algorithms** by **Jason Brownbridge**. The method used for this project is well explained in this paper. All credits go to him for the original idea. A copy of the paper can be obtained here:  
https://people.cs.uct.ac.za/~jkenwood/JasonBrownbridge.pdf
