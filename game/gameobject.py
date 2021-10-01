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
    def __init__(self, stats: Stats):
        self.stats = stats

    def decide(self) -> Action:
        pass

    def observe(self, sight):
        pass

    def create_weapon(self, action):
        return Weapon(self.weapon_stats, action, self)


player_images = ['Red.png', 'Blue.png']


class Player(GameObject):
    """Bot or Person playing"""
    images = (image for i in range(1000) for image in player_images)

    def __init__(self, weapon_stats: Stats, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weapon_stats = weapon_stats
        self.image = next(self.images)

    def damage(self, weapon):
        self.stats.health -= weapon.stats.health


class Weapon(GameObject):
    image = 'Shuriken.png'

    def __init__(self, stats: Stats, action: Action, player: Player):
        super().__init__(stats)
        self.action = action
        self.player = player

    def decide(self):
        return [self.action]
