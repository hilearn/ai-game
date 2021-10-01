from dataclasses import dataclass
from enum import Enum


class Action(Enum):
    NOTHING = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_UP = 3
    MOVE_DOWN = 4
    SHOOT = 5


@dataclass
class Stats:
    speed: int
    health: int


class GameObject:
    def __init__(self, stats: Stats, weapon_stats: Stats):
        self.stats = stats
        self.weapon_stats = weapon_stats

    def decide(self) -> Action:
        pass

    def observe(self, sight):
        pass

    def create_weapon(self, action):
        return Weapon(self.weapon_stats, action, self)


class Player(GameObject):
    """Bot or Person playing"""
    def damage(self, weapon):
        self.stats.health -= weapon.stats.health


class Weapon(GameObject):
    def __init__(self, stats: Stats, action: Action, player: Player):
        super().__init__(stats)
        self.action = action
        self.player = player

    def decide(self):
        return self.action
