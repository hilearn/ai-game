import time
import random
from dataclasses import dataclass
from .gameobject import Action, GameObject
from .map import Cell, Map


@dataclass
class ObjectInGame:
    gameobject: GameObject
    y: int
    x: int
    size: tuple[int, int]


class Game:
    CELL_SIZE = 10  # pixels
    TICK_PER_SEC = 24  # number of ticks per second
    MAX_NUM_TICKS = 2880  # number of ticks till the end of the game

    def __init__(self, map_: Map, players: list[GameObject]):
        self.map_ = map_
        assert (len(self.map_.spawn_points) >= len(players)
                ), "Can't have more players than spawn points"
        self.clear(players)

    def clear(self, players):
        spawn_points = self.map_.spawn_points[:]  # copy
        random.shuffle(spawn_points)
        self.objects = [
            ObjectInGame(
                player,
                spawn_point[0], spawn_point[1],
                (self.CELL_SIZE // 2, self.CELL_SIZE // 2)
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
        pass

    def sight(self, object_in_game: ObjectInGame):
        pass

    def update(self):
        pass

    @property
    def ended(self):
        # FIXME:
        return (self._ended
                or (self.tick >= self.MAX_NUM_TICKS)
                or len(self.players) == 1)


class VideoGame(Game):
    pass


class RemoteGame(VideoGame):
    pass
