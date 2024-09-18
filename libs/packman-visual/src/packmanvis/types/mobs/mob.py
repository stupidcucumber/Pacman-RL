from __future__ import annotations

from typing import Callable

from packmanvis.types.animated import Animated
from packmanvis.types.mobs.action import Action
from packmanvis.types.mobs.state import State


class Mob(Animated):
    def __init__(
        self,
        move_right_gif: str,
        move_left_gif: str,
        move_up_gif: str,
        move_down_gif: str,
        state: State,
    ) -> None:
        super(Mob, self).__init__(gif=move_right_gif)
        self.action_to_gif: dict[Action, str] = {
            Action.MOVE_UP: move_up_gif,
            Action.MOVE_DOWN: move_down_gif,
            Action.MOVE_LEFT: move_left_gif,
            Action.MOVE_RIGHT: move_right_gif,
        }

        self.action_to_move_slot: dict[Action, Callable[[Mob], bool] | None] = {
            Action.MOVE_UP: None,
            Action.MOVE_DOWN: None,
            Action.MOVE_LEFT: None,
            Action.MOVE_RIGHT: None,
        }

        self.previous_state: State | None = None
        self.current_state: State = state

        self.on_move_end_slot: Callable[..., None] | None = None

    def on_move(self, action: Action, slot: Callable[[Mob], bool]) -> None:
        """Callback that will be called when object will try to move.

        Parameters
        ----------
        action : Action
            Action that will be associated with the callback.
        slot : Callable[[Mob], bool]
            Callback that will be called when mooving. Callback
            must accept mob object and return whether movement is
            successful.
        """
        self.action_to_move_slot[action] = slot

    def on_move_end(self, slot: Callable[..., None]) -> None:
        """Callback that will be called at the end of the movement.

        Parameters
        ----------
        slot : Callable[..., None]
            Callback that accepts no arguments and returns no
            values.
        """
        self.on_move_end_slot = slot

    def movement_end(self) -> None:
        if self.previous_state.action != self.current_state.action:
            self.setGif(self.action_to_gif[self.current_state.action])
        self.on_move_end_slot()

    def action(self) -> Action:
        raise NotImplementedError("This action needs to be implemented!")

    def move(self) -> Action:
        action = self.action()

        self.temp_state = self.previous_state
        self.previous_state = self.current_state

        movement_succeed = self.action_to_move_slot[action](self)

        if movement_succeed:
            self.current_state.action = action
            self.movement_end()
        else:
            self.previous_state = self.temp_state
