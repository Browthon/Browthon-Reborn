#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class BrowserWidget(QWebEngineView):
    def __init__(self, parent):
        super(BrowserWidget, self).__init__(parent)
        self.parent = parent
        self.load(QUrl("http://google.com"))