from .game import Observation
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
        self.state = None

    def decide(self):
        return self._parse(self.strategy.decide(bot=self))

    def observe(self, sight: Observation):
        self.state = sight

    @staticmethod
    def _parse(decision: list[float]) -> list[Action]:
        sorted_decision = sorted(range(len(decision)),
                                 key=lambda k: decision[k])
        actions = [Action(sorted_decision[-1])]
        if sorted_decision[-2] == 5:
            actions.append(Action.SHOOT)
        return actions
