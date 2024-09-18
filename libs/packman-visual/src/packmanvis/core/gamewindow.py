from packmanvis.core.widgets.maze import MazeWidget
from packmanvis.types.maze import Maze
from PyQt6.QtWidgets import QMainWindow, QWidget


class PackmanWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super(PackmanWindow, self).__init__(parent)
        self.setWindowTitle("Pacman Inc.")
        self.maze = Maze(shape=(10, 20))
        self._setup_layout()

    def _setup_layout(self) -> None:
        widget = MazeWidget(self.maze, parent=self)
        self.setCentralWidget(widget)
