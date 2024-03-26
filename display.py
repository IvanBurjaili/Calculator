from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from config import BIG_FONT_SIZE, TEXT_MARGINS, MINIMUM_WIDTH
from utils import isEmpty, isNumOrDot


class Display(QLineEdit):
    eqPressed = Signal()
    backspacePressed = Signal()
    escPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.congfigStyle()


    def congfigStyle(self):
        margins = [TEXT_MARGINS for _ in range(4)]
        self.setStyleSheet(f'font-size:{BIG_FONT_SIZE}px;')
        self.setMaximumHeight(2 * BIG_FONT_SIZE)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)
        self.setMinimumWidth(MINIMUM_WIDTH)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()

        isEnter = key in [Qt.Key.Key_Enter , Qt.Key.Key_Return]
        isBackspace = key in [Qt.Key.Key_Delete , Qt.Key.Key_Backspace]
        isEsc = key in [Qt.Key.Key_Escape]
        isOperator = key in [Qt.Key.Key_Plus, Qt.Key.Key_Asterisk, Qt.Key.Key_Minus,
                             Qt.Key.Key_Slash, Qt.Key.Key_P]

        if isEnter or text == '=':
            self.eqPressed.emit()
            return event.ignore()
        
        if isBackspace:
            self.backspacePressed.emit()
            return event.ignore()
        
        if isEsc:
            self.escPressed.emit()
            return event.ignore()
        
        if isOperator:
            self.operatorPressed.emit(text)
            return event.ignore()

        if isNumOrDot(text):
            if text.lower() == 'p':
                text = '^'
            self.inputPressed.emit(text)
            return event.ignore()

        if isEmpty(text):
            return event.ignore()



