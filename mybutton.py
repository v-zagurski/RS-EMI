# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 10:36:32 2025

@author: user
"""

from PySide6.QtWidgets import QPushButton

class MyPushButton(QPushButton):
    def __init__(self, parent = None):
       super().__init__(parent)
       
       self.setAutoDefault(False)
       self.setDefault(False)