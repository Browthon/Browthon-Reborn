#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QUrl

from Core.Utils.urlUtils import getGoodUrl

class UrlInput(QLineEdit):
    def __init__(self, parent):
        super(UrlInput, self).__init__(parent)
        self.parent = parent
        self.returnPressed.connect(self.enterUrl)
    
    def enterUrlGiven(self, url):
        url = getGoodUrl(self.parent.dbConnection, url)
        self.parent.browserWidget.load(QUrl(url))
    
    def enterUrl(self):
        url = self.text()
        self.enterUrlGiven(url)

    def setUrl(self):
        self.setText(self.parent.browserWidget.url().toString())