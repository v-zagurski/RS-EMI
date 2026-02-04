# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 09:43:53 2025

@author: user
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QLineEdit, QItemDelegate, QAbstractItemView

class MyTableWidget(QTableWidget):
    def __init__(self, parent = None):
       super().__init__(parent)
       self.cellDoubleClicked.connect(self.editcell)
       self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
       self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
       # self.setItemDelegate(FloatDelegate(3))
    
    def editcell(self, row, col):
        try:
            flags  = self.item(row, col).flags()
            if Qt.ItemIsEditable in flags:
                text = self.item(row, col).text()
                self.ql = QLineEdit()
                self.ql.setStyleSheet('background-color : white')
                self.ql.setText(text)
                self.ql.editingFinished.connect(lambda: self.updatecell(row, col))
                self.setCellWidget(row, col, self.ql)
        except: pass

    def updatecell(self, row, col):
        newtext = self.ql.text()
        self.item(row, col).setText(newtext)
        self.removeCellWidget(row, col)
        
class FloatDelegate(QItemDelegate):
    def __init__(self, decimals, parent=None):
        QItemDelegate.__init__(self, parent=parent)
        self.nDecimals = decimals

    def paint(self, painter, option, index):
        value = index.model().data(index, Qt.EditRole)
        try:
            number = float(value)
            painter.drawText(option.rect, Qt.AlignLeft, "{:.{}f}".format(number, self.nDecimals))
        except :
            QItemDelegate.paint(self, painter, option, index)