from __future__ import annotations

import numpy as np
from packmanvis.algorithms.maze import generate_maze, strave_maze
from packmanvis.types.mobs import Mob

from .wall import Wall
from .wall_type import WallType


class Labirinth:
    def __init__(self, walls_layout: np.ndarray | None = None) -> None:
        self.maze = walls_layout
        self.map = Labirinth._map_from_layout(walls_layout)

    @staticmethod
    def _map_from_layout(layout: np.ndarray) -> list:
        result = []
        for y_index, y in enumerate(layout):
            row = []
            for x_index, x in enumerate(y):
                row.append(
                    Wall(type=WallType.infer(layout=layout, x=x_index, y=y_index))
                    if x == 1
                    else []
                )
            result.append(row)
        return result

    @classmethod
    def generate(cls, seed: int = 42) -> Labirinth:
        maze = generate_maze(shape=(10, 20))
        return Labirinth(walls_layout=strave_maze(maze))

    def reset(self, mobs: list[Mob]) -> None:
        pass

    def update(self, mobs: list[Mob]) -> ...:
        pass
