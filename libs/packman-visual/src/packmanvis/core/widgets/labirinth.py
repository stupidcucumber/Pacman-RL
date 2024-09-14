from packmanvis.core.widgets.path import PlaceholderWidget
from packmanvis.core.widgets.wall import WallWidget
from packmanvis.types.labirinth import Labirinth
from packmanvis.types.wall import Wall
from PyQt6.QtWidgets import QGridLayout, QWidget


class LabirinthWidget(QWidget):
    def __init__(self, labirinth: Labirinth, parent: QWidget | None = None) -> None:
        super(LabirinthWidget, self).__init__(parent)
        self.labirinth = labirinth
        self._setup_layout()

    def _setup_layout(self) -> None:
        layout = QGridLayout(self)
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)
        for row_index, row in enumerate(self.labirinth.map):
            for column_index, column in enumerate(row):
                layout.addWidget(
                    (
                        WallWidget(wall_obj=column)
                        if isinstance(column, Wall)
                        else PlaceholderWidget("path_sprite:0.png")
                    ),
                    row_index,
                    column_index,
                )
        self.setLayout(layout)
