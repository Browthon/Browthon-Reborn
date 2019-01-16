#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt, QEvent, QEventLoop, QPoint, QPointF, QVariant, QTimer
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QKeySequence

from browthon.Core.Utils.webHitTestResult import WebHitTestResult
from browthon.Core.Utils.contextMenu import ContextMenu


class BrowserWidget(QWebEngineView):
    def __init__(self, parent):
        super(BrowserWidget, self).__init__(parent)
        self.parent = parent
        self.page = Page(self)
        self.page.setParent(self)
        self.setPage(self.page)
        self.load(QUrl("http://google.com"))
        self.urlChanged.connect(self.parent.urlInput.seturl)
        self.titleChanged.connect(lambda: self.parent.settitle(self))
        self.loadFinished.connect(lambda: self.parent.loadfinished(self))
        self.loadStarted.connect(lambda: self.parent.tabWidget.settitleloading(self))
        self.iconChanged.connect(lambda: self.parent.tabWidget.seticon(self))
        self.page.fullScreenRequested.connect(self.page.makefullscreen)

        self.viewSource = QAction(self)
        self.viewSource.setShortcut(QKeySequence(Qt.Key_F2))
        self.viewSource.triggered.connect(self.page.vsource)
        self.reloadAction = QAction(self)
        self.reloadAction.setShortcut(QKeySequence("Ctrl+R"))
        self.reloadAction.triggered.connect(self.reload)
        self.addTabAction = QAction(self)
        self.addTabAction.setShortcut(QKeySequence("Ctrl+T"))
        self.addTabAction.triggered.connect(self.parent.tabWidget.requestsaddtab)
        self.closeTabAction = QAction(self)
        self.closeTabAction.setShortcut(QKeySequence("Ctrl+Q"))
        self.closeTabAction.triggered.connect(lambda: self.parent.tabWidget.requestsremovetab(
            self.parent.tabWidget.indexOf(self)))
        self.forwardAction = QAction(self)
        self.forwardAction.setShortcut(QKeySequence("Ctrl+N"))
        self.forwardAction.triggered.connect(self.forward)
        self.backAction = QAction(self)
        self.backAction.setShortcut(QKeySequence("Ctrl+B"))
        self.backAction.triggered.connect(self.back)

        self.addAction(self.viewSource)
        self.addAction(self.reloadAction)
        self.addAction(self.addTabAction)
        self.addAction(self.closeTabAction)
        self.addAction(self.forwardAction)
        self.addAction(self.backAction)

    def event(self, event):
        if event.type() == QEvent.ChildAdded:
            child_ev = event
            widget = child_ev.child()

            if widget:
                widget.installEventFilter(self)
            return True

        return super(BrowserWidget, self).event(event)

    def contextMenuEvent(self, event):
        hit = self.page.hittestcontent(event.pos())
        menu = ContextMenu(self, hit)
        pos = event.globalPos()
        p = QPoint(pos.x(), pos.y() + 1)
        menu.exec_(p)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.MiddleButton:
                hit = self.page.hittestcontent(event.pos())
                clickedurl = hit.linkurl()
                baseurl = hit.baseurl()
                if clickedurl != baseurl and clickedurl != '':
                    if 'http://' in clickedurl or 'https://' in clickedurl:
                        result = clickedurl
                    elif clickedurl == "#":
                        result = baseurl + clickedurl
                    else:
                        result = "http://" + baseurl.split("/")[2] + clickedurl
                    self.parent.opennewongletwithurl(result, False)
                event.accept()
                return True
        return super(BrowserWidget, self).eventFilter(obj, event)


class Page(QWebEnginePage):
    def __init__(self, view):
        super(Page, self).__init__()
        self.parent = view.parent
        self.view = view
        self.result = QVariant()
        self.fullView = QWebEngineView()
        self.exitFSAction = QAction(self.fullView)
        self.loop = None

    def javaScriptConsoleMessage(self, level, msg, line, sourceid):
        """Override javaScriptConsoleMessage to use debug log."""
        if level == QWebEnginePage.InfoMessageLevel:
            print("JS - INFO - Ligne {} : {}".format(line, msg))
        elif level == QWebEnginePage.WarningMessageLevel:
            print("JS - WARNING - Ligne {} : {}".format(line, msg))
        else:
            print("JS - ERROR - Ligne {} : {}".format(line, msg))

    def hittestcontent(self, pos):
        return WebHitTestResult(self, pos)

    def maptoviewport(self, pos):
        return QPointF(pos.x(), pos.y())

    def executejavascript(self, scriptsrc):
        self.loop = QEventLoop()
        self.result = QVariant()
        QTimer.singleShot(250, self.loop.quit)

        self.runJavaScript(scriptsrc, self.callbackjs)
        self.loop.exec_()
        self.loop = None
        return self.result

    def callbackjs(self, res):
        if self.loop is not None and self.loop.isRunning():
            self.result = res
            self.loop.quit()

    def vsource(self):
        if "view-source:http" in self.url().toString():
            self.load(QUrl(self.url().toString().split("view-source:")[1]))
        else:
            self.triggerAction(self.ViewSource)

    def exitfs(self):
        self.triggerAction(self.ExitFullScreen)

    def makefullscreen(self, request):
        if request.toggleOn():
            self.fullView = QWebEngineView()
            self.exitFSAction = QAction(self.fullView)
            self.exitFSAction.setShortcut(Qt.Key_Escape)
            self.exitFSAction.triggered.connect(self.exitfs)

            self.fullView.addAction(self.exitFSAction)
            self.setView(self.fullView)
            self.fullView.showFullScreen()
            self.fullView.raise_()
        else:
            del self.fullView
            self.setView(self.view)
        request.accept()
