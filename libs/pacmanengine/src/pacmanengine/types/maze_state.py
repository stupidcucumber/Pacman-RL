from dataclasses import dataclass

import numpy as np
from pacmanengine.types.state import State


@dataclass
class MazeState:
    """State of the maze. This allegedly can be used
    to train RL agent.

    Attributes
    ----------
    ghost_states: list[State]
        States of the individual ghosts.
    pacman_state: State
        State of the pacman.
    score: int
        Score achieved on the current step.
    hearts: int
        Hearts left on the current step.
    """

    ghost_states: list[State]
    pacman_state: State
    score: int
    hearts: int
    layout: np.ndarray
