from characters import character

class Player():
    def __init__(self, name, gameMaster, hand):
        self.name = name
        self.gameMaster = gameMaster  # это эксемпляр игры(у всех он одинаковый), они будут так влиять друг на друга
        self.charList = [] # это нужно для игры вдвоем или втроем. Максимум будет 2 персонажа в этом списке
        self.character = character(None, self.gameMaster)
        self.city = [] # построенные кварталы
        self.hand = hand # кварталы в руке
        self.gold = 51
        self.take = {'gold': 2, 'quarter': 2} # сколько игрок может взять золота или кварталов
        self.all_actions = {'build': True, 'ability': True, # все действия игроков
                            'laboratory_action': False, 'graveyard_action': False,
                            'greatwall_bonus': False, 'laboratory_action': False,
                            'observatory_bonus': False, 'smithy_action': False,
                            'library_bonus': False, 'schoolofmagic_bonus': False,
                            'hauntedcity_bonus': False, 'imperialtreasury_bonus': False,
                            'maproom_bonus': False}
        self.action_pool = []

    def get_hand(self):
        row = ''
        for i in range(len(self.hand)):
            row += self.hand[i].name + '(value: ' + str(self.hand[i].value) + ')(' + str(i + 1)  + '), '
        row = row[0: len(row) - 2]
        return row

    def available_chars(self, characters):
        row = ''
        for char in characters: # набор доступных персонажей
            if not char.choosen:
                row += char.name + '(' + str(char.initiative) + ') '
        return row

    def choose_character(self, characters):
        print(self.available_chars(characters))
        charCount = len(self.charList) + 1
        while len(self.charList) < charCount: # выбор персонажа
            index = int(input('which character? ')) - 1
            if characters[index].choosen == False:
                self.charList.append(characters[index])
        characters[index].choosen = True # теперь этот персонаж выбран
        return index

    def choose_drop(self, characters):
        print(self.available_chars(characters))
        index = int(input('you have to drop someone hide ')) - 1
        characters[index].choosen = True

    def _take_resources(self, kind):
        if kind == '2':
            newCards = self.gameMaster.giveCard(self.take['quarter']) # игрок берет столько карт, сколько ему положено
            row = ''
            for i in range(len(newCards)):
                row += newCards[i].name + '(' + str(i + 1) + ') '
            if not self.all_actions['library_bonus']:
                index = int(input('which one do you want to take? ' + row)) - 1
                card = newCards[index]
                del newCards[index]
                self.hand.append(card)
                self.gameMaster.takeCard(newCards)
            else:
                print('you got: ' + row)
                for card in newCards:
                    self.hand.append(card)
            print('done')
        else:
            print('take 2 coins')
            self.gold += self.take['gold']

    def _build_stucture(self):
        print('you have', self.gold, 'gold')
        if len(self.hand) == 0: return
        row = self.get_hand()
        index = int(input(row + ' ')) - 1
        for quart in self.city:
            if self.hand[index].name == quart.name:
                print("you can't build same quarters")
                return # нельзя строить одинаковые кварталы
        if self.gold - self.hand[index].value < 0:
            print('not enough gold')
            return # если не хватает золота, то сразу выходим
        self.city.append(self.hand[index])
        self.gold -= self.hand[index].value
        self.city[-1].built(self) # если есть возможность, открывает игроку новое действие
        if len(self.city) >= self.gameMaster.max_city_size and self.gameMaster.firstConstruct == None:
            self.gameMaster.firstConstruct = self
        del self.hand[index]

    def action(self, initiative):
        for char in self.charList: # выбираем персонажа из множества наших перс-ей относительно инициативы
            if initiative == char.initiative:
                self.character = char
        if self.character.alive == False:
            print('oh no, you are dead!') # никто об этом не должен знать
            if self.character.name == 'King':
                self.character.default()
            return
        if self.character.robed: # если персонаж ограблен
            for player in self.gameMaster.players: # смотрим у каждого игрока...
                for char in player.charList: # ...нету ли у него вора(':
                    if char.name == 'Thief':
                        player.gold += self.gold
                        self.gold = 0
            print('oh my god, you have lost whole your gold!')
        self.character.default() # применяется свойства персонажа по умолчанию

        # action_pool = []
        for act in self.all_actions: # собираем все действия, которые доступны игроку на данный момент
            if self.all_actions[act]:
                self.action_pool.append(act)
                if act == 'graveyard_action' or act == 'greatwall_bonus' or \
                    act == 'library_bonus' or act == 'schoolofmagic_bonus' or \
                    act == 'hauntedcity_bonus' or act == 'imperialtreasury_bonus' or \
                    act == 'maproom_bonus':
                    self.action_pool.pop()
        self.action_pool.append('done')
        resource = input('gold(1) or quarter(2)?') # обязательное действие, оно отдельно
        self._take_resources(resource)
        thinking = True
        while thinking: # здесь игрок ходоит
            row = ''
            for i in range(len(self.action_pool)):
                row += self.action_pool[i] + '(' + str(i + 1) + '), '
            row = row[0: len(row) - 2]
            choise = int(input(row)) - 1
            if self.action_pool[choise] == 'done': thinking = False # конец хода
            if self.action_pool[choise] == 'build': self._build_stucture() # строит
            if self.action_pool[choise] == 'ability': self.character.ability() # способность карты персонажа
            if self.action_pool[choise] == 'laboratory_action': self.laboratory_action() # можно выбрать, если построена лаборатория
            if self.action_pool[choise] == 'smithy_action': self.smithy_action()
            self.action_pool.pop(choise) # удаляем использованное действие
            if len(self.action_pool) == 1: thinking = False # если игрок сделал все действия
        self.action_pool.clear()

    def laboratory_action(self):
        print('you can burn 1 your quarter from hand and get 2 gold')
        row = self.get_hand()
        choise = int(input(row + ' ')) - 1
        burned = self.hand.pop(choise)
        self.gameMaster.deckQuar.append(burned)
        self.gold += 2

    def smithy_action(self):
        print('you have', self.gold, 'gold')
        yes = input('you can buy 3 quarters for 2 gold (y/n) ' )
        if self.gold < 2: return
        if yes == 'no': return
        if yes == 'y':
            self.gold -= 2
            cards = self.gameMaster.giveCard(3)
            print('you got: ' + cards[0].name + '(1), ' + cards[1].name + '(2), ' + cards[2].name + '(3)')
            for card in cards:
                self.hand.append(card)
            cards.clear()

    def graveyard_action(self, quart):
        if not self.all_actions['graveyard_action'] or self.gold < 1: return False # у игрока нет кладбища или денег
        choise = input(self.name + ' can buy quarter ' + quart.name + ' for 1 gold(y/n) ')
        if choise == 'y':
            self.hand.append(quart)
            self.gold -= 1
            return True
        else: return False

    def greatwall_bonus(self, quarter):
        if self.all_actions['greatwall_bonus'] and quarter.name != 'greatwall':
            return 1
        else: return 0

    def dropCharList(self):
        self.charList.clear()

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