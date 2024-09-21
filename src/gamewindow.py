from pacmanengine.types.maze import Maze
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from src.widgets import GameInfoBar, MazeWidget, RestartButton


class PackmanWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super(PackmanWindow, self).__init__(parent)
        self.setWindowTitle("Pacman Inc.")

        self.info_bar_widget = GameInfoBar(self)
        self.maze_widget = MazeWidget(Maze(shape=(10, 20)), self)
        self.restart_button = RestartButton(self)

        self._setup_layout()

    def _setup_layout(self) -> None:
        widget = QWidget(self)
        layout = QVBoxLayout()
        for _widget in [self.info_bar_widget, self.maze_widget, self.restart_button]:
            layout.addWidget(_widget)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
