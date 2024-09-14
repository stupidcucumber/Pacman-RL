from pathlib import Path
from packmanvis.types.mobs.action import Action
from PyQt6.QtGui import QImage


def load_sprite(fpath: Path) -> list[QImage]:
    pass


class Mob:
    def __init__(self, fsprite: Path) -> None:
        self.sprites: list[QImage] = load_sprite(fsprite)
        
    def sprite(self) -> QImage:
        pass
        
    def action(self) -> Action:
        pass