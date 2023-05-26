list = []

with open('30000BTC.txt', 'r') as f:
    lists = f.readlines()
    for i in lists:
        list.append(i[9:43])

with open('BTC.txt', 'w') as f:
    for i in list:
        f.write(i+'\n')
