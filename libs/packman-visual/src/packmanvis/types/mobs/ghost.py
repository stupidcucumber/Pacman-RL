from packmanvis.types.mobs.mob import Mob
from pathlib import Path
import enum


class GhostColor(enum.Enum):
    YELLOW: int = 0
    ORANGE: int = 1
    BLUE: int = 2
    GREEN: int = 3
    PURPLE: int = 4
    PINK: int = 5
    WHITE: int = 6


class Ghost(Mob):
    def __init__(self, fsprite: Path, color: GhostColor) -> None:
        super(Ghost, self).__init__(fsprite=fsprite)
        self.color = color