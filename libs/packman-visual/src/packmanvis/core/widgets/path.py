from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QPixmap


class PlaceholderWidget(QLabel):
    def __init__(self, sprite_path: str, parent: QWidget | None = None) -> None:
        super(PlaceholderWidget, self).__init__(parent)
        self.setPixmap(
            QPixmap(sprite_path)
        )
        self.resize(
            self.pixmap().width(),
            self.pixmap().height()
        )