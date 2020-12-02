from characters import character

class Player():
    def __init__(self, name, gameMaster, hand):
        self.name = name
        self.character = character()
        self.city = []
        self.hand = hand # кварталы в руке
        self.gold = 2
        self.gameMaster = gameMaster # это эксемпляр игры(у всех он одинаковый), они будут так влиять друг на друга

    def choose_character(self, characters):
        row = ''
        for char in characters: # набор доступных персонажей
            if char.choosen == False:
                row += char.name + '(' + str(char.initiative) + ') '
        print(row)
        while self.character.choosen: # выбор персонажа
            index = int(input('which character? ')) - 1
            self.character = characters[index]
        self.character.choosen = True # теперь этот персонаж выбран
        return index

    def take_resources(self, kind):
        if kind == 'quarter':
            print('take 2 cards')
        else:
            print('take 2 coins')
            self.gold += 2

    def build_stucture(self):
        row = ''
        for i in range(len(self.quarters)):
            row += self.quarters[i] + '(' + str(i + 1) + '), '
        index = int(input('which quarter? ' + row)) - 1
        value = int(self.quarters[index][-1])
        if value > self.gold:
            return
        self.gold -= value
        self.city.append(self.quarters[index])
        del self.quarters[index]

        print(*self.quarters)
        print(*self.city)


    def action(self):
        choose_1 = input('1) gold or quarter? ')
        self.take_resources(choose_1)

        choose_2 = input('2) wanna make special ability? ')
        if choose_2 == 'yes':
            self.character.ability()

        choose_3 = input('3) wanna build something? ')
        if choose_3 == 'yes':
            self.build_stucture()

    def info(self):
        quarters = ''
        for card in self.hand:
            quarters += card.name + ', '
        print(self.name +
              ': gold = ' + str(self.gold) +
              ', quarters = ' + quarters)