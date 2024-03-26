# Applicativo de calculadora em pythons e pysede6 (pyQT) - seguindo curso Udemy de python dev
# Tipografias:
# snake_case
# PascalCase
# camelCase

import sys

from main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from config import WINDOW_ICON_PATH
from info import Info
from display import Display
from style import themeSet
from buttons import Button, ButtonsGrid

if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    window = MainWindow()

    # aplica o tema dark
    

    # Define o ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info
    info = Info()
    window.addWidgetToVLayout(info)    

    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid de botões
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    # Executa tudo
    window.adjustFixedSize()
    
    window.show()
    app.setStyleSheet(themeSet())
    app.exec()


# Main.py End