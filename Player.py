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
        if kind == '2':
            newCards = self.gameMaster.giveCard(2) # вместо константу нужна переменная, но что и как будет ее менять?
            row = ''
            for i in range(len(newCards)):
                row += newCards[i].name + '(' + str(i + 1) + ') '
            index = int(input('which one do you want to take? ' + row)) - 1
            card = newCards[index]
            del newCards[index]
            self.hand.append(card)
            self.gameMaster.takeCard(newCards)
            print('done')
        else:
            print('take 2 coins')
            self.gold += 2

    def build_stucture(self):
        row = ''
        for i in range(len(self.hand)):
            row += self.hand[i].name + '(value: ' + str(self.hand[i].value) + ')(' + str(i + 1) + ') '
        index = int(input(row)) - 1
        if self.gold - self.hand[index].value < 0:
            return # если не хватает золота, то сразу выходим
        self.city.append(self.hand[index])
        self.gold -= self.hand[index].value
        del self.hand[index]

    def action(self):
        choose_1 = input('1) gold(1) or quarter(2)? ')
        self.take_resources(choose_1)

        # choose_2 = input('2) wanna make special ability? ')
        # if choose_2 == 'yes':
        #     self.character.ability()

        choose_3 = input('3) wanna build something?(you have ' + str(self.gold) + ' gold) ')
        if choose_3 == 'yes':
            self.build_stucture()

    def info(self):
        quarters = ''
        built = ''
        for card in self.hand:
            quarters += card.name + ', '
        for card in self.city:
            built += card.name + ', '
        print(self.name +
              ': gold = ' + str(self.gold) +
              ', quarters = ' + quarters +
              ', city = ' + built)