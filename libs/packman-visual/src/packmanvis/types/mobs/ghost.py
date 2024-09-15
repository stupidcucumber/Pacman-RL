import enum

from packmanvis.types.mobs.mob import Mob


class GhostColor(enum.Enum):
    YELLOW: int = 0
    ORANGE: int = 1
    BLUE: int = 2
    GREEN: int = 3
    PURPLE: int = 4
    PINK: int = 5
    WHITE: int = 6


class Ghost(Mob):
    def __init__(self, gif: str, color: GhostColor) -> None:
        super(Ghost, self).__init__(gif=gif)
        self.color = color
