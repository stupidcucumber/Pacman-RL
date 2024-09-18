from __future__ import annotations

import enum

from packmanvis.types.mobs.mob import Mob
from packmanvis.types.mobs.state import State


class GhostType(enum.Enum):
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
        state: State,
    ) -> None:
        super(Ghost, self).__init__(
            move_down_gif=move_down_gif,
            move_left_gif=move_left_gif,
            move_right_gif=move_right_gif,
            move_up_gif=move_up_gif,
            state=state,
        )
        self.health = 3
        self.score = 0

    @classmethod
    def create(cls, state: State, ghost_type: GhostType) -> Ghost:
        return cls(
            state=state,
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
