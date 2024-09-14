import enum
from PyQt6.QtGui import QPixmap


class WallType(enum.StrEnum):
    VERTICAL_OPENED: str = "packmanvis/assets/s_wall/0.png"
    


class Wall:
    def __init__(self, type: WallType) -> None:
        self.type = type
        self.pixmap: QPixmap | None = None

    def sprite(self) -> QPixmap:
        if not self.pixmap:
            self.pixmap = QPixmap(self.type.value)
        return self.pixmap