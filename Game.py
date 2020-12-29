from Player import Player
from characters import*
from Quarter import deck
import random

class Game(): # нужны приватные методы, чтобы ограничить возможности игроков
    def __init__(self, names):
        self.max_city_size = 5
        self.deckQuar = deck # колода кварталов
        self.character = character(None, self) # пустой персонаж, он всегда взят
        self.deckChar = [Assassin(None, self), Thief(None, self), Wizard(None, self), King(None, self),
                         Bishop(None, self), Merchant(None, self), Architect(None, self), Warlord(None, self)] # все персонажи
        self.players = [] # игроки заполняются при вызове self.init()
        self.queue = [None] * 8 # порядок хода игроков
        self.firstConstruct = None # игрок, который первый достроил город
        self.init(names)

    def init(self, names):
        for name in names:
            hand = []
            for i in range(4):
                hand.append(self.deckQuar.pop(0))
            self.players.append(Player(name, self, hand))

    def _random_drop(self, hide):
        index = random.randint(0, 7)
        while self.deckChar[index].choosen: index = random.randint(0, 7)
        if not hide and index == 3:
            while index == 3:
                print('King! King!! King!!!')
                index = random.randint(0, 7)
                while self.deckChar[index].choosen: index = random.randint(0, 7)
        self.deckChar[index].choosen = True
        if not hide: print(self.deckChar[index].name, 'dropped')
        return index

    def _choosen_drop(self, player):
        player.choose_drop(self.deckChar)

    def _give_char(self, player):
        print(player.name, 'выбирает :з')
        index = player.choose_character(self.deckChar)
        self.queue[index] = player
        self.deckChar[index].player = player

    def _two_players(self):
        self._random_drop(True)
        self._give_char(self.players[0])
        for i in range(3):
            self._give_char(self.players[1 - i])
            self._choosen_drop(self.players[1 - i])

    def _three_players(self):
        self._random_drop(True)
        for i in range(2):
            for j in range(len(self.players)):
                self._give_char(self.players[j])

    def _four_players(self):
        for i in range(3):
            self._random_drop(i > 0) # сбрасываем 1го в открытую и 2ух взакрытую
        self._many_people_choose()

    def _five_players(self):
        for i in range(2):
            self._random_drop(i > 0) # сбрасываем 1го в открытую и 1го взакрытую
        self._many_people_choose()

    def _six_players(self):
        self._random_drop(True)  # сбрасываем 1го взакрытую
        self._many_people_choose()

    def _seven_players(self):
        index = self._random_drop(True)  # сбрасываем 1го взакрытую и запоминаем индекс для последнего игрока
        for i in range(len(self.players) - 1):
            self._give_char(self.players[i])
        self.deckChar[index].choosen = False # возвращаем в выбор карту для последнего игрока
        self._give_char(self.players[-1])

    def _many_people_choose(self):
        for i in range(len(self.players)):
            self._give_char(self.players[i])

    def _prepare_round(self): # каждый игрок выбирает себе персонажа
        print() # чтобы удобнее было читать в консоле(разграничение раундов)
        if len(self.players) == 2: self._two_players()
        elif len(self.players) == 3: self._three_players()
        elif len(self.players) == 4: self._four_players()
        elif len(self.players) == 5: self._five_players()
        elif len(self.players) == 6: self._six_players()
        elif len(self.players) == 7: self._seven_players()

    def _round(self): # по очереди вызывается каждый персонаж от 1 до 8
        for i in range(len(self.queue)):
            if self.queue[i] != None:
                print(self.queue[i].name, 'ходит :) (' + self.deckChar[i].name + ')') # временная строка
                self.queue[i].action(i + 1)

    def _reload(self): # забирает у всех игроков карты персонажей, делает колоду персонажей полной, опусташает очередь
        game_running = True
        for player in self.players:
            player.dropCharList()
            player.character = self.character # отдаем каждому игроку нейтрального персонажа
            if len(player.city) >= self.max_city_size: # проверка на конец игры
                game_running = False
                self._winner()

        for char in self.deckChar:
            char.choosen = False # делаем каждого персонажа НЕ выбранным
            char.alive = True # делаем каждого персонажа вновь живым(исправляем активити ассасина)
            char.robed = False # делаем каждого необоворованным, чтобы обворовать
            char.player = None # теперь карта персонажа не присовоена игроку

        for i in range(len(self.queue)): # опусташаем очередь
            self.queue[i] = None
        return  game_running

    def giveCrown(self, player):
        index = 0
        for i in range(len(self.players)):
            if player.name == self.players[i].name:
                index = i
        for i in range(index):
            peasant = self.players[0]
            del self.players[0]
            self.players.append(peasant)
        print('now king is:', self.players[0].name, 'peasants count:', len(self.players) - 1)

    def giveCard(self, count): # даем count карт игроку который вызвал этот метод
        cards = []
        for i in range(count):
            cards.append(self.deckQuar[0])
            del self.deckQuar[0]
        return cards

    def takeCard(self, cards):
        for card in cards:
            self.deckQuar.append(card)

    def graveYard(self, quarter):
        sold = False
        for player in self.players:
            if player.character.name != 'Warlord' and sold == False:
                sold = player.graveyard_action(quarter)
        if sold == False:
            self.deckQuar.append(quarter)

    def _winner(self):
        record = []
        for player in self.players:
            value = 0
            colors = {'pink': False, 'yellow': False, 'blue': False, 'green': False, 'red': False}
            for quarter in player.city:
                if quarter.name != 'hauntedcity_bonus':
                    colors[quarter.color] = True
                value += quarter.bounus()
            color_count = 0
            for col in colors:
                if colors[col]: color_count += 1
            if player.all_actions['hauntedcity_bonus'] and color_count < 5:
                color_count += 1
            if color_count == 5: value += 3
            if len(player.city) >= self.max_city_size: value += 2
            if player.name == self.firstConstruct.name: value += 2
            if player.all_actions['imperialtreasury_bonus']: value += player.gold
            if player.all_actions['maproom_bonus']: value += len(player.hand)
            record.append(value)
            player.info()
        print("\nwinner is:", self.players[record.index(max(record))].name)
        print("score:", max(record))

    def info(self): # просто дает информацию о состоянии игры
        for player in self.players:
            player.info()

    def run(self):
        self._prepare_round()
        self._round()
        return self._reload()
