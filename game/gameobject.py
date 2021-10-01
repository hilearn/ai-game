from enum import Enum


class Action(Enum):
    NOTHING = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_UP = 3
    MOVE_DOWN = 4
    SHOOT = 5


class GameObject:
    def decide(self) -> Action:
        pass

    def observe(self, sight):
        pass


class Player(GameObject):
    """Bot or Person playing"""


class Weapon(GameObject):
    def __init__(self, action):
        self.action = action

    def decide(self):
        return self.action
