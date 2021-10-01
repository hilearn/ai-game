from game import Game, Player, _3X5Map, Stats


def main():
    players = [Player(stats=Stats(2, 3)), Player(stats=Stats(4, 2))]
    game = Game(_3X5Map, players)

    game.run()


if __name__ == '__main__':
    main()
