from game import Game, Player, _3X5Map


def main():
    players = [Player(), Player()]
    game = Game(_3X5Map, players)

    game.run()


if __name__ == '__main__':
    main()
