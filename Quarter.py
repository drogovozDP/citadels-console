import random

class Quarter():
    def __init__(self, name, value):
        self.name = name
        self.value = value

deck = []
file = open('quarters.txt', 'r')

for line in file:
    name = line[0:len(line) - 5]
    value = int(line[len(line) - 4: len(line) - 3])
    amount = int(line[len(line) - 2: len(line) - 1])
    for i in range(amount):
        deck.append(Quarter(name, value))
    # data.append(line[0:len(line) - 1])

# random.shuffle(deck)

