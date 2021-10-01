from enum import Enum


class Cell(Enum):
    EMPTY = 0
    WALL = 1
    # LAVA = 2


class Map:
    def __init__(self,
                 lst: list[list[Cell]],
                 spawn_points: list[tuple[int, int]]):
        self._map = lst
        self.spawn_points = spawn_points

        for y, x in self.spawn_points:
            assert (self._map[y][x] is Cell.EMPTY
                    ), "player can only spawn on an empty cell"

    def size(self):
        return (len(self._map), len(self._map[0]))


_3X5Map = Map([[Cell.EMPTY] * 5,
               [Cell.EMPTY, Cell.WALL, Cell.EMPTY, Cell.WALL, Cell.EMPTY],
               [Cell.EMPTY] * 5],
              [(1, 0), (1, 4)])
