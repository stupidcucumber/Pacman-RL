from pacmanengine.types.mobs.action import Action
from pacmanengine.types.mobs.mob import Mob
from pacmanengine.types.position import Position


class Pacman(Mob):
    def __init__(
        self,
        position: Position,
        action: Action,
        move_right_gif: str = "animations:mobs/pacman/pacman_move_right.gif",
        move_left_gif: str = "animations:mobs/pacman/pacman_move_left.gif",
        move_up_gif: str = "animations:mobs/pacman/pacman_move_up.gif",
        move_down_gif: str = "animations:mobs/pacman/pacman_move_down.gif",
    ) -> None:
        super(Pacman, self).__init__(
            move_down_gif=move_down_gif,
            move_left_gif=move_left_gif,
            move_right_gif=move_right_gif,
            move_up_gif=move_up_gif,
            position=position,
            action=action,
        )
