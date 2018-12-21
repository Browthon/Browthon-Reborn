#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineProfile

from Core.Widgets.urlInput import UrlInput
from Core.Widgets.tabWidget import TabWidget
from Core.Widgets.pushButton import PushButton
from Core.Utils.dbUtils import DBConnection
from Core.Utils.urlUtils import getgoodurl
from Core.Utils.dateUtils import getdate
from Core.Utils.themeUtils import parsetheme
from Core.Windows.parameterWindow import ParameterWindow

import os


class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.dbConnection = DBConnection("data.db")
        self.dbConnection.createdb()

        self.centralWidget = QWidget(self)
        self.grid = QGridLayout(self.centralWidget)

        self.urlInput = UrlInput(self)
        self.urlInput.setObjectName("addressBar")
        self.back = PushButton("", QIcon("Icons/NavigationBar/back.png"), "backButton")
        self.forward = PushButton("", QIcon("Icons/NavigationBar/forward.png"), "forwardButton")
        self.reload = PushButton("", QIcon("Icons/NavigationBar/reload.png"), "reloadButton")
        self.bookmark = PushButton("", QIcon("Icons/NavigationBar/noFav.png"), "favButton")
        self.home = PushButton("", QIcon("Icons/NavigationBar/home.png"), "homeButton")
        self.parameter = PushButton("", QIcon("Icons/NavigationBar/param.png"), "paramButton")
        self.tabWidget = TabWidget(self)
        self.tabWidget.setObjectName("tabBar")

        self.tabWidget.requestsaddtab()
        self.back.setFlat(True)
        self.forward.setFlat(True)
        self.reload.setFlat(True)
        self.bookmark.setFlat(True)
        self.home.setFlat(True)
        self.parameter.setFlat(True)

        self.reload.clicked.connect(self.browserWidget.reload)
        self.back.clicked.connect(self.browserWidget.back)
        self.forward.clicked.connect(self.browserWidget.forward)
        self.bookmark.clicked.connect(self.fav)
        self.home.clicked.connect(lambda: self.urlInput.enterurlgiven(
            self.dbConnection.executewithreturn("""SELECT home FROM parameters""")[0][0]))
        self.parameter.clicked.connect(self.openparameter)

        self.grid.addWidget(self.back, 0, 0)
        self.grid.addWidget(self.reload, 0, 1)
        self.grid.addWidget(self.forward, 0, 2)
        self.grid.addWidget(self.urlInput, 0, 3)
        self.grid.addWidget(self.bookmark, 0, 4)
        self.grid.addWidget(self.home, 0, 5)
        self.grid.addWidget(self.parameter, 0, 6)
        self.grid.addWidget(self.tabWidget, 1, 0, 1, 7)

        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.setCentralWidget(self.centralWidget)
        self.showMaximized()
        self.setWindowTitle('Browthon')

        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        if self.dbConnection.executewithreturn("""SELECT js FROM parameters""")[0][0] == "Activé":
            QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        else:
            QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
        self.parameterWindow = ParameterWindow(self)
        QWebEngineProfile.defaultProfile().\
            downloadRequested.connect(self.parameterWindow.downloadPage.downloadrequested)

        theme = self.dbConnection.executewithreturn("""SELECT theme FROM parameters""")[0][0]
        if theme == "":
            self.applytheme("")
        else:
            if os.path.exists("Themes/"+theme+"/theme.json"):
                self.applytheme("Themes/"+theme)
            else:
                print("Le theme "+theme+" n'existe pas/plus.")
                self.applytheme("")

        self.show()

    def settitle(self):
        self.setWindowTitle(self.browserWidget.title() + " - Browthon")
        self.tabWidget.settitle()

    def applytheme(self, folder):
        if folder == "" or folder == "Themes/":
            self.setStyleSheet("")
            self.parameterWindow.setStyleSheet("")
        else:
            with open(folder+"/main.bss", 'r') as fichier:
                bss = parsetheme(fichier.read())
                self.setStyleSheet(bss)
                self.parameterWindow.setStyleSheet(bss)
    
    def opennewongletwithurl(self, url):
        url, temp = getgoodurl(self.dbConnection, url)
        self.tabWidget.requestsaddtab()
        self.browserWidget.load(QUrl(url))

    def opennewongletwithurllist(self, urllist):
        for i in urllist:
            if i != urllist[0]:
                self.tabWidget.requestsaddtab()
                self.browserWidget.load(QUrl(i))
            else:
                self.browserWidget.load(QUrl(i))

    def openparameter(self):
        self.parameterWindow.setWindowModality(Qt.ApplicationModal)
        self.parameterWindow.show()
    
    def fav(self):
        bookmarks = self.dbConnection.executewithreturn("""SELECT * FROM bookmarks""")
        find = False
        for i in bookmarks:
            if i[2] == self.browserWidget.url().toString():
                self.dbConnection.executewithoutreturn("""DELETE FROM bookmarks WHERE id = ?""", (i[0],))
                self.bookmark.setIcon(QIcon("Icons/NavigationBar/noFav.png"))
                find = True
        if not find:
            self.dbConnection.executewithoutreturn("""INSERT INTO bookmarks(name, url, date) VALUES(?, ?, ?)""", (
                self.browserWidget.title(), self.browserWidget.url().toString(),
                getdate()))
            self.bookmark.setIcon(QIcon("Icons/NavigationBar/yesFav.png"))
        self.parameterWindow.bookmarksPage.showupdate()
    
    def loadfinished(self):
        self.addhistory()
        bookmarks = self.dbConnection.executewithreturn("""SELECT * FROM bookmarks""")
        find = False
        for i in bookmarks:
            if i[2] == self.browserWidget.url().toString():
                self.bookmark.setIcon(QIcon("Icons/NavigationBar/yesFav.png"))
                find = True
        if not find:
            self.bookmark.setIcon(QIcon("Icons/NavigationBar/noFav.png"))
        self.parameterWindow.bookmarksPage.showupdate()
    
    def addhistory(self):
        self.dbConnection.executewithoutreturn("""INSERT INTO history(name, url, date) VALUES(?, ?, ?)""", (
            self.browserWidget.title(), self.browserWidget.url().toString(),
            getdate()))
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R or event.key() == Qt.Key_F5:
            self.browserWidget.reload()
        elif event.key() == Qt.Key_N:
            self.tabWidget.requestsaddtab()
        elif event.key() == Qt.Key_Q:
            self.tabWidget.requestsremovetab(self.tabWidget.currentIndex())
    
    def closeEvent(self, event):
        if self.tabWidget.count() == 0 or (self.tabWidget.count() == 1 and self.tabWidget.closer):
            self.dbConnection.disconnect()
            self.tabWidget.closer = False
            event.accept()
        elif self.tabWidget.count() != 1:
            if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter les autres onglets ? \nDans tous les cas, l'onglet actuel sera fermé", QMessageBox.Yes,
                                      QMessageBox.No) == 16384:
                self.dbConnection.disconnect()
                event.accept()
            else:
                event.ignore()
                self.tabWidget.requestsremovetab(self.tabWidget.currentIndex())
        else:
            if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter Browthon ?", QMessageBox.Yes,
                                      QMessageBox.No) == 16384:
                self.dbConnection.disconnect()
                event.accept()
            else:
                event.ignore()
