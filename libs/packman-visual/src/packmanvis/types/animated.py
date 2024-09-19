from __future__ import annotations

from typing import Callable


class Animated:
    def __init__(self, gif: str) -> None:
        self.gif = gif

        self.on_gif_changed_slot: Callable[..., None] | None = None

    def setGif(self, gif: str) -> None:
        self.gif = gif
        self.on_gif_changed_slot()

    def on_gif_changed(self, slot: Callable[[Animated], None]) -> None:
        self.on_gif_changed_slot = slot
