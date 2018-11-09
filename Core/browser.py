#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox, QPushButton

from Core.Widgets.browserWidget import BrowserWidget
from Core.Widgets.urlInput import UrlInput
from Core.Widgets.tabWidget import TabWidget


class Browser(QWidget):
    def __init__(self):
        super(Browser, self).__init__()
        self.grid = QGridLayout()

        self.urlInput = UrlInput(self)
        self.back = QPushButton("<")
        self.forward = QPushButton(">")
        self.reload = QPushButton("↺")
        self.tabWidget = TabWidget(self)

        self.tabWidget.requestsAddTab()

        self.reload.clicked.connect(self.browserWidget.reload)
        self.back.clicked.connect(self.browserWidget.back)
        self.forward.clicked.connect(self.browserWidget.forward)

        self.grid.addWidget(self.back, 0, 0)
        self.grid.addWidget(self.reload, 0, 1)
        self.grid.addWidget(self.forward, 0, 2)
        self.grid.addWidget(self.urlInput, 0, 3)
        self.grid.addWidget(self.tabWidget, 1, 0, 1, 4)

        self.setLayout(self.grid)
        self.setGeometry(100, 100, 1200, 1200)
        self.setWindowTitle('Browthon')
        self.show()
    
    def setTitle(self):
        self.setWindowTitle(self.browserWidget.title() + " - Browthon")
        self.tabWidget.setTitle()
    
    def closeEvent(self, event):
        if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter Browthon ?", QMessageBox.Yes, QMessageBox.No) == 16384:
            event.accept()
        else:
            event.ignore()