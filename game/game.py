import time
import random
from enum import Enum
from dataclasses import dataclass
from .gameobject import Action, GameObject, Player, Weapon
from .map import Cell, Map


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def to_action(self):
        if self is self.UP:
            return Action.MOVE_UP
        elif self is self.LEFT:
            return Action.MOVE_LEFT
        elif self is self.RIGHT:
            return Action.MOVE_RIGHT
        elif self is self.DOWN:
            return Action.MOVE_DOWN
        else:
            assert False


@dataclass
class Rect:
    top: int
    bottom: int
    left: int
    right: int


@dataclass
class ObjectInGame:
    gameobject: GameObject
    y: int  # top
    x: int  # left
    direction: Direction
    size: tuple[int, int]

    @property
    def rect(self):
        return Rect(self.y, self.y + self.size[0],
                    self.x, self.x + self.size[1])


@dataclass
class PlayerInGame(ObjectInGame):
    last_shot: float = None  # timestamp


@dataclass
class Observation:
    map_: Map
    objects: list[ObjectInGame]
    cell_size: int


class Game:
    CELL_SIZE = 200  # pixels
    FENCE_SIZE = 50
    TICK_PER_SEC = 24  # number of ticks per second
    MAX_NUM_TICKS = 2880  # number of ticks till the end of the game

    def __init__(self, map_: Map, players: list[Player]):
        self.map_ = map_
        self.borders = Rect(0, self.map_.size()[0] * self.CELL_SIZE - 1,
                            0, self.map_.size()[1] * self.CELL_SIZE - 1)
        assert (len(self.map_.spawn_points) >= len(players)
                ), "Can't have more players than spawn points"
        self.clear(players)

    def clear(self, players: list[Player]):
        spawn_points = self.map_.spawn_points[:]  # copy
        random.shuffle(spawn_points)
        half_cell = self.CELL_SIZE // 2
        quarter_cell = self.CELL_SIZE // 4
        self.objects = [
            PlayerInGame(
                player,
                spawn_point[0] * self.CELL_SIZE + quarter_cell,
                spawn_point[1] * self.CELL_SIZE + quarter_cell,
                Direction.UP,
                (half_cell, half_cell)
            )
            for player, spawn_point in zip(players, spawn_points)
        ]

        self.tick = 0
        if self.TICK_PER_SEC == 0:
            self.tick_length = 0
        else:
            self.tick_length = 1 / self.TICK_PER_SEC

    def run(self):
        self.end = time.time()
        for self.tick in range(self.MAX_NUM_TICKS):
            delta = self.end - time.time()
            time.sleep(max(delta, 0))
            if delta < -2:
                start = time.time()
            else:
                start = self.end
            self.end = start + self.tick_length

            for object_ in self.objects:
                object_.gameobject.observe(self.sight(object_))

            for object_ in self.objects[:]:
                self.act(object_, object_.gameobject.decide())
            if self.ended:
                break

    def act(self, object_: ObjectInGame, actions: list[Action]):
        if actions is None:
            return
        eighth_cell = self.CELL_SIZE // 8
        for action in actions:
            speed = object_.gameobject.stats.speed
            if action == Action.NOTHING:
                continue
            elif action == Action.MOVE_LEFT:
                self.move(object_, Direction.LEFT, speed)
            elif action == Action.MOVE_RIGHT:
                self.move(object_, Direction.RIGHT, speed)
            elif action == Action.MOVE_UP:
                self.move(object_, Direction.UP, speed)
            elif action == Action.MOVE_DOWN:
                self.move(object_, Direction.DOWN, speed)
            elif action == Action.SHOOT:
                if (object_.last_shot is None
                        or self.end - object_.last_shot
                        >= object_.gameobject.stats.reload_time):
                    self.objects.append(
                        ObjectInGame(
                            object_.gameobject.create_weapon(
                                object_.direction.to_action()),
                            object_.y,
                            object_.x,
                            object_.direction,
                            (eighth_cell, eighth_cell)
                        )
                    )
                    object_.last_shot = self.end

    def move(self, object_: ObjectInGame, direction: Direction, speed: int):
        object_.direction = direction

        if direction is Direction.LEFT:
            speed = min(speed, object_.rect.left - self.borders.left)
            if Cell.WALL in {self.get_cell(object_.rect.left - speed,
                                           object_.rect.top),
                             self.get_cell(object_.rect.left - speed,
                                           object_.rect.bottom)}:
                speed2 = object_.rect.left % self.CELL_SIZE
                speed = min(speed, speed2)
        elif direction is Direction.RIGHT:
            speed = min(speed, self.borders.right - object_.rect.right)
            if Cell.WALL in {self.get_cell(object_.rect.right + speed,
                                           object_.rect.top),
                             self.get_cell(object_.rect.right + speed,
                                           object_.rect.bottom)}:
                speed2 = self.CELL_SIZE - object_.rect.right % self.CELL_SIZE
                if speed2 == self.CELL_SIZE:
                    speed2 = 0
                speed = min(speed, speed2)
        elif direction is Direction.UP:
            speed = min(speed, object_.rect.top - self.borders.top)
            if Cell.WALL in {self.get_cell(object_.rect.right,
                                           object_.rect.top - speed),
                             self.get_cell(object_.rect.left,
                                           object_.rect.top - speed)}:
                speed2 = object_.rect.top % self.CELL_SIZE
                speed = min(speed, speed2)
        elif direction is Direction.DOWN:
            speed = min(speed, self.borders.bottom - object_.rect.bottom)
            if Cell.WALL in {self.get_cell(object_.rect.right,
                                           object_.rect.bottom + speed),
                             self.get_cell(object_.rect.left,
                                           object_.rect.bottom + speed)}:
                speed2 = self.CELL_SIZE - object_.rect.bottom % self.CELL_SIZE
                if speed2 == self.CELL_SIZE:
                    speed2 = 0
                speed = min(speed, speed2)

        if speed == 0:
            if isinstance(object_.gameobject, Weapon):
                self.objects.remove(object_)
            return

        if direction is Direction.LEFT:
            yx = (0, -speed)
        elif direction is Direction.RIGHT:
            yx = (0, speed)
        elif direction is Direction.UP:
            yx = (-speed, 0)
        elif direction is Direction.DOWN:
            yx = (speed, 0)

        object_.x += yx[1]
        object_.y += yx[0]

        self.triggers(object_)

    def get_cell(self, x, y):
        return self.map_[y // self.CELL_SIZE][x // self.CELL_SIZE]

    def triggers(self, object_: ObjectInGame):
        for other in self.objects:
            if other is object_:
                continue
            self.collide(other, object_)

    def collide(self, obj1: ObjectInGame, obj2: ObjectInGame):
        if (isinstance(obj1.gameobject, Weapon) and
                isinstance(obj2.gameobject, Player)):
            player = obj2.gameobject
            weapon = obj1.gameobject
            weapon_obj = obj1
            player_obj = obj2
        elif (isinstance(obj2.gameobject, Weapon) and
              isinstance(obj1.gameobject, Player)):
            player = obj1.gameobject
            weapon = obj2.gameobject
            weapon_obj = obj2
            player_obj = obj1
        else:
            return
        if weapon.player is not player and self.hit(obj1, obj2):
            player.damage(weapon)
            self.objects.remove(weapon_obj)
            if player.health <= 0:
                self.objects.remove(player_obj)
                weapon.player.kill()
            else:
                weapon.player.hit()

    @staticmethod
    def hit(first: ObjectInGame, second: ObjectInGame):
        # If one rectangle is on left side of other
        if (first.rect.left > second.rect.right) or (
                second.rect.left > first.rect.right):
            return False

        # If one rectangle is above other
        if (first.rect.bottom < second.rect.top) or (
                second.rect.bottom < first.rect.top):
            return False

        return True

    def sight(self, object_in_game: ObjectInGame) -> Observation:
        return Observation(self.map_, self.objects, self.CELL_SIZE)

    @property
    def ended(self):
        return ((self.tick >= self.MAX_NUM_TICKS)
                or len(self.objects) == 1)


class RemoteGame(Game):
    pass


class TrainableGame(Game):
    TICK_SIZE = 0
