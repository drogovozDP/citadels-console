class character(): # шаблон от которого будем наследоваться
    def __init__(self, player, gameMaster):
        self.choosen = True
        self.player = player
        self.gameMaster = gameMaster
        self.alive = True
        self.robed = False

    def ability(self):
        print(self.initiative)


class Assassin(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 1 # порядок вызова персонажа
        self.name = 'Assassin'
    def ability(self):
        index = int(input('who will die in this round?(2)(3)(4)(5)(6)(7)(8)')) - 1
        if index + 1 < 2 or index + 1 > 8: # защита от дураков
            print('you are fool,', self.name)
            return
        self.gameMaster.deckChar[index].alive = False

class Thief(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 2
        self.name = 'Thief'
    def ability(self):
        row = ''
        dead_index = 0
        for i in range(len(self.gameMaster.deckChar) - 2): # убираем жертву ассасина из пула выбора
            if self.gameMaster.deckChar[i + 2].alive:
                row += '(' + str(i + 3) + ')'
            else:
                dead_index = i + 2
        # print('dead index is:', dead_index)
        index = int(input('who are we robbing?' + row)) - 1 # выбор
        if index == dead_index or index + 1 < 3 or index + 1 > 8: # защита от дураков
            print('you are fool,', self.name)
            return
        self.gameMaster.deckChar[index].robed = True # обворуем этого персонажа, если вызовется метод действия у игрока

class Wizard(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 3
        self.name = 'Wizard'

class King(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 4
        self.name = 'King'


class Bishop(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 5
        self.name = 'Bishop'

class Merchant(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 6
        self.name = 'Merchant'

class Architect(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 7
        self.name = 'Architect'

class Warlord(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 8
        self.name = 'Warlord'
