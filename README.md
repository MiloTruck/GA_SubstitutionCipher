# Genetic Algorithm and Substitution Ciphers

This project uses Genetic Algorithms to decrypt substitution ciphers by frequency analysis.

In the English language, some sequences of letters appear more often than others, such as "AND". By analysing the frequency of bi-grams (2 letters) and tri-grams (3 letters) in English text, we are able to observe a pattern in letter frequencies in the English language. In this project, I obtained the letter frequencies using **The Great Gatsby** as training text.

The algorithm repeatedly generates random keys and decrypts the ciphertext using these keys. The key is assigned a fitness value based on how much the letter frequencies of the decrypted text matches the letter frequencies from the training text. Over numerous generations, the keys' fitness improves, which increases the chance of the key decrypting the ciphertext correctly.

Thus, frequency analysis can be used to break substitution ciphers although individual letters are substituted with others. The plaintext, after decryption with a generated key, which matches the frequency of ngrams in English, has the highest probability of being the correct key.

## Demo
The plaintext used is from the opening line of **The Great Gatsby**:
```
'In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since. Whenever you feel like criticizing anyone, he told me, just remember that all the people in this world haven't had the advantages that you've had.
```

The ciphertext is obtained by encrypting the plaintext using substitution cipher with the key `ZYXWVUTSRQPONMLKJIHGFEDCBA`:
```
'Rm nb blfmtvi zmw nliv efomvizyov bvzih nb uzgsvi tzev nv hlnv zwerxv gszg R'ev yvvm gfimrmt levi rm nb nrmw vevi hrmxv. Dsvmvevi blf uvvo orpv xirgrxrarmt zmblmv, sv glow nv, qfhg ivnvnyvi gszg zoo gsv kvlkov rm gsrh dliow szevm'g szw gsv zwezmgztvh gszg blf'ev szw.
```

After running the decryption program `main.py`, we obtain the original plaintext without knowing the decryption key:
```
--------------------------------------------------
Average Fitness: 423.55366352956
Max Fitness: 774.6525013478013
Key: ZYXWVUTSRQPONMLKJIHGFEDCBA
Decrypted Text: 'IN MY YOUNGER AND MORE VULNERABLE YEARS MY FATHER GAVE ME SOME ADVICE THAT I'VE BEEN TURNING OVER IN MY MIND EVER SINCE. WHENEVER YOU FEEL LIKE CRITICIZING ANYONE, HE TOLD ME, JUST REMEMBER THAT ALL THE PEOPLE IN THIS WORLD HAVEN'T HAD THE ADVANTAGES THAT YOU'VE HAD.
--------------------------------------------------
```

## Usage

### Obtaining n-gram frequency
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
* *n-gram length* refers to the length of n-grams to extract. I recommend using a length of 2 as it gave the provided results.

### Substitution Cipher Decryption 
To run the decryption program, run the `main.py` python script in a terminal using the command:
```
python3 main.py
```

The script will ask for the ciphertext to decrypt, which can just be pasted:
```
Ciphertext: 
```

The program will then output the average and highest fitness, decryption key and plaintext obtained using that key every generation. For example:
```
--------------------------------------------------
Average Fitness: 423.55366352956
Max Fitness: 774.6525013478013
Key: ZYXWVUTSRQPONMLKJIHGFEDCBA
Decrypted Text: 'IN MY YOUNGER AND MORE VULNERABLE YEARS MY FATHER GAVE ME SOME ADVICE THAT I'VE BEEN TURNING OVER IN MY MIND EVER SINCE. WHENEVER YOU FEEL LIKE CRITICIZING ANYONE, HE TOLD ME, JUST REMEMBER THAT ALL THE PEOPLE IN THIS WORLD HAVEN'T HAD THE ADVANTAGES THAT YOU'VE HAD.
--------------------------------------------------
```


If you wish to tweak the genetic algorithm, the algorithm's parameters can be changed in `config.py`:
```python
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
```

## References

To obtain the frequency of ngrams, the novel "The Great Gatsby" was used. The training text `TheGreatGatsby.txt` was obtained from Project Gutenberg:  
http://gutenberg.net.au/ebooks02/0200041.txt 

This project was heavily inspired by the paper **Decrypting Substitution Ciphers with Genetic Algorithms** by **Jason Brownbridge**. The method used for this project is well explained in this paper. All credits go to him for the original idea. A copy of the paper can be obtained here:  
https://people.cs.uct.ac.za/~jkenwood/JasonBrownbridge.pdf
