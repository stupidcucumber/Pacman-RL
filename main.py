import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication

from src.gamewindow import PackmanWindow

QtCore.QDir.addSearchPath("wall_sprite", "assets/s_wall")
QtCore.QDir.addSearchPath("path_sprite", "assets/s_path")
QtCore.QDir.addSearchPath("animations", "assets/animations")
QtCore.QDir.addSearchPath("ui", "assets/ui")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PackmanWindow()
    window.show()

    app.exec()
