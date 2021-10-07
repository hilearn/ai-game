import numpy as np
from game import Cell, Bot


class Strategy:
    def decide(self, bot: Bot) -> list[float]:
        pass


class RandomStrategy:
    def decide(self, bot: Bot) -> list[float]:
        return np.random.random(6)


class NNStrategy(Strategy):
    def __init__(self, model):
        self.model = model

    def decide(self, bot: Bot) -> list[float]:
        return self.model.feed(self._input_from_state(bot))

    @staticmethod
    def _input_from_state(bot: Bot):
        input_map = bot.state.map_._map
        layer_num = 3
        input_matrix = np.zeros((layer_num,
                                 bot.state.cell_size * len(input_map),
                                 bot.state.cell_size * len(input_map[0]),))
        for i, row in enumerate(input_map):
            for j, cell in enumerate(row):
                if cell == Cell.WALL:
                    y1 = i * bot.state.cell_size
                    y2 = y1 + bot.state.cell_size
                    z1 = j * bot.state.cell_size
                    z2 = z1 + bot.state.cell_size
                    input_matrix[0, y1:y2, z1:z2] = 1
        for obj in bot.state.objects:
            if obj.gameobject == bot:
                layer = 2
            else:
                layer = 1
            size_y, size_x = obj.size
            input_matrix[layer, obj.y:obj.y + size_y, obj.x:obj.x + size_x] = 1
        return input_matrix
