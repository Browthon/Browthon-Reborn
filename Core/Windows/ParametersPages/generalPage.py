#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt

from Core.Widgets.pushButton import PushButton

class GeneralPage(QWidget):
    def __init__(self, parent):
        super(GeneralPage, self).__init__()
        self.parent = parent
        self.grid = QGridLayout()
        
        self.title = QLabel("Paramètres")
        self.title.setAlignment(Qt.AlignHCenter)

        self.grid.addWidget(self.title, 0, 0)
        self.setLayout(self.grid)