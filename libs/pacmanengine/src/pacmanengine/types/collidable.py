from __future__ import annotations

from typing import Any, Callable, Type

from pacmanengine.types.state import State


class Collidable:
    """Base class for all instances that can have a collision.

    Parameters
    ----------
    state : State
        Current state of the object.
    """

    def __init__(self, state: State) -> None:
        self.on_collision_slots: dict[Type, Callable[[Collidable], bool]] = {}
        self.on_state_changed_slot: Callable[[State], None]
        self.on_destroy_slot: Callable[[], None]

        self.previous_state = None
        self.current_state = state

    def on_state_changed(self, slot: Callable[[State], None]) -> None:
        """Set callback to be called when state have been changed.

        Parameters
        ----------
        slot : Callable[[State], None]
            Function that accepts a new state.
        """
        self.on_state_changed_slot = slot

    def on_collision(
        self, collidable_type: Type, slot: Callable[[Collidable], Any]
    ) -> None:
        """Set callback to be called when state have been changed.

        Parameters
        ----------
        collidable_type : Type
            An instance of type bound to collidable.
        slot : Callable[[State], None]
            Function that accepts other collidable.
        """
        self.on_collision_slots[collidable_type] = slot

    def on_destroy(self, slot: Callable[[], None]) -> None:
        """Set callback to be called when object has beed destroyed.

        Parameters
        ----------
        slot : Callable[[State], None]
            Function that accepts not Arguments.
        """
        self.on_destroy_slot = slot

    def setState(self, state: State) -> None:
        """Sets the new state.

        Parameters
        ----------
        state : State
            The new state to be set. This will be placed instead of
            self.current_state.

        Notes
        -----
        Previous state will be equal to the current_state.
        """
        self.previous_state = self.current_state
        self.current_state = state
        self.on_state_changed_slot(state)

    def collision(self, other: Collidable) -> None:
        """Conducts a collision (being present on the same tile with
        other collidable object).

        Parameters
        ----------
        other : Collidable
            Other object that also can be collided with.
        """
        if self.on_collision_slots.get(type(other)):
            self.on_collision_slots[type(other)](other)

    def destroy(self) -> None:
        """Destroy object."""
        self.on_destroy_slot()
