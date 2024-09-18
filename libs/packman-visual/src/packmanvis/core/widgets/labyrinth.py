from packmanvis.core.widgets.animate import AnimatedWidget
from packmanvis.types.animated import Animated
from packmanvis.types.labyrinth import Labyrinth
from PyQt6.QtWidgets import QGridLayout, QWidget


class LabirinthWidget(QWidget):
    def __init__(self, labyrinth: Labyrinth, parent: QWidget | None = None) -> None:
        super(LabirinthWidget, self).__init__(parent)
        self.labyrinth = labyrinth
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
        for row_index in range(self.labyrinth.maze.nrows):
            for column_index in range(self.labyrinth.maze.ncols):
                layout.addWidget(
                    self._create_stacked_widget(
                        self.labyrinth.maze.tile(column_index, row_index).objects
                    ),
                    row_index,
                    column_index,
                )
                layout.setColumnMinimumWidth(column_index, 32)
            layout.setRowMinimumHeight(row_index, 32)
        self.setLayout(layout)
