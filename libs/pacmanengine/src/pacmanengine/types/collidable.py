from __future__ import annotations

from typing import Any, Callable, Type

from pacmanengine.types.position import Position


class Collidable:
    """Base class for all instances that can have a collision.

    Parameters
    ----------
    position : Position
        Current position of the object.
    """

    def __init__(self, position: Position) -> None:
        self.on_collision_slots: dict[Type, Callable[[Collidable], bool]] = {}
        self.on_position_changed_slot: Callable[[Position], None]
        self.on_destroy_slot: Callable[[], None]

        self.previous_position = None
        self.current_position = position

    def on_position_changed(self, slot: Callable[[Position], None]) -> None:
        """Set callback to be called when position have been changed.

        Parameters
        ----------
        slot : Callable[[Position], None]
            Function that accepts a new position.
        """
        self.on_position_changed_slot = slot

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
        slot : Callable[[], None]
            Function that accepts not Arguments.
        """
        self.on_destroy_slot = slot

    def setPosition(self, position: Position) -> None:
        """Sets the new state.

        Parameters
        ----------
        position : Position
            The new position to be set. This will be placed instead of
            self.current_position.

        Notes
        -----
        Previous position will be equal to the current_position.
        """
        self.previous_position = self.current_position
        self.current_position = position
        self.on_position_changed_slot(position)

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
