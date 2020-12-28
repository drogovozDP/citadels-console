from Player import Player
from characters import*
from Quarter import deck

class Game(): # нужны приватные методы, чтобы ограничить возможности игроков
    def __init__(self, names):
        self.max_city_size = 5
        self.deckQuar = deck # колода кварталов
        self.character = character(None, self) # пустой персонаж, он всегда взят
        self.deckChar = [Assassin(None, self), Thief(None, self), Wizard(None, self), King(None, self),
                         Bishop(None, self), Merchant(None, self), Architect(None, self), Warlord(None, self)] # все персонажи
        self.players = [] # игроки заполняются при вызове self.init()
        self.queue = [None] * 8 # порядок хода игроков
        self.firstConstruct = None
        self.init(names)

    def init(self, names):
        for name in names:
            hand = [self.deckQuar[0], self.deckQuar[1], self.deckQuar[2], self.deckQuar[3]]
            for i in range(4):
                del self.deckQuar[0]
            self.players.append(Player(name, self, hand))

    def _prepare_round(self): # каждый игрок выбирает себе персонажа
        print() # чтобы удобнее было читать в консоле(разграничение раундов)
        for player in self.players:
            print(player.name, 'выбирает :з') # временная строка
            index = player.choose_character(self.deckChar)
            self.queue[index] = player
            self.deckChar[index].player = player

    def _round(self): # по очереди вызывается каждый персонаж от 1 до 8
        for i in range(len(self.queue)):
            if self.queue[i] != None:
                print(self.queue[i].name, 'ходит :)') # временная строка
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
