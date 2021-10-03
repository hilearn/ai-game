from game import Game, Player, KeyboardPlayer, _3X5Map, Stats, PlayerStats


def main():
    players = [KeyboardPlayer(stats=PlayerStats(8, 3, 1),
                              weapon_stats=Stats(12, 1)),
               Player(stats=PlayerStats(8, 3, 1),
                      weapon_stats=Stats(12, 1))]
    game = Game(_3X5Map, players)

    game.run()


if __name__ == '__main__':
    main()
