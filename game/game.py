import time
import random
from enum import Enum
from dataclasses import dataclass
from .gameobject import Action, GameObject, Player, Weapon, Stats
from .map import Cell, Map


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


@dataclass
class Rect:
    top: int
    bottom: int
    left: int
    right: int

    def distance(self, other, direction):
        pass


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
class Observation:
    map_: Map
    objects: list[ObjectInGame]


class Game:
    CELL_SIZE = 10  # pixels
    TICK_PER_SEC = 24  # number of ticks per second
    MAX_NUM_TICKS = 2880  # number of ticks till the end of the game

    def __init__(self, map_: Map, players: list[GameObject]):
        self.map_ = map_
        self.borders = Rect(0, self.map_.size()[0] * self.CELL_SIZE,
                            0, self.map_.size()[1] * self.CELL_SIZE)
        assert (len(self.map_.spawn_points) >= len(players)
                ), "Can't have more players than spawn points"
        self.clear(players)

    def clear(self, players):
        spawn_points = self.map_.spawn_points[:]  # copy
        random.shuffle(spawn_points)
        half_cell = self.CELL_SIZE // 2
        quarter_cell = self.CELL_SIZE // 4
        self.objects = [
            ObjectInGame(
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

        self._ended = False

    def run(self):
        end = time.time()
        for self.tick in range(self.MAX_NUM_TICKS):
            time.sleep(max(time.time() - end, 0))
            start = end
            end = start + self.tick_length

            for object_ in self.objects:
                object_.gameobject.observe(self.sight(object_))

            for gameobject in self.objects:
                self.act(object_, object_.gameobject.decide())

            self.update()

    def act(self, object_: ObjectInGame, actions: list[Action]):
        if actions is None:
            return
        for action in actions:
            speed = 1
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
                # TODO:
                pass

    def move(self, object_: ObjectInGame, direction: Direction, speed: int):
        object_.direction = direction

        if direction is Direction.LEFT:
            speed = min(speed, object_.x - self.borders.left)
        elif direction is Direction.RIGHT:
            speed = min(speed, self.borders.right - object_.x)
        elif directoin is Direction.UP:
            speed = min(speed, object_.y - self.borders.top)
        elif direction is Direction.DOWN:
            speed = min(speed, self.borders.bottom - object_.y)

        if direction is Direction.LEFT:
            yx = (0, -speed)
        elif direction is Direction.RIGHT:
            yx = (0, speed)
        elif direction is Direction.UP:
            yx = (-speed, 0)
        elif directoin is Direction.DOWN:
            yx = (speed, 0)

        object_.x += yx[1]
        object_.y += yx[0]

        self.triggers(object_)


    def triggers(self, object_: ObjectInGame):
        for other in self.objects:
            if other is object_:
                continue
            if self.hit(other, object_):
                pass

    @staticmethod
    def hit(first, second):
        return False

    def sight(self, object_in_game: ObjectInGame) -> Observation:
        return Observation(self.map_, self.objects)

    def update(self):
        """Updates on game independent of specific objects"""

    @property
    def ended(self):
        # FIXME:
        return (self._ended
                or (self.tick >= self.MAX_NUM_TICKS)
                or len(self.players) == 1)


class RemoteGame(Game):
    pass


class TrainableGame(Game):
    TICK_SIZE = 0
