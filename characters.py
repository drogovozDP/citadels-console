class character(): # шаблон от которого будем наследоваться
    def __init__(self, player, gameMaster):
        self.initiative = 0
        self.choosen = True
        self.player = player
        self.gameMaster = gameMaster
        self.alive = True
        self.robed = False
    def ability(self):
        print(self.initiative)
    def default(self):
        pass


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
    def _exhange_with_deck(self):
        handCards = ''
        for i in range(len(self.player.hand)):
            handCards += self.player.hand[i].name + '(' + str(i + 1) + '), '  # собираем все карты в нашей руке
        handCards = handCards[0: len(handCards) - 2]
        index_row = input('choose what to exchange: ' + handCards + ' ') + ' '
        cards = []
        index = []
        for i in range(len(index_row) // 2):
            index.append(int(index_row[i * 2]) - 1)
            cards.append(self.player.hand[index[-1]])  # здесь пользователь выбрал конкретные ненужные карты
        for card in cards:  # удаляем выбранные пользователем карты
            exict = True
            for i in range(len(self.player.hand)):
                if exict and card.name == self.player.hand[i].name:
                    del self.player.hand[i]
                    exict = False
        self.gameMaster.takeCard(cards)  # возвращаем эти карты в колоду
        new_cards = self.gameMaster.giveCard(len(index))
        for card in new_cards:
            self.player.hand.append(card)
        for card in self.player.hand:
            print(card.name)
    def _echange_with_player(self, players):
        row = ''
        for i in range(len(players)):
            row += players[i].name + '(' + str(i + 1) + '), '
        row = row[0:len(row) - 2]
        index = int(input('who? (' + row + ') ')) - 1
        self_hand = []
        enemy_hand = []
        for i in range(len(self.player.hand)):
            self_hand.append(self.player.hand[0])
            del self.player.hand[0]
        for i in range(len(players[index].hand)):
            enemy_hand.append(players[index].hand[0])
            del players[index].hand[0]
        for card in self_hand:
            players[index].hand.append(card)
        for card in enemy_hand:
            self.player.hand.append(card)
    def ability(self):
        row_p = ''
        row_h = ''
        players = []
        for card in self.player.hand:
            row_h += card.name + '(' + str(card.value) + '), '
        row_h = row_h[0: len(row_h) - 2]
        for player in self.gameMaster.players: # берем всех игроков, кроме себя
            if player.name != self.player.name:
                row_p += player.name + '(cards: ' + str(len(player.hand)) + '), '
                players.append(player)
        row_p = row_p[0: len(row_p) - 2]
        choise = input('exchange with deck(your hand:' + row_h +') or players(' + row_p + ')?(print 1 or 2) ') # делаем выбор из 2 действий
        if choise == '1': # здесь меняемся с колодой
            self._exhange_with_deck()
        if choise == '2': # здесь выбираем игрока для обмена
            self._echange_with_player(players)

class King(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 4
        self.name = 'King'
    def default(self):
        if self.player.name == self.gameMaster.players[0].name:
            return
        self.gameMaster.giveCrown(self.player)

    def ability(self):
        gold = 0
        if self.player.all_actions['schoolofmagic_bonus']: gold += 1
        for card in self.player.city:
            if card.color == 'yellow':
                gold += 1
        print('you recived ' + str(gold) + ' gold!')
        self.player.gold += gold

class Bishop(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 5
        self.name = 'Bishop'
    def ability(self):
        gold = 0
        if self.player.all_actions['schoolofmagic_bonus']: gold += 1
        for card in self.player.city:
            if card.color == 'blue':
                gold += 1
        print('you recived ' + str(gold) + ' gold!')
        self.player.gold += gold

class Merchant(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 6
        self.name = 'Merchant'
    def default(self): # в начале хода получает 1 монетку(после того как обворует вор)
        print('you just recived 1 gold!')
        self.player.gold += 1
    def ability(self):
        gold = 0
        if self.player.all_actions['schoolofmagic_bonus']: gold += 1
        for card in self.player.city:
            if card.color == 'green':
                gold += 1
        print('you recived ' + str(gold) + ' gold!')
        self.player.gold += gold

class Architect(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 7
        self.name = 'Architect'
    def default(self): # в начале хода должен получить 2 карты квартала
        cards = self.gameMaster.giveCard(2)
        row = ''
        for i in range(len(cards)):
            row += cards[i].name + '(' + str(i + 1) + '), '
            self.player.hand.append(cards[i])
        row = row[0:len(row) - 2]
        print('you just recived 2 cards!', row)
    def ability(self):
        self.player.action_pool.pop() # убираем выбор "done"
        for i in range(2):
            self.player.action_pool.append('build') # теперь игрок может посмтроить 3 раза
        self.player.action_pool.append('done') # возвращаем в конец "done"

class Warlord(character):
    def __init__(self, player, gameMaster):
        character.__init__(self, player, gameMaster)
        self.choosen = False
        self.initiative = 8
        self.name = 'Warlord'
    def destroy(self):
        players = self.gameMaster.players # просто чтобы меньше года было
        print('you have', self.player.gold)
        for i in range(len(players)): # пробегаем по всем игрокам
            row = players[i].name
            if players[i].name == self.player.name: # если мы нашли игрока с кондотьером
                row += '(you)' # подсказка игроку, что это он. Игрок может ломать свои кварталы
            row += '(' + str(i + 1) + '): '
            for quarter in players[i].city: # собираем все построенные кварталы
                value = str(quarter.value - 1 + players[i].greatwall_bonus(quarter)) # стоимость уничтожения квартала
                if quarter.name == 'keep': value = 'unbreakable'
                row += quarter.name + '(value: ' + value + '), '
            print(row) # выводим, чтобы игрок сделал выбор
        index = int(input('which player? ')) - 1
        for char in players[index].charList:
            if char.name == 'Bishop':
                print("you can't destroy Bishop's quarters")
                return
        quarters = ''
        count = 1
        values = [] # здесь будут хранитсья все цены кварталов выбранного игрока
        for quart in players[index].city:
            values.append(quart.value - 1 + players[index].greatwall_bonus(quart))  # стоимость уничтожения квартала
            if quart.name == 'keep': values[-1] = 'unbreakable'
            quarters += quart.name + '(value: ' + str(values[-1]) + ')' + '(' + str(count) + '), '
            count += 1
        choise = int(input(quarters[0:len(quarters) - 2] + ' ')) - 1 # игрок выбрал какой квартал уничтожить
        if values[choise] == 'unbreakable': return
        if self.player.gold < values[choise]: return # провевряем хватит ли денег на уничтожение
        else: self.player.gold -= values[choise]
        lost_quart = players[index].city.pop(choise) # удалили этот квартал из города и сохранили его в переменную
        lost_quart.destroyed(players[index]) # игрок теряет действие, которое давал этот квартал
        self.gameMaster.graveYard(lost_quart)
    def take_gold(self):
        gold = 0
        if self.player.all_actions['schoolofmagic_bonus']: gold += 1
        for card in self.player.city:
            if card.color == 'red':
                gold += 1
        print('you recived', gold, 'gold!')
        self.player.gold += gold
    def ability(self):
        choise_pool = ['done(1)', 'destroy quarter(2)', 'take gold(3)']
        while len(choise_pool) != 0:
            row = ''
            for ch in choise_pool:
                row += ch + ' '
            choise = input(row)
            if choise == '3':
                self.take_gold()
                choise_pool.pop()
            elif choise == '2':
                self.destroy()
                choise_pool.pop(1)
            elif choise == '1':
                choise_pool.clear()
            if len(choise_pool) == 1: choise_pool.pop()
