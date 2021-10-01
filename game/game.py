from enum import Enum
from .gameobject import Action, GameObject


class Cell(Enum):
    EMPTY = 0
    WALL = 1
    # LAVA = 2


class Map:
    def __init__(self, lst):
        """lst is 2 dim map of the game"""

class Game:
    CELL_SIZE = 10  # pixels
    TICK_PER_SEC = 24  # number of ticks per second
    MAX_NUM_TICKS = 2880  # number of ticks till the end of the game

    def __init__(self, map_: Map, players: list[Player]):
        self.map_ = map_
        self.gameobjects = players
        self.tick = 0
        self._ended = False

    def run(self):
        for self.tick in range(self.MAX_NUM_TICKS):
            for gameobject in self.gameobjects:
                gameobject.observe(self.sight(player))

            for gameobject in self.gameobjects:
                self.act(gameobject.decide())

            self.update()

    def act(self, player: Player, action: Action):
        pass

    def sight(self):
        pass

    def update(self):
        pass

    @property
    def ended(self):
        # FIXME:
        return self._ended or (self.tick >= self.MAX_NUM_TICKS) or len(self.players) == 1


class VideoGame(Game):
    pass


class RemoteGame(VideoGame):
    pass
