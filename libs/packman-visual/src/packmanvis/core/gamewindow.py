from packmanvis.core.widgets.labyrinth import LabirinthWidget
from packmanvis.types.labyrinth import Labyrinth
from PyQt6.QtWidgets import QMainWindow, QWidget


class PackmanWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super(PackmanWindow, self).__init__(parent)
        self.setWindowTitle("Pacman Inc.")
        self.labyrinth = Labyrinth(shape=(10, 20))
        self._setup_layout()

    def _setup_layout(self) -> None:
        widget = LabirinthWidget(labyrinth=self.labyrinth, parent=self)
        self.setCentralWidget(widget)
