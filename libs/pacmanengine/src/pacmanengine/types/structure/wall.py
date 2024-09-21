from __future__ import annotations

from pacmanengine.types.animated import Animated

from .wall_type import WallType


class Wall(Animated):

    @classmethod
    def create(cls, wall_type: WallType) -> Wall:
        return cls(gif=f"animations:structure/wall/{wall_type.value}.gif")
