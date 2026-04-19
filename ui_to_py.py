# -*- coding: utf-8 -*-
"""
Created on Sun May 26 21:56:08 2024

@author: pc
"""



from PyQt5 import uic

with open("widgets.py","w", encoding="utf-8") as fout:
    uic.compileUi("manav.ui", fout)
    
from PyQt5 import uic

with open("hakkinda_widgets.py","w", encoding="utf-8") as fout:
    uic.compileUi("hakkinda.ui", fout)
    
    
from PyQt5 import uic

with open("widgetsGiris.py","w", encoding="utf-8") as fout:
    uic.compileUi("untitled.ui", fout)