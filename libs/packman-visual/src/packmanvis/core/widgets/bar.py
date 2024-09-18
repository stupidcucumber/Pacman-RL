from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget


class HeartWidget(QLabel):
    def __init__(self, parent: QWidget | None = None) -> None:
        super(HeartWidget, self).__init__(parent)
        self.empty_heart = QPixmap("ui:empty_heart.png")
        self.full_heart = QPixmap("ui:full_heart.png")
        self.setPixmap(self.full_heart)
        self.resize(self.pixmap().width(), self.pixmap().height())


class LevelWidget(QLabel):
    def __init__(self, level: int, parent: QWidget | None = None) -> None:
        super(LevelWidget, self).__init__(parent)
        self.level = level
        self.setText(f"Level: {self.level}")
        self.setMaximumWidth(100)


class ScoreWidget(QLabel):
    def __init__(self, score: int, parent: QWidget | None = None) -> None:
        super(ScoreWidget, self).__init__(parent)
        self.score = score
        self.setText(f"Score: {self.score}")


class HealthIndicator(QWidget):
    def __init__(self, n_hearts: int, parent: QWidget | None = None) -> None:
        super(HealthIndicator, self).__init__(parent)
        self.hearts = [HeartWidget(self) for _ in range(n_hearts)]
        self._setup_layout()

    def _setup_layout(self) -> None:
        layout = QHBoxLayout(self)
        for heart in self.hearts:
            layout.addWidget(heart)
            layout.setAlignment(heart, Qt.AlignmentFlag.AlignLeft)
        self.setMaximumWidth(len(self.hearts) * 32)


class GameInfoBar(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super(GameInfoBar, self).__init__(parent)
        self.level_widget = LevelWidget(level=1, parent=self)
        self.score_widget = ScoreWidget(score=0, parent=self)
        self.health_indicator = HealthIndicator(n_hearts=3, parent=self)
        self._setup_layout()

    def _setup_layout(self) -> None:
        layout = QHBoxLayout(self)
        for widget in [self.level_widget, self.health_indicator, self.score_widget]:
            layout.addWidget(widget)
