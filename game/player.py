import pygame
import threading
from .gameobject import Player, Action, Stats
from .game import Observation


class RemotePlayer(Player):
    def decide(self):
        self.socket.get_decision()

    def observe(self, sight):
        self.socket.send_sight(sight)


class KeyboardPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_pressed = [Action.NOTHING, Action.NOTHING]
        pygame.init()
        listener = threading.Thread(target=self.listener, daemon=True)
        listener.start()

    def decide(self):
        keys = self.key_pressed
        self.key_pressed = [Action.NOTHING, Action.NOTHING]
        return keys

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
            pygame.event.pump()


class Bot(Player):
    def __init__(self, strategy, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
