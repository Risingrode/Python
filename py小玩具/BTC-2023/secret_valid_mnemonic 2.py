import secrets

def generate_seed_phrase(num_words):
    # Load the word list
    with open('wordlist.txt') as f:
        wordlist = f.read().splitlines()

    # Generate a list of random words
    words = []
    for i in range(num_words):
        word = secrets.choice(wordlist)
        words.append(word)

    # Join the words into a phrase
    seed_phrase = ' '.join(words)

    return seed_phrase

# Generate 10000 seed phrases with 12 words each
num_phrases = 10000
num_words = 12
seed_phrases = []

for i in range(num_phrases):
    seed_phrase = generate_seed_phrase(num_words)
    seed_phrases.append(seed_phrase)
    print(seed_phrase)

# Save seed phrases to a text file
with open('seed_phrases.txt', 'w') as f:
    for seed_phrase in seed_phrases:
        f.write(seed_phrase + '\n')
