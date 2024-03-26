### Usando Qtdarktheme para esta aula https://pyqtdarktheme.readthedocs.io/en/stable
# pip install pyqtdarktheme
# CSS style sheet for configuring style

import qdarktheme
from config import (DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR,
                       PRIMARY_COLOR)


qss = f"""
    PushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    PushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    PushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""


def themeSet(*args):
    return (qdarktheme.load_stylesheet("dark") + qss)
     
    
    

    
