from packmanvis.core.widgets.animate import AnimatedWidget
from packmanvis.core.widgets.path import PlaceholderWidget
from packmanvis.core.widgets.wall import WallWidget
from packmanvis.types.entity import Animated
from packmanvis.types.labirinth import Labirinth
from packmanvis.types.wall import Wall
from PyQt6.QtWidgets import QGridLayout, QWidget


class LabirinthWidget(QWidget):
    def __init__(self, labirinth: Labirinth, parent: QWidget | None = None) -> None:
        super(LabirinthWidget, self).__init__(parent)
        self.labirinth = labirinth
        self._setup_layout()

    def _create_stacked_widget(self, entities: list[Animated]) -> QWidget:
        widget = QWidget()

        previous_entity = PlaceholderWidget("path_sprite:0.png", widget)
        for entity in entities:
            entity_widget = AnimatedWidget(entity, parent=previous_entity)
            previous_entity = entity_widget

        return widget

    def _setup_layout(self) -> None:
        layout = QGridLayout(self)
        layout.setSpacing(0)
        for row_index, row in enumerate(self.labirinth.map):
            for column_index, column in enumerate(row):
                layout.addWidget(
                    (
                        WallWidget(wall_obj=column)
                        if isinstance(column, Wall)
                        else self._create_stacked_widget(column)
                    ),
                    row_index,
                    column_index,
                )
        self.setLayout(layout)
