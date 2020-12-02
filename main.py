from Game import Game

names = ['Димочка', 'Ромочка']
game = Game()
game.init(names)

while game.run:
    game.prepare_round()
    game.round()
    game.reload()
    game.info()