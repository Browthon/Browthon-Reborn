#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox

from Core.Widgets.browserWidget import BrowserWidget
from Core.Widgets.urlInput import UrlInput


class Browser(QWidget):
    def __init__(self):
        super(Browser, self).__init__()
        self.grid = QGridLayout()

        self.browserWidget = BrowserWidget(self)
        self.urlInput = UrlInput(self)

        self.grid.addWidget(self.browserWidget, 1, 0)
        self.grid.addWidget(self.urlInput, 0, 0)

        self.setLayout(self.grid)
        self.show()
    
