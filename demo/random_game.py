from game import Game, Bot, Stats, PlayerStats, big_map
from strategy import RandomStrategy


def main():
    player_stats = PlayerStats(8, 3, 1)
    weapon_stats = Stats(16, 1)
    kwargs = {'stats': player_stats,
              'weapon_stats': weapon_stats,
              'strategy': RandomStrategy()}
    players = [Bot(**kwargs),
               Bot(**kwargs),
               Bot(**kwargs),
               Bot(**kwargs)]
    game = Game(big_map, players, ticks_per_sec=0)

    game.run()


if __name__ == '__main__':
    for i in range(500):
        main()
