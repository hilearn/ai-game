import pickle
from .base_game import Game, Observation, Action


class RemoteGame(Game):
    def __init__(self, s, player):
        self.s = s
        self.player = player

    def run(self):
        self.player.connect()

        while True:
            self.player.observe(self.sight())
            self.act(self.player.decide())

    def sight(self) -> Observation:
        return pickle.loads(self.s.recv(4096))

    def act(self, actions: list[Action]):
        byte_array = pickle.dumps(actions)
        self.s.sendall(byte_array)
