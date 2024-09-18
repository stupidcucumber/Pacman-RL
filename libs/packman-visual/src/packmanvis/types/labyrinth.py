from __future__ import annotations

import numpy as np
from packmanvis.algorithms.maze import generate_pacmanlike_maze
from packmanvis.types.maze import Maze
from packmanvis.types.mobs.ghost import GhostType

COIN_WEIGHT = 2
PACMAN_WEIGHT = 5
GHOST_WEIGHT = 13


class Labyrinth:
    def __init__(self, shape: tuple[int, int]) -> None:
        self.shape = shape
        self._maze: Maze | None = None

    @property
    def maze(self) -> Maze:
        if self._maze is None:
            empty_layout = generate_pacmanlike_maze(shape=self.shape)
            populated_layout = Labyrinth.populate_maze(empty_layout)
            self._maze = Maze(populated_layout)
        return self._maze

    @staticmethod
    def _spawn_coins(layout: np.ndarray) -> np.ndarray:
        layout[layout == 0] = COIN_WEIGHT
        return layout

    @staticmethod
    def _spawn_pacman(layout: np.ndarray) -> np.ndarray:
        layout[1, layout.shape[1] // 2 - 1] = PACMAN_WEIGHT
        return layout

    @staticmethod
    def _spawn_ghosts(layout: np.ndarray) -> np.ndarray:
        layout[layout.shape[0] // 2 + 1, layout.shape[1] // 2 - 1] = 0
        layout[layout.shape[0] // 2 + 1, layout.shape[1] // 2 - 1] = (
            len(GhostType._member_names_) * GHOST_WEIGHT
        )
        return layout

    @staticmethod
    def populate_maze(layout: np.ndarray) -> np.ndarray:
        layout_with_coins = Labyrinth._spawn_coins(layout)
        layout_with_ghosts = Labyrinth._spawn_ghosts(layout_with_coins)
        return Labyrinth._spawn_pacman(layout_with_ghosts)
