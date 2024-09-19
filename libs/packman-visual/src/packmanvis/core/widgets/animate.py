from packmanvis.types.animated import Animated
from PyQt6.QtGui import QMovie, QShowEvent
from PyQt6.QtWidgets import QLabel, QWidget


class AnimatedWidget(QLabel):
    def __init__(self, animate: Animated, parent: QWidget | None = None) -> None:
        super(AnimatedWidget, self).__init__(parent)
        self.setMovie(QMovie(animate.gif))

    def showEvent(self, a0: QShowEvent | None) -> None:
        self.movie().start()
        self.resize(32, 32)
        return super().showEvent(a0)
