import socket
from game import Game, RemotePlayer, _3X5Map, Stats


def main(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        players = [RemotePlayer(s,
                                stats=Stats(8, 3),
                                weapon_stats=Stats(12, 1),
                                image='Blue.png'),
                   RemotePlayer(s,
                                stats=Stats(8, 3),
                                weapon_stats=Stats(12, 1),
                                image='Red.png')]

        game = Game(_3X5Map, players)
        game.run()


if __name__ == '__main__':
    main('127.0.0.1', 3000)
