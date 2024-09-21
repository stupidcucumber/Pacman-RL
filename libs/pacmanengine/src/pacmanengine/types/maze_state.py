from dataclasses import dataclass

import numpy as np
from pacmanengine.types.position import Position


@dataclass
class MazeState:
    """State of the maze. This allegedly can be used
    to train RL agent.

    Attributes
    ----------
    ghost_positions: list[Position]
        Positions of the individual ghosts.
    pacman_position: Position
        Position of the pacman.
    score: int
        Score achieved on the current step.
    hearts: int
        Hearts left on the current step.
    """

    ghost_positions: list[Position]
    pacman_position: Position
    score: int
    hearts: int
    layout: np.ndarray
