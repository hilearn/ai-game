import socket
import pickle
from game import RemoteGame, KeyboardPlayer


def main(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        args, kwargs = pickle.loads(s.recv(4096))
        player = KeyboardPlayer(*args, **kwargs)
        RemoteGame(s, player).run()


if __name__ == '__main__':
    main('127.0.0.1', 3000)

