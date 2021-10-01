from .gameobject import GameObject, Action



class Player(GameObject):
    """Bot or Person playing"""


class RemotePlayer(Player):
    def decide(self):
        self.socket.get_decision()

    def observe(self, sight):
        self.socket.send_sight(sight)


class KeyboardPlayer(Player):
    def __init__(self):
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
    def __init__(self, strategy):
        self.strategy = strategy

    def decide(self):
        return self.parse(self.strategy.decide(self.state))

    def parse(self, decision: list[float]) -> Action:
        pass


class Weapon(GameObject):
    def __init__(self, action):
        self.action = action

    def decide(self):
        return self.action

