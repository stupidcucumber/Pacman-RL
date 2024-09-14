from PyQt6.QtWidgets import QApplication
from packmanvis.core.gamewindow import PackmanWindow
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PackmanWindow()
    window.show()
    
    app.exec()
    