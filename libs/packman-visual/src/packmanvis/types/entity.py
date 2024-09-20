from __future__ import annotations

from typing import Any, Callable, Type

from packmanvis.types.action import Action
from packmanvis.types.state import State


class Entity:
    def __init__(self, state: State, action: Action) -> None:
        self.on_collision_slots: dict[Type, Callable[[Entity], bool]] = {}
        self.on_state_changed_slot: Callable[[State], None]
        self.on_action_changed_slot: Callable[[Action], None]
        self.on_destroy_slot: Callable[[], None]

        self.previous_state = None
        self.current_state = state

        self.current_action = action

    def on_action_changed(self, slot: Callable[[Action], None]) -> None:
        self.on_action_changed_slot = slot

    def on_state_changed(self, slot: Callable[[State], None]) -> None:
        self.on_state_changed_slot = slot

    def on_collision(self, entity_type: Type, slot: Callable[[Entity], Any]) -> None:
        self.on_collision_slots[entity_type] = slot

    def on_destroy(self, slot: Callable[[], None]) -> None:
        self.on_destroy_slot = slot

    def setAction(self, action: Action) -> None:
        self.current_action = action
        self.on_action_changed_slot(action)

    def setState(self, state: State) -> None:
        self.previous_state = self.current_state
        self.current_state = state
        self.on_state_changed_slot(state)

    def collision(self, other: Entity) -> None:
        if self.on_collision_slots.get(type(other)):
            self.on_collision_slots[type(other)](other)

    def destroy(self) -> None:
        self.on_destroy_slot()
