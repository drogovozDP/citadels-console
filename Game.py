from Player import Player
from characters import*
from Quarter import deck

class Game(): # нужны приватные методы, чтобы ограничить возможности игроков
    def __init__(self):
        # self.run = True
        self.deckQuar = deck # колода кварталов
        self.character = character(None, self) # пустой персонаж, он всегда взят
        self.deckChar = [Assassin(None, self), Thief(None, self), Wizard(None, self), King(None, self),
                         Bishop(None, self), Merchant(None, self), Architect(None, self), Warlord(None, self)] # все персонажи
        self.players = [] # игроки заполняются при вызове self.init()
        self.queue = [None] * 8 # порядок хода игроков

    def init(self, names):
        for name in names:
            hand = [self.deckQuar[0], self.deckQuar[1], self.deckQuar[2], self.deckQuar[3]]
            for i in range(4):
                del self.deckQuar[0]
            self.players.append(Player(name, self, hand))

    def _prepare_round(self): # каждый игрок выбирает себе персонажа
        for player in self.players:
            print(player.name, 'выбирает :з') # временная строка
            index = player.choose_character(self.deckChar)
            self.queue[index] = player
            self.deckChar[index].player = player

    def _round(self): # по очереди вызывается каждый персонаж от 1 до 8
        for player in self.queue:
            if player != None:
                print(player.name, 'ходит :)') # временная строка
                player.action()

    def _reload(self): # забирает у всех игроков карты персонажей, делает колоду персонажей полной, опусташает очередь
        game_running = True
        for player in self.players:
            player.character = self.character # отдаем каждому игроку нейтрального персонажа
            if len(player.city) == 3: # проверка на конец игры
                # self.run = False
                game_running = False
                self._winner()

        for char in self.deckChar:
            char.choosen = False # делаем каждого персонажа НЕ выбранным
            char.alive = True # делаем каждого персонажа вновь живым(исправляем активити ассасина)
            char.robed = False # делаем каждого необоворованным, чтобы обворовать
            char.player = None # теперь карта персонажа не присовоен игроку

        for i in range(len(self.queue)): # опусташаем очередь
            self.queue[i] = None
        return  game_running

    def giveCard(self, count): # даем count карт игроку который вызвал этот метод
        cards = []
        for i in range(count):
            cards.append(self.deckQuar[0])
            del self.deckQuar[0]
        return cards

    def takeCard(self, cards):
        for card in cards:
            self.deckQuar.append(card)

    def _winner(self):
        record = []
        for player in self.players:
            value = 0
            for quarter in player.city:
                value += quarter.value
            record.append(value)
        print("winner is:", self.players[record.index(max(record))].name)

    def info(self): # просто дает информацию о состоянии игры
        for player in self.players:
            player.info()

    def run(self):
        self._prepare_round()
        self._round()
        return self._reload()
