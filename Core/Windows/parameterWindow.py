#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from Core.Widgets.pushButton import PushButton
from Core.Windows.ParametersPages.generalPage import GeneralPage

class ParameterWindow(QWidget):
    def __init__(self, parent):
        super(ParameterWindow, self).__init__()
        self.parent = parent
        self.setWindowTitle('Paramètres')
        self.grid = QGridLayout()
        
        self.title = QLabel("Paramètres")
        self.title.setAlignment(Qt.AlignHCenter)

        self.generalPage = GeneralPage(self)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.tabWidget.addTab(self.generalPage, QIcon("logo.png"), "")
        
        self.grid.addWidget(self.title, 0, 0)
        self.grid.addWidget(self.tabWidget, 1, 0)
        self.setLayout(self.grid)
        