#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class BrowserWidget(QWebEngineView):
    def __init__(self, parent):
        super(BrowserWidget, self).__init__(parent)
        self.parent = parent
        self.load(QUrl("http://google.com"))
        self.urlChanged.connect(self.parent.urlInput.setUrl)
        self.titleChanged.connect(self.parent.setTitle)
        self.iconChanged.connect(self.parent.tabWidget.setIcon)
        self.loadFinished.connect(self.parent.addHistory)