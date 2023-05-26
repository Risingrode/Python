with open('test.txt') as f:
    test_words = f.read().splitlines()

with open('res.txt') as f:
    res_words = f.read().splitlines()

word_indices = []
for word in test_words:
    if word in res_words:
        word_indices.append(res_words.index(word))

with open('output.txt', 'w') as f:
    f.write('\n'.join(map(str, word_indices)))
