from __future__ import annotations

import enum

from pacmanengine.algorithms.agent.agent import Agent
from pacmanengine.algorithms.agent.ghost import (
    BlinkyAgent,
    ClydeAgent,
    InkyAgent,
    PinkyAgent,
)
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
    PINK: str = "pink"


_ghost_type_to_agent_type = {
    GhostType.RED: BlinkyAgent,
    GhostType.BLUE: InkyAgent,
    GhostType.PINK: PinkyAgent,
    GhostType.ORANGE: ClydeAgent,
}


class Ghost(Mob):
    def __init__(
        self,
        move_right_gif: str,
        move_left_gif: str,
        move_up_gif: str,
        move_down_gif: str,
        action: Action,
        state: State,
        agent: Agent | None = None,
    ) -> None:
        super(Ghost, self).__init__(
            move_down_gif=move_down_gif,
            move_left_gif=move_left_gif,
            move_right_gif=move_right_gif,
            move_up_gif=move_up_gif,
            state=state,
            action=action,
            agent=agent,
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
            agent=_ghost_type_to_agent_type[ghost_type](),
        )
