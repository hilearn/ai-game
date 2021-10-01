import pygame
import threading
from .gameobject import GameObject, Action, Stats


class Player(GameObject):
    """Bot or Person playing"""


class RemotePlayer(Player):
    def decide(self):
        self.socket.get_decision()

    def observe(self, sight):
        self.socket.send_sight(sight)


class KeyboardPlayer(Player):
    def __init__(self, stats: Stats):
        super().__init__(stats)
        self.key_pressed = None
        pygame.init()
        listener = threading.Thread(self.listener)
        listener.start()

    def decide(self):
        keys = self.key_pressed
        self.key_pressed = []
        if keys is not None:
            return keys
        else:
            return [Action.NOTHING]

    def listener(self):
        while True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.key_pressed[0] = Action.MOVE_LEFT
            elif keys[pygame.K_RIGHT]:
                self.key_pressed[0] = Action.MOVE_RIGHT
            elif keys[pygame.K_DOWN]:
                self.key_pressed[0] = Action.MOVE_DOWN
            elif keys[pygame.K_UP]:
                self.key_pressed[0] = Action.MOVE_UP
            elif keys[pygame.K_SPACE]:
                self.key_pressed[1] = Action.SHOOT
            # pygame.event.pump()


class Bot(Player):
    def __init__(self, stats: Stats, strategy):
        super().__init__(stats)
        self.strategy = strategy

    def decide(self):
        return self.parse(self.strategy.decide(self.state))

    def parse(self, decision: list[float]) -> Action:
        pass
