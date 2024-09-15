from packmanvis.types.coin import Coin
from PyQt6.QtGui import QMovie, QShowEvent
from PyQt6.QtWidgets import QLabel, QWidget


class CoinWidget(QLabel):
    def __init__(self, coin: Coin, parent: QWidget | None = None) -> None:
        super(CoinWidget, self).__init__(parent)
        self.setMovie(QMovie(coin.gif))

    def showEvent(self, a0: QShowEvent | None) -> None:
        self.movie().start()
        return super().showEvent(a0)
