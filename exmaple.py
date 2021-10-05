from game import Game, Player, KeyboardPlayer, Stats, PlayerStats
from game import big_map, _3X5Map


def main():
    players = [KeyboardPlayer(stats=PlayerStats(8, 3, 1),
                              weapon_stats=Stats(12, 1)),
               Player(stats=PlayerStats(8, 3, 1),
                      weapon_stats=Stats(12, 1))]
    game = Game(_3X5Map, players)

    game.run()


def main2():
    player_stats = PlayerStats(8, 3, 1)
    weapon_stats = Stats(12, 1)
    kwargs = {'stats': player_stats,
              'weapon_stats': weapon_stats}
    players = [KeyboardPlayer(**kwargs),
               Player(**kwargs),
               Player(**kwargs),
               Player(**kwargs)]
    game = Game(big_map, players)

    game.run()


if __name__ == '__main__':
    main2()
