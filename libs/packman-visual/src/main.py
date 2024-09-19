import sys

from packmanvis.core.gamewindow import PackmanWindow
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication

QtCore.QDir.addSearchPath("wall_sprite", "packmanvis/assets/s_wall")
QtCore.QDir.addSearchPath("path_sprite", "packmanvis/assets/s_path")
QtCore.QDir.addSearchPath("animations", "packmanvis/assets/animations")
QtCore.QDir.addSearchPath("ui", "packmanvis/assets/ui")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PackmanWindow()
    window.show()

    app.exec()
