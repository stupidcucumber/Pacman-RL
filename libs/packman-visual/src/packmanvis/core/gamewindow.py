from PyQt6.QtWidgets import QMainWindow, QWidget
from packmanvis.core.widgets.labirinth import LabirinthWidget
from packmanvis.types.labirinth import Labirinth


class PackmanWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super(PackmanWindow, self).__init__(parent)
        self.setWindowTitle("Pacman Inc.")
        self.labirinth = Labirinth.generate()
        self._setup_layout()
        
    def _setup_layout(self) -> None:
        widget = LabirinthWidget(
            labirinth=self.labirinth,
            parent=self
        )
        self.setCentralWidget(widget)
