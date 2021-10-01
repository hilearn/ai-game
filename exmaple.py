from game import Game, Player, KeyboardPlayer, _3X5Map, Stats


def main():
    players = [KeyboardPlayer(stats=Stats(8, 3)),
               Player(stats=Stats(8, 3))]
    game = Game(_3X5Map, players)

    game.run()


if __name__ == '__main__':
    main()
