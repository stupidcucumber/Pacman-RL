from __future__ import annotations

from typing import Any, Callable


class Animated:
    def __init__(self, gif: str) -> None:
        self.gif = gif

        self.on_collision_slot: Callable[[Animated], Any] | None = None
        self.on_gif_changed_slot: Callable[..., None] | None = None

    def setGif(self, gif: str) -> None:
        self.gif = gif
        self.on_gif_changed_slot()

    def on_collision(self, slot: Callable[[Animated], Any]) -> None:
        self.on_collision_slot = slot

    def on_gif_changed(self, slot: Callable[[Animated], None]) -> None:
        self.on_gif_changed_slot = slot
