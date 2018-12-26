#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtWidgets import QWidget, QMainWindow, QGridLayout, QMessageBox
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QIcon
from PySide2.QtWebEngineWidgets import QWebEngineSettings, QWebEngineProfile

from Core.Widgets.urlInput import UrlInput
from Core.Widgets.tabWidget import TabWidget
from Core.Widgets.pushButton import PushButton
from Core.Utils.dbUtils import DBConnection
from Core.Utils.urlUtils import getgoodurl
from Core.Utils.dateUtils import getdate
from Core.Utils.themeUtils import parsetheme, geticonpath
from Core.Windows.parameterWindow import ParameterWindow

import os


class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.dbConnection = DBConnection("data.db")
        self.dbConnection.createdb()

        self.centralWidget = QWidget(self)
        self.grid = QGridLayout(self.centralWidget)
        self.theme = ""
        self.version = "0.1.0"

        self.urlInput = UrlInput(self)
        self.urlInput.setObjectName("addressBar")
        self.back = PushButton("", QIcon(geticonpath(self, "Icons/NavigationBar/back.png")), "backButton")
        self.forward = PushButton("", QIcon(geticonpath(self, "Icons/NavigationBar/forward.png")), "forwardButton")
        self.reload = PushButton("", QIcon(geticonpath(self, "Icons/NavigationBar/reload.png")), "reloadButton")
        self.bookmark = PushButton("", QIcon(geticonpath(self, "Icons/NavigationBar/noFav.png")), "favButton")
        self.home = PushButton("", QIcon(geticonpath(self, "Icons/NavigationBar/home.png")), "homeButton")
        self.parameter = PushButton("", QIcon(geticonpath(self, "Icons/NavigationBar/param.png")), "paramButton")
        self.tabWidget = TabWidget(self)
        self.tabWidget.tabBar().setObjectName("tabBar")

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
            self.theme = ""
            self.applytheme()
        else:
            if os.path.exists("Themes/"+theme+"/theme.json"):
                self.theme = "Themes/"+theme
                self.applytheme()
            else:
                print("Le theme "+theme+" n'existe pas/plus.")
                self.theme = ""
                self.applytheme()

        self.parameterWindow.addonsPage.launchaddons("load")
        self.show()
        if self.dbConnection.executewithreturn("""SELECT first FROM parameters""")[0][0] == "O":
            parameters = self.dbConnection.executewithreturn("""SELECT * FROM parameters""")
            self.dbConnection.executewithoutreturn(
                """UPDATE parameters SET first = ? WHERE id = ?""", ("N", parameters[0][0]))

    def settitle(self):
        self.setWindowTitle(self.browserWidget.title() + " - Browthon")
        self.tabWidget.settitle()

    def applytheme(self):
        if self.theme == "" or self.theme == "Themes/":
            self.setStyleSheet("")
            self.parameterWindow.setStyleSheet("")
        else:
            with open(self.theme+"/main.bss", 'r') as fichier:
                bss = parsetheme(fichier.read(), self.theme)
                self.setStyleSheet(bss)
                self.parameterWindow.setStyleSheet(bss)
        self.back.setIcon(QIcon(geticonpath(self, "Icons/NavigationBar/back.png")))
        self.forward.setIcon(QIcon(geticonpath(self, "Icons/NavigationBar/forward.png")))
        self.reload.setIcon(QIcon(geticonpath(self, "Icons/NavigationBar/reload.png")))
        self.bookmark.setIcon(QIcon(geticonpath(self, "Icons/NavigationBar/noFav.png")))
        self.home.setIcon(QIcon(geticonpath(self, "Icons/NavigationBar/home.png")))
        self.parameter.setIcon(QIcon(geticonpath(self, "Icons/NavigationBar/param.png")))
        self.tabWidget.addTabButton.setIcon(QIcon(geticonpath(self, "Icons/Tabs/tabs-add.png")))
        self.parameterWindow.tabWidget.setTabIcon(0, QIcon(geticonpath(self, "Icons/Parameters/General.png")))
        self.parameterWindow.tabWidget.setTabIcon(1, QIcon(geticonpath(self, "Icons/Parameters/History.png")))
        self.parameterWindow.tabWidget.setTabIcon(2, QIcon(geticonpath(self, "Icons/Parameters/Fav.png")))
        self.parameterWindow.tabWidget.setTabIcon(3, QIcon(geticonpath(self, "Icons/Parameters/Raccourcis.png")))
        self.parameterWindow.tabWidget.setTabIcon(4, QIcon(geticonpath(self, "Icons/Parameters/Sessions.png")))
        self.parameterWindow.tabWidget.setTabIcon(5, QIcon(geticonpath(self, "Icons/Parameters/Download.png")))
        self.parameterWindow.tabWidget.setTabIcon(6, QIcon(geticonpath(self, "Icons/Parameters/Themes.png")))
        self.parameterWindow.tabWidget.setTabIcon(7, QIcon(geticonpath(self, "Icons/Parameters/Addons.png")))
        self.parameterWindow.tabWidget.setTabIcon(8, QIcon(geticonpath(self, "Icons/Parameters/Info.png")))

    def opennewongletwithurl(self, url):
        url, temp = getgoodurl(self.dbConnection, url)
        self.tabWidget.requestsaddtab()
        self.browserWidget.load(QUrl(url))
        self.parameterWindow.addonsPage.launchaddons("openOnglet", url)

    def opennewongletwithurllist(self, urllist):
        for i in urllist:
            if i != urllist[0]:
                self.tabWidget.requestsaddtab()
                self.browserWidget.load(QUrl(i))
            else:
                self.browserWidget.load(QUrl(i))
            self.parameterWindow.addonsPage.launchaddons("openOnglet", i)

    def openparameter(self):
        self.parameterWindow.setWindowModality(Qt.ApplicationModal)
        self.parameterWindow.show()
    
    def fav(self):
        bookmarks = self.dbConnection.executewithreturn("""SELECT * FROM bookmarks""")
        find = False
        for i in bookmarks:
            if i[2] == self.browserWidget.url().toString():
                self.dbConnection.executewithoutreturn("""DELETE FROM bookmarks WHERE id = ?""", (i[0],))
                self.bookmark.setIcon(QIcon(geticonpath(self, "Icons/NavigationBar/noFav.png")))
                find = True
        if not find:
            self.dbConnection.executewithoutreturn("""INSERT INTO bookmarks(name, url, date) VALUES(?, ?, ?)""", (
                self.browserWidget.title(), self.browserWidget.url().toString(),
                getdate()))
            self.bookmark.setIcon(QIcon(geticonpath(self, "Icons/NavigationBar/yesFav.png")))
        self.parameterWindow.bookmarksPage.showupdate()
    
    def loadfinished(self):
        self.addhistory()
        bookmarks = self.dbConnection.executewithreturn("""SELECT * FROM bookmarks""")
        find = False
        for i in bookmarks:
            if i[2] == self.browserWidget.url().toString():
                self.bookmark.setIcon(QIcon(geticonpath(self, "Icons/NavigationBar/yesFav.png")))
                find = True
        if not find:
            self.bookmark.setIcon(QIcon(geticonpath(self, "Icons/NavigationBar/noFav.png")))
        self.parameterWindow.bookmarksPage.showupdate()
    
    def addhistory(self):
        self.dbConnection.executewithoutreturn("""INSERT INTO history(name, url, date) VALUES(?, ?, ?)""", (
            self.browserWidget.title(), self.browserWidget.url().toString(),
            getdate()))
    
    def keyPressEvent(self, event):
        self.parameterWindow.addonsPage.launchaddons("keyPress", event)
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
            self.parameterWindow.addonsPage.launchaddons("unload")
            event.accept()
        elif self.tabWidget.count() != 1:
            if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter les autres onglets ? \nDans tous les cas, l'onglet actuel sera fermé", QMessageBox.Yes,
                                      QMessageBox.No) == 16384:
                self.dbConnection.disconnect()
                self.parameterWindow.addonsPage.launchaddons("unload")
                event.accept()
            else:
                event.ignore()
                self.tabWidget.requestsremovetab(self.tabWidget.currentIndex())
        else:
            if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter Browthon ?", QMessageBox.Yes,
                                      QMessageBox.No) == 16384:
                self.dbConnection.disconnect()
                self.parameterWindow.addonsPage.launchaddons("unload")
                event.accept()
            else:
                event.ignore()
