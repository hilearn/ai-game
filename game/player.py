from .gameobject import Player, Action, Stats


class RemotePlayer(Player):
    def decide(self):
        self.socket.get_decision()

    def observe(self, sight):
        self.socket.send_sight(sight)


class KeyboardPlayer(Player):
    def __init__(self, stats: Stats):
        super().__init__(stats)
        self.key_pressed = None

    def decide(self):
        if self.key_pressed is not None:
            return self.key_pressed
        else:
            return Action.NOTHING

    def listener(self):
        while True:
            self.key_pressed = self.keyboard_listener.getkey()


class Bot(Player):
    def __init__(self, stats: Stats, strategy):
        super().__init__(stats)
        self.strategy = strategy

    def decide(self):
        return self.parse(self.strategy.decide(self.state))

    def parse(self, decision: list[float]) -> Action:
        pass
