from enum import Enum


class Cell(Enum):
    EMPTY = 0
    WALL = 1
    # LAVA = 2

    @classmethod
    def convert(cls, char):
        return {
            's': cls.EMPTY,
            '.': cls.EMPTY,
            '#': cls.WALL
        }[char]


class Map:
    def __init__(self,
                 lst: list[list[Cell]],
                 spawn_points: list[tuple[int, int]],
                 cell_size: int):
        self._map = lst
        self.spawn_points = spawn_points
        self.cell_size = cell_size

        for y, x in self.spawn_points:
            assert (self._map[y][x] is Cell.EMPTY
                    ), "player can only spawn on an empty cell"

    def size(self):
        return (len(self._map), len(self._map[0]))

    def __getitem__(self, ind):
        return self._map[ind]

    @classmethod
    def convert(cls, str_map):
        lines = str_map.split('\n')
        assert all(len(line) == len(lines[0]) for line in lines)

        spawn_points = [
            (y, x)
            for y, line in enumerate(lines)
            for x, char in enumerate(line)
            if char == 's'
        ]

        return (
            [[Cell.convert(char)
              for char in line]
             for line in lines],
            spawn_points)


_3X5map_str = """
.....
s#.#s
.....
""".strip()

_3X5Map = Map(*Map.convert(_3X5map_str), 200)

big_map_str = """
.........
.##...#s.
.s#...##.
..#......
.......#.
.#.....#.
.##...##s
.s.......
""".strip()

big_map = Map(*Map.convert(big_map_str), 80)
