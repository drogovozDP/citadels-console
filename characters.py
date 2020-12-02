class character(): # шаблон от которого будем наследоваться
    def __init__(self):
        self.choosen = True

    def ability(self):
        print(self.initiative)


class Assassin(character):
    def __init__(self):
        character.__init__(self)
        self.choosen = False
        self.initiative = 1 # порядок вызова персонажа
        self.name = 'Assassin'

class Thief(character):
    def __init__(self):
        character.__init__(self)
        self.choosen = False
        self.initiative = 2
        self.name = 'Thief'

class Wizard(character):
    def __init__(self):
        character.__init__(self)
        self.choosen = False
        self.initiative = 3
        self.name = 'Wizard'

class King(character):
    def __init__(self):
        character.__init__(self)
        self.choosen = False
        self.initiative = 4
        self.name = 'King'


class Bishop(character):
    def __init__(self):
        character.__init__(self)
        self.choosen = False
        self.initiative = 5
        self.name = 'Bishop'

class Merchant(character):
    def __init__(self):
        character.__init__(self)
        self.choosen = False
        self.initiative = 6
        self.name = 'Merchant'

class Architect(character):
    def __init__(self):
        character.__init__(self)
        self.choosen = False
        self.initiative = 7
        self.name = 'Architect'

class Warlord(character):
    def __init__(self):
        character.__init__(self)
        self.choosen = False
        self.initiative = 8
        self.name = 'Warlord'
