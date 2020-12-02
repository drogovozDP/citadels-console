from Player import Player
from characters import*
from Quarter import deck

class Game(): # нужны приватные методы, чтобы ограничить возможности игроков
    def __init__(self):
        self.run = True
        self.deckQuar = deck # колода кварталов
        self.character = character() # пустой персонаж, он всегда взят
        self.deckChar = [Assassin(), Thief(), Wizard(), King(), Bishop(), Merchant(), Architect(), Warlord()] # все персонажи
        self.players = [] # игроки заполняются при вызове self.init()
        self.queue = [None] * 8 # порядок хода игроков

    def init(self, names):
        for name in names:
            hand = [self.deckQuar[0], self.deckQuar[1], self.deckQuar[2], self.deckQuar[3]]
            del self.deckQuar[0], self.deckQuar[1], self.deckQuar[2], self.deckQuar[3]
            self.players.append(Player(name, self, hand))

    def prepare_round(self): # каждый игрок выбирает себе персонажа
        for player in self.players:
            print(player.name, 'выбирает :з') # временная строка
            index = player.choose_character(self.deckChar)
            self.queue[index] = player

    def round(self): # по очереди вызывается каждый персонаж от 1 до 8
        for player in self.queue:
            if player != None:
                print(player.name, 'ходит :)') # временная строка
                player.action()

    def reload(self): # забирает у всех игроков карты персонажей, делает колоду персонажей полной, опусташает очередь
        for player in self.players:
            player.character = self.character # отдаем каждому игроку нейтрального персонажа
            if len(player.city) == 2: # проверка на конец игры
                self.run = False

        for char in self.deckChar: # делаем каждого персонажа НЕ выбранным
            char.choosen = False

        for i in range(len(self.queue)): # опусташаем очередь
            self.queue[i] = None

    def winner(self):
        pass

    def info(self): # просто дает информацию о состоянии игры
        for player in self.players:
            player.info()