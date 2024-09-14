from packmanvis.types.wall import Wall
from PyQt6.QtWidgets import QLabel, QWidget


class WallWidget(QLabel):
    def __init__(self, wall_obj: Wall, parent: QWidget | None = None) -> None:
        super(WallWidget, self).__init__(parent)
        self.wall_obj = wall_obj
        self.setPixmap(self.wall_obj.sprite())