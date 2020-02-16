# Genetic Algorithm and Substitution Ciphers
*Note that this project is still under progress.*

This project uses Genetic Algorithms to decrypt substitution ciphers by frequency analysis.

In the English language, some sequences of letters appear more often than others, such as "AND". By analysing the frequency of bi-grams (2 letters) and tri-grams (3 letters) in English text, we are able to observe a pattern in the English language. 

Thus, frequency analysis can be used to break substitution ciphers although individual letters are substituted with others. The plaintext, after decryption with a generated key, which matches the frequency of ngrams in English, has the highest probability of being the correct key.

## Usage

To run the program, run the `main.py` python script in a terminal using the command:
```
python3 main.py
```

Note that the substitution cipher has to be defined in `main.py` first:
```python
# Defining the substitution cipher
ciphertext = ''
plaintext = ''
key = ''
```

Other parameters affecting the program can also be changed in `main.py`:
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

This project was heavily inspired by the paper **Decrypting Substitution Ciphers with Genetic Algorithms** by **Jason Brownbridge**. All credits go to him for the original idea. A copy of the paper can be obtained here:
https://people.cs.uct.ac.za/~jkenwood/JasonBrownbridge.pdf

## Future Work
* Implementing a wrapper for `main.py` for smoother usage.
* Including word ngrams for frequency analysis.
* File organization.

