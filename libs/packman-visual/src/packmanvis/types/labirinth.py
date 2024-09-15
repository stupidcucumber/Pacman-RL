from __future__ import annotations

import numpy as np
from packmanvis.algorithms.maze import generate_pacmanlike_maze
from packmanvis.types.items import Coin
from packmanvis.types.mobs import Mob

from .wall import Wall
from .wall_type import WallType


class Labirinth:
    def __init__(self, shape: tuple[int, int]) -> None:
        self.shape = shape
        self.maze: np.ndarray | None = None

    @property
    def map(self) -> list:
        if self.maze is None:
            self.maze = generate_pacmanlike_maze(shape=self.shape)
        return self._map_from_layout(self.maze)

    @staticmethod
    def _spawn_coins(maze: np.ndarray) -> np.ndarray:
        pass

    @staticmethod
    def _spawn_pacman(maze: np.ndarray) -> np.ndarray:
        pass

    @staticmethod
    def _spawn_ghosts(maze: np.ndarray) -> np.ndarray:
        pass

    def _map_from_layout(self, layout: np.ndarray) -> list:
        result = []
        for y_index, y in enumerate(layout):
            row = []
            for x_index, x in enumerate(y):
                row.append(
                    Wall(type=WallType.infer(layout=layout, x=x_index, y=y_index))
                    if x == 1
                    else [Coin()]
                )
            result.append(row)
        return result

    def reset(self, mobs: list[Mob]) -> None:
        pass

    def update(self, mobs: list[Mob]) -> ...:
        pass
