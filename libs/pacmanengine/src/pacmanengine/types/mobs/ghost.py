from __future__ import annotations

import enum

from pacmanengine.types.mobs.action import Action
from pacmanengine.types.mobs.mob import Mob
from pacmanengine.types.state import State


class GhostType(enum.Enum):
    """Represents types of ghosts as in the
    original version of Pacman game. Each type
    has its own strategy for chasing player.
    """

    RED: str = "red"
    ORANGE: str = "orange"
    BLUE: str = "blue"
    GREEN: str = "pink"


class Ghost(Mob):
    def __init__(
        self,
        move_right_gif: str,
        move_left_gif: str,
        move_up_gif: str,
        move_down_gif: str,
        action: Action,
        state: State,
    ) -> None:
        super(Ghost, self).__init__(
            move_down_gif=move_down_gif,
            move_left_gif=move_left_gif,
            move_right_gif=move_right_gif,
            move_up_gif=move_up_gif,
            state=state,
            action=action,
        )

    @classmethod
    def create(cls, state: State, action: Action, ghost_type: GhostType) -> Ghost:
        """Instantiates a Ghost with the specific type.

        Parameters
        ----------
        state : State
            Initial state of the ghost.
        action : Action
            Initial action the ghost should take.
        ghost_type : GhostType
            Type of the ghost.

        Returns
        -------
        Ghost
            Ghost of the specific type.
        """
        return cls(
            state=state,
            action=action,
            move_right_gif=(
                f"animations:mobs/ghost/{ghost_type.value}/ghost_move_right.gif"
            ),
            move_left_gif=(
                f"animations:mobs/ghost/{ghost_type.value}/ghost_move_left.gif"
            ),
            move_up_gif=(f"animations:mobs/ghost/{ghost_type.value}/ghost_move_up.gif"),
            move_down_gif=(
                f"animations:mobs/ghost/{ghost_type.value}/ghost_move_down.gif"
            ),
        )
