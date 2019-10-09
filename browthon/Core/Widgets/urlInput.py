#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtWidgets import QLineEdit
from PySide2.QtCore import QUrl

from browthon.Core.Utils.urlUtils import getgoodurl


class UrlInput(QLineEdit):
    def __init__(self, parent):
        super(UrlInput, self).__init__(parent)
        self.parent = parent
        self.returnPressed.connect(self.enterurl)
    
    def enterurlgiven(self, url):
        url, error = getgoodurl(self.parent.dbConnection, url)
        if error == "SESSION":
            self.parent.opennewongletwithurllist(url.split(" | "))
        else:
            self.parent.browserWidget.load(QUrl(url))
            self.parent.parameterWindow.addonsPage.launchaddons("enterUrl", url)
    
    def enterurl(self):
        url = self.text()
        self.enterurlgiven(url)

    def seturl(self):
        self.setText(self.parent.browserWidget.url().toString())
