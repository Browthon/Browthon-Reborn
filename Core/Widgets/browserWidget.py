#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt, QEvent, QEventLoop, QPoint, QPointF, QVariant, QTimer
from PyQt5.QtWidgets import QAction

from Core.Utils.webHitTestResult import WebHitTestResult
from Core.Utils.contextMenu import ContextMenu

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
        self.loadFinished.connect(self.parent.loadFinished)
        self.page.fullScreenRequested.connect(self.page.makeFullScreen)
        self.viewSource = QAction(self)
        self.viewSource.setShortcut(Qt.Key_F2)
        self.viewSource.triggered.connect(self.page.vSource)
        self.addAction(self.viewSource)

    def event(self, event):
        if event.type() == QEvent.ChildAdded:
            child_ev = event
            widget = child_ev.child()

            if widget:
                widget.installEventFilter(self)
            return True

        return super(BrowserWidget, self).event(event)

    def contextMenuEvent(self, event):
        hit = self.page.hitTestContent(event.pos())
        menu = ContextMenu(self, hit)
        pos = event.globalPos()
        p = QPoint(pos.x(), pos.y() + 1)
        menu.exec_(p)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.MiddleButton:
                hit = self.page.hitTestContent(event.pos())
                clickedUrl = hit.linkUrl()
                baseUrl = hit.baseUrl()
                if clickedUrl != baseUrl and clickedUrl != '':
                    if 'http://' in clickedUrl or 'https://' in clickedUrl:
                        result = clickedUrl
                    elif clickedUrl == "#":
                        result = baseUrl + clickedUrl
                    else:
                        result = "http://" + baseUrl.split("/")[2] + clickedUrl
                    self.parent.openNewOngletWithUrl(result)
                event.accept()
                return True
        return super(BrowserWidget, self).eventFilter(obj, event)

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

    def hitTestContent(self, pos):
        return WebHitTestResult(self, pos)

    def mapToViewport(self, pos):
        return QPointF(pos.x(), pos.y())

    def executeJavaScript(self, scriptSrc):
        self.loop = QEventLoop()
        self.result = QVariant()
        QTimer.singleShot(250, self.loop.quit)

        self.runJavaScript(scriptSrc, self.callbackJS)
        self.loop.exec_()
        self.loop = None
        return self.result

    def callbackJS(self, res):
        if self.loop is not None and self.loop.isRunning():
            self.result = res
            self.loop.quit()

    def vSource(self):
        if "view-source:http" in self.url().toString():
            self.load(QUrl(self.url().toString().split("view-source:")[1]))
        else:
            self.triggerAction(self.ViewSource)

    def cutAction(self):
        self.triggerAction(self.Cut)

    def copyAction(self):
        self.triggerAction(self.Copy)

    def pasteAction(self):
        self.triggerAction(self.Paste)

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