from typing import TYPE_CHECKING

from math import pow
from PySide6.QtWidgets import QGridLayout, QPushButton
from PySide6.QtCore import Slot
from config import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isValidNumber


if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow

#class Button(QPushButton):
#    def __init__(self, text: str="Button", parent: QWidget | None = None) -> None:
#        super().__init__(text,parent)


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
        
    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)
        self.setProperty('cssClass', 'specialButton')


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', mainWindow: 'MainWindow', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        
        self.display = display
        self.info = info
        self.mainWindow = mainWindow
        self._equation = ''
        self._left = None
        self._right = None
        self._operator = None
        self._initialInfoValue = 'Insira um valor'
        self.equation = self._initialInfoValue

        self._makeGrid()

    @property
    def equation(self):
        return self._equation


    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    # faz a grid de botões da calculadora, cada um com suas propriedades
    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.backspacePressed.connect(self.display.backspace)
        self.display.escPressed.connect(self.display.clear)
        self.display.inputPressed.connect(self.display.insert)
        self.display.operatorPressed.connect(self._operatorClicked)



        for i, row in enumerate(self._grid_mask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)
                
                # statement para configurar os botões especiais
                if not isNumOrDot(buttonText):
                    self._configSpecialButton(button)

                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertButtonTextToDisplay, button)
                self._connectButtonSlot(button, slot)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot
    
    def _connectButtonSlot(self, button, slot):
        button.clicked.connect(slot)  # type: ignore

    def _configSpecialButton(self, button: Button):
        ButtonText = button.text()

        if (ButtonText == 'C'):
            slot = self._makeSlot(self._clear)
            self._connectButtonSlot(button,slot)

        if (ButtonText in '◀'):
            button.clicked.connect(self.display.backspace)

        if (ButtonText in '+-*/^') and ButtonText != '':
            slot = self._makeSlot(self._operatorClicked, ButtonText)
            self._connectButtonSlot(button, slot)

        if (ButtonText in '='):
            button.clicked.connect(self._eq)


    def _insertButtonTextToDisplay(self, button):
        newDisplayValue = self.display.text() + button.text()

        if isValidNumber(newDisplayValue):
            self.display.insert(button.text())

    def _clear(self):
        self.equation = self._initialInfoValue
        self._left = None
        self._right = None
        self._operator = None
     #   self.info.clear()
        self.display.clear()


    def _operatorClicked(self, buttonText):
        print(f'This is the operator clicked: {buttonText}')
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showErrorMessage("você não digitou nada")
            return
        
        if self._left is None:
            self._left = float(displayText)

        self._operator = buttonText
        self.equation = f"{self._left} {self._operator}  ??"

        print(f'Esse é o operador guardado: {self._operator}')


    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            self._showErrorMessage("você não digitou nada")
            return

        self._right = float(displayText)
        self.equation = f"{self._left} {self._operator} {self._right}"
        result = 0.0

        try:
            if '^' in self.equation and self._left != None:
                result = pow(self._left, self._right)
                self.display.clear()
            else:
                result = eval(self.equation)
                self.display.clear()

        except ZeroDivisionError:
            result = 'error'
            self._showErrorMessage("Divisão por zero não é possível")
        
        except OverflowError:
            result = 'error'
            self._showErrorMessage("Resultado da operação é muito grande")
        
        self.info.setText(F"{self.equation} = {result}")

        if result == 'error':
            self._left = None
            self._right = None
        else:
            self._left = result
            self._right = None


        print(result)

    def _showErrorMessage(self, text):
        msgBox = self.mainWindow.createMsgBox()
        msgBox.setText(text)
        msgBox.setWindowTitle('Erro de execução')
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

    def _showInfoMessage(self, text):
        msgBox = self.mainWindow.createMsgBox()
        msgBox.setText(text)
        msgBox.setWindowTitle('Caixa informativa')
        msgBox.setIcon(msgBox.Icon.Warning)
        msgBox.exec()







