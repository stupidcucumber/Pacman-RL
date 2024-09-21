from dataclasses import dataclass

from pacmanengine.types.mobs import Action
from pacmanengine.types.state import State


@dataclass
class MazeState:
    """State of the maze. This allegedly can be used
    to train RL agent.

    Attributes
    ----------
    ghost_states: list[State]
        States of the individual ghosts.
    ghost_actions: list[Action]
        Current actions that are taken by the ghosts.
    pacman_state: State
        State of the pacman.
    pacman_action: Action
        Action that is currently pacman takes.
    score: int
        Score achieved on the current step.
    hearts: int
        Hearts left on the current step.
    """

    ghost_states: list[State]
    ghost_actions: list[Action]
    pacman_state: State
    pacman_action: Action
    score: int
    hearts: int
