from Game import Game

names = ['Димочка', 'Ромочка', 'Полиночка']
game = Game()
game.init(names)

while game.run():
    game.info()