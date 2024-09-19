from PyQt6.QtWidgets import QPushButton, QWidget


class RestartButton(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super(RestartButton, self).__init__(parent)
        self.setText("Restart")
