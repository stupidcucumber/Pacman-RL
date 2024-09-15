from __future__ import annotations

import numpy as np
from packmanvis.algorithms.maze import generate_pacmanlike_maze
from packmanvis.types.animated import Animated
from packmanvis.types.items import Coin
from packmanvis.types.mobs import Ghost, Mob, Pacman

from .wall import Wall
from .wall_type import WallType

COIN_WEIGHT = 2
PACMAN_WEIGHT = 5
GHOST_WEIGHT = 13


class Labirinth:
    def __init__(self, shape: tuple[int, int]) -> None:
        self.shape = shape
        self.maze: np.ndarray | None = None

    @property
    def map(self) -> list:
        if self.maze is None:
            empty_maze = generate_pacmanlike_maze(shape=self.shape)
            self.maze = Labirinth.populate_maze(empty_maze)
        return self._map_from_layout(self.maze)

    @staticmethod
    def populate_maze(maze: np.ndarray) -> np.ndarray:
        maze_coins = Labirinth._spawn_coins(maze)
        maze_ghosts = Labirinth._spawn_ghosts(maze_coins)
        return Labirinth._spawn_pacman(maze_ghosts)

    @staticmethod
    def _spawn_coins(maze: np.ndarray) -> np.ndarray:
        maze[maze == 0] = COIN_WEIGHT
        return maze

    @staticmethod
    def _spawn_pacman(maze: np.ndarray) -> np.ndarray:
        maze[1, maze.shape[1] // 2] = PACMAN_WEIGHT
        return maze

    @staticmethod
    def _spawn_ghosts(maze: np.ndarray) -> np.ndarray:
        maze[maze.shape[0] // 2, maze.shape[1] // 2] = 0
        maze[maze.shape[0] // 2, maze.shape[1] // 2] = 4 * GHOST_WEIGHT
        return maze

    @staticmethod
    def _unravel_weight(maze: np.ndarray, x: int, y: int) -> Wall | list[Animated]:
        if maze[y, x] == 1:
            return Wall(type=WallType.infer(layout=maze, x=x, y=y))

        result = []
        weight = maze[y, x]
        while weight > 0:
            if weight - GHOST_WEIGHT >= 0:
                result.append(Ghost())
                weight -= GHOST_WEIGHT
            elif weight - PACMAN_WEIGHT >= 0:
                result.append(Pacman())
                weight -= PACMAN_WEIGHT
            elif weight - COIN_WEIGHT >= 0:
                result.append(Coin())
                weight -= COIN_WEIGHT

        return result

    def _map_from_layout(self, layout: np.ndarray) -> list:
        result = []
        for y_index, y in enumerate(layout):
            row = []
            for x_index, _ in enumerate(y):
                row.append(Labirinth._unravel_weight(maze=layout, x=x_index, y=y_index))
            result.append(row)
        return result

    def reset(self, mobs: list[Mob]) -> None:
        pass

    def update(self, mobs: list[Mob]) -> ...:
        pass
