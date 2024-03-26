from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt
from config import SMALL_FONT_SIZE

class Info(QLabel):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.configStyle()


    def configStyle(self):
        self.setStyleSheet(f"font-size: {SMALL_FONT_SIZE}px")
        self.setAlignment(Qt.AlignmentFlag.AlignRight)