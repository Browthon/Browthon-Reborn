#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox, QPushButton, QMenu
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

from Core.Widgets.browserWidget import BrowserWidget
from Core.Widgets.urlInput import UrlInput
from Core.Widgets.tabWidget import TabWidget
from Core.Widgets.pushButton import PushButton
from Core.Utils.dbUtils import DBConnection
from Core.Utils.urlUtils import getGoodUrl
from Core.Windows.parameterWindow import ParameterWindow


class Browser(QWidget):
    def __init__(self):
        super(Browser, self).__init__()
        self.dbConnection = DBConnection("data.db")
        self.dbConnection.createDB()

        self.createUI()

        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.parameterWindow = ParameterWindow(self)

        self.show()

    def setTitle(self):
        self.setWindowTitle(self.browserWidget.title() + " - Browthon")
        self.tabWidget.setTitle()
    
    def openNewOngletWithUrl(self, url):
        url = getGoodUrl(url)
        self.tabWidget.requestsAddTab()
        self.browserWidget.load(QUrl(url))

    def openParameter(self):
        self.parameterWindow.setWindowModality(Qt.ApplicationModal)
        self.parameterWindow.show()
    
    def fav(self):
        bookmarks = self.dbConnection.executeWithReturn("""SELECT * FROM bookmarks""")
        find = False
        for i in bookmarks:
            if i[2] == self.browserWidget.url().toString():
                self.dbConnection.executeWithoutReturn("""DELETE FROM bookmarks WHERE id = ?""", (i[0],))
                self.bookmark.setIcon(QIcon("Icons/NavigationBar/noFav.png"))
                find = True
        if not find:
            self.dbConnection.executeWithoutReturn("""INSERT INTO bookmarks(name, url) VALUES(?, ?)""", (self.browserWidget.title(), self.browserWidget.url().toString()))
            self.bookmark.setIcon(QIcon("Icons/NavigationBar/yesFav.png"))
        self.parameterWindow.bookmarksPage.showUpdate()
    
    def loadFinished(self):
        self.addHistory()
        bookmarks = self.dbConnection.executeWithReturn("""SELECT * FROM bookmarks""")
        find = False
        for i in bookmarks:
            if i[2] == self.browserWidget.url().toString():
                self.bookmark.setIcon(QIcon("Icons/NavigationBar/yesFav.png"))
                find = True
        if not find:
            self.bookmark.setIcon(QIcon("Icons/NavigationBar/noFav.png"))
        self.parameterWindow.bookmarksPage.showUpdate()
    
    def addHistory(self):
        self.dbConnection.executeWithoutReturn("""INSERT INTO history(name, url) VALUES(?, ?)""", (self.browserWidget.title(), self.browserWidget.url().toString()))
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R or event.key() == Qt.Key_F5:
            self.browserWidget.reload()
        elif event.key() == Qt.Key_N:
            self.tabWidget.requestsAddTab()
        elif event.key() == Qt.Key_Q:
            self.tabWidget.requestsRemoveTab(self.tabWidget.currentIndex())
        elif event.key() == Qt.Key_H:
            self.historyWindow.setWindowModality(Qt.ApplicationModal)
            self.historyWindow.showUpdate()
        elif event.key() == Qt.Key_F:
            self.bookmarksWindow.setWindowModality(Qt.ApplicationModal)
            self.bookmarksWindow.showUpdate()
    
    def closeEvent(self, event):
        if self.tabWidget.count() == 0:
            self.dbConnection.disconnect()
            event.accept()
        elif self.tabWidget.count() != 1:
            if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter tous les onglets ?", QMessageBox.Yes, QMessageBox.No) == 16384:
                self.dbConnection.disconnect()
                event.accept()
            else:
                event.ignore()
                self.tabWidget.requestsRemoveTab(self.tabWidget.currentIndex())
        else:
            if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter Browthon ?", QMessageBox.Yes, QMessageBox.No) == 16384:
                self.dbConnection.disconnect()
                event.accept()
            else:
                event.ignore()

    def createUI(self):
        self.grid = QGridLayout()

        self.urlInput = UrlInput(self)
        self.back = PushButton("", QIcon("Icons/NavigationBar/back.png"))
        self.forward = PushButton("", QIcon("Icons/NavigationBar/forward.png"))
        self.reload = PushButton("", QIcon("Icons/NavigationBar/reload.png"))
        self.bookmark = PushButton("", QIcon("Icons/NavigationBar/noFav.png"))
        self.home = PushButton("", QIcon("Icons/NavigationBar/home.png"))
        self.parameter = PushButton("", QIcon("Icons/NavigationBar/param.png"))
        self.tabWidget = TabWidget(self)

        self.tabWidget.requestsAddTab()

        self.reload.clicked.connect(self.browserWidget.reload)
        self.back.clicked.connect(self.browserWidget.back)
        self.forward.clicked.connect(self.browserWidget.forward)
        self.bookmark.clicked.connect(self.fav)
        self.home.clicked.connect(lambda: self.urlInput.enterUrlGiven(self.dbConnection.executeWithReturn("""SELECT home FROM parameters""")[0][0]))
        self.parameter.clicked.connect(self.openParameter)

        self.grid.addWidget(self.back, 0, 0)
        self.grid.addWidget(self.reload, 0, 1)
        self.grid.addWidget(self.forward, 0, 2)
        self.grid.addWidget(self.urlInput, 0, 3)
        self.grid.addWidget(self.bookmark, 0, 4)
        self.grid.addWidget(self.home, 0, 5)
        self.grid.addWidget(self.parameter, 0, 6)
        self.grid.addWidget(self.tabWidget, 1, 0, 1, 7)

        self.setLayout(self.grid)
        self.showMaximized()
        self.setWindowTitle('Browthon')