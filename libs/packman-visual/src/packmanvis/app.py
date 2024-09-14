from PyQt6.QtWidgets import QApplication
import sys


class Environment:
    def __init__(self, gui: bool = True) -> None:
        self.gui = gui
        self.application = QApplication(sys.argv)
        
    def _start_gui(self) -> None:
        
    
    def reset(self, seed: int = 42) -> ...:
        pass
    
    def step(self, action: list) -> ...:
        pass
    
    def close(self) -> None:
        pass 