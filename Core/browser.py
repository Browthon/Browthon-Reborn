#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QMainWindow

from Core.Widgets.browserWidget import BrowserWidget


class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.grid = QGridLayout()
        self.browserWidget = BrowserWidget(self)
        self.setLayout(self.grid)
        self.show()