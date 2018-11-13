#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QAction

class BrowserWidget(QWebEngineView):
    def __init__(self, parent):
        super(BrowserWidget, self).__init__(parent)
        self.parent = parent
        self.page = Page(self)
        self.setPage(self.page)
        self.load(QUrl("http://google.com"))
        self.urlChanged.connect(self.parent.urlInput.setUrl)
        self.titleChanged.connect(self.parent.setTitle)
        self.iconChanged.connect(self.parent.tabWidget.setIcon)
        self.loadFinished.connect(self.parent.addHistory)
        self.page.fullScreenRequested.connect(self.page.makeFullScreen)

class Page(QWebEnginePage):
    def __init__(self, view):
        super(Page, self).__init__()
        self.parent = view.parent
        self.view = view
        self.loop = None

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        """Override javaScriptConsoleMessage to use debug log."""
        if level == QWebEnginePage.InfoMessageLevel:
            print("JS - INFO - Ligne {} : {}".format(line, msg))
        elif level == QWebEnginePage.WarningMessageLevel:
             print("JS - WARNING - Ligne {} : {}".format(line, msg))
        else:
             print("JS - ERROR - Ligne {} : {}".format(line, msg))

    def ExitFS(self):
        self.triggerAction(self.ExitFullScreen)

    def makeFullScreen(self, request):
        if request.toggleOn():
            self.fullView = QWebEngineView()
            self.exitFSAction = QAction(self.fullView)
            self.exitFSAction.setShortcut(Qt.Key_Escape)
            self.exitFSAction.triggered.connect(self.ExitFS)

            self.fullView.addAction(self.exitFSAction)
            self.setView(self.fullView)
            self.fullView.showFullScreen()
            self.fullView.raise_()
        else:
            del self.fullView
            self.setView(self.view)
        request.accept()