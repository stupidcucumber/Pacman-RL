from pacmanengine.types import Animated, Maze
from PyQt6.QtWidgets import QGridLayout, QWidget

from src.widgets.animate import AnimatedWidget


class MazeWidget(QWidget):
    def __init__(self, maze: Maze, parent: QWidget | None = None) -> None:
        super(MazeWidget, self).__init__(parent)
        self.maze = maze
        self._setup_layout()

    def _create_stacked_widget(self, entities: list[Animated]) -> QWidget:
        if len(entities) == 0:
            raise ValueError("Tile must have at lest one entity!")
        widget = QWidget()
        previous_entity = AnimatedWidget(entities[0], parent=widget)
        for entity in entities[1:]:
            entity_widget = AnimatedWidget(entity, parent=previous_entity)
            previous_entity = entity_widget
        return widget

    def _setup_layout(self) -> None:
        layout = QGridLayout(self)
        layout.setSpacing(0)
        for row_index in range(self.maze.nrows):
            for column_index in range(self.maze.ncols):
                layout.addWidget(
                    self._create_stacked_widget(
                        self.maze.tile(column_index, row_index).objects
                    ),
                    row_index,
                    column_index,
                )
                layout.setColumnMinimumWidth(column_index, 32)
            layout.setRowMinimumHeight(row_index, 32)
        self.setLayout(layout)
