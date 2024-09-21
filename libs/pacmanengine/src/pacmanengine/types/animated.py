from __future__ import annotations

from typing import Callable


class Animated:
    """Base class for all objects that have sprite and
    will be displayed on the map.

    Parameters
    ----------
    gif : str
        Default gif to be displayed.
    """

    def __init__(self, gif: str) -> None:
        self.gif = gif
        self.on_gif_changed_slot: Callable[..., None] | None = None

    def setGif(self, gif: str) -> None:
        """Change current gif to the one provided.

        Parameters
        ----------
        gif : str
            Path to the gif to be used instead.
        """
        self.gif = gif
        self.on_gif_changed_slot()

    def on_gif_changed(self, slot: Callable[..., None]) -> None:
        """Set callback on gif being changed.

        Parameters
        ----------
        slot : Callable[[Animated], None]
            Function to call when gif has changed.
        """
        self.on_gif_changed_slot = slot
