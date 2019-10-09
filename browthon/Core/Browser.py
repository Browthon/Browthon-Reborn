#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtWidgets import QWidget, QMainWindow, QGridLayout, QMessageBox
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QIcon
from PySide2.QtWebEngineWidgets import QWebEngineSettings, QWebEngineProfile

from browthon.Core.Widgets.urlInput import UrlInput
from browthon.Core.Widgets.tabWidget import TabWidget
from browthon.Core.Widgets.pushButton import PushButton
from browthon.Core.Utils.dbUtils import majdb
from browthon.Core.Utils.urlUtils import getgoodurl
from browthon.Core.Utils.dateUtils import getdate
from browthon.Core.Utils.themeUtils import parsetheme, geticonpath
from browthon.Core.Windows.parameterWindow import ParameterWindow
from browthon.Core.Database import Database

import os
from urllib.request import urlopen


class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.db = Database(os.path.join(os.path.dirname(__file__), "data.db"))
        self.db.createdb()

        self.centralWidget = QWidget(self)
        self.grid = QGridLayout(self.centralWidget)
        self.theme = ""
        self.version = "1.0.0"
        self.versionCompaDB = 1
        self.versionAccDB = self.db.executewithreturn("""SELECT version FROM informations""")[0][0]
        if self.versionAccDB != self.versionCompaDB:
            QMessageBox.information(self, "Base de donnée non à jour", "La Base de donnée n'est pas compatible avec "
                                                                       "cette version de Browthon.\n"
                                                                       "Elle va être mise à jour.")
            self.dbConnection.disconnect()
            self.versionAccDB = majdb(os.path.join(os.path.dirname(__file__), "data.db"),
                                      self.versionAccDB, self.versionCompaDB)
            self.dbConnection.reconnect(os.path.join(os.path.dirname(__file__), "data.db"))
            self.dbConnection.createdb()
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        if self.db.executewithreturn("""SELECT js FROM parameters""")[0][0] == "Activé":
            QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        else:
            QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
        if self.db.executewithreturn("""SELECT private FROM parameters""")[0][0] == "Activé":
            self.privateBrowsing = True
            QWebEngineProfile.defaultProfile().setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
        else:
            self.privateBrowsing = False
            QWebEngineProfile.defaultProfile().setHttpCacheType(QWebEngineProfile.DiskHttpCache)

        self.urlInput = UrlInput(self)
        self.urlInput.setObjectName("addressBar")
        self.back = PushButton("", QIcon(geticonpath(self, "../Icons/NavigationBar/back.png")), "backButton")
        self.forward = PushButton("", QIcon(geticonpath(self, "../Icons/NavigationBar/forward.png")), "forwardButton")
        self.reload = PushButton("", QIcon(geticonpath(self, "../Icons/NavigationBar/reload.png")), "reloadButton")
        self.bookmark = PushButton("", QIcon(geticonpath(self, "../Icons/NavigationBar/noFav.png")), "favButton")
        self.home = PushButton("", QIcon(geticonpath(self, "../Icons/NavigationBar/home.png")), "homeButton")
        self.parameter = PushButton("", QIcon(geticonpath(self, "../Icons/NavigationBar/param.png")), "paramButton")
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
            self.db.executewithreturn("""SELECT home FROM parameters""")[0][0]))
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

        self.parameterWindow = ParameterWindow(self)
        QWebEngineProfile.defaultProfile().\
            downloadRequested.connect(self.parameterWindow.downloadPage.downloadrequested)

        theme = self.db.executewithreturn("""SELECT theme FROM parameters""")[0][0]
        if theme == "":
            self.theme = ""
            self.applytheme()
        else:
            if os.path.exists(os.path.join(os.path.dirname(__file__), "..", "Themes", theme, "theme.json")):
                self.theme = os.path.join(os.path.dirname(__file__), "..", "Themes", theme)
                self.applytheme()
            else:
                print("Le theme "+theme+" n'existe pas/plus.")
                self.theme = ""
                self.applytheme()

        self.parameterWindow.addonsPage.launchaddons("load")
        self.show()
        if self.db.executewithreturn("""SELECT first FROM parameters""")[0][0] == "O":
            parameters = self.dbConnection.executewithreturn("""SELECT * FROM parameters""")
            self.db.executewithoutreturn(
                """UPDATE parameters SET first = ? WHERE id = ?""", ("N", parameters[0][0]))
        # self.checkmaj()

    def settitle(self, widget):
        if self.privateBrowsing:
            self.setWindowTitle("[Privé] "+self.browserWidget.title() + " - Browthon")
        else:
            self.setWindowTitle(self.browserWidget.title() + " - Browthon")
        self.tabWidget.settitle(widget)

    def applytheme(self):
        if self.theme == "" or self.theme == os.path.join(os.path.dirname(__file__), "..", "Themes"):
            self.setStyleSheet("")
            self.parameterWindow.setStyleSheet("")
        else:
            with open(self.theme+"/main.bss", 'r') as fichier:
                bss = parsetheme(fichier.read(), self.theme)
                self.setStyleSheet(bss)
                self.parameterWindow.setStyleSheet(bss)
        self.back.setIcon(QIcon(geticonpath(self,
                                            os.path.join(os.path.dirname(__file__),
                                                         "../Icons/NavigationBar/back.png"))))
        self.forward.setIcon(QIcon(geticonpath(self,
                                               os.path.join(os.path.dirname(__file__),
                                                            "../Icons/NavigationBar/forward.png"))))
        self.reload.setIcon(QIcon(geticonpath(self,
                                              os.path.join(os.path.dirname(__file__),
                                                           "../Icons/NavigationBar/reload.png"))))
        self.bookmark.setIcon(QIcon(geticonpath(self,
                                                os.path.join(os.path.dirname(__file__),
                                                             "../Icons/NavigationBar/noFav.png"))))
        self.home.setIcon(QIcon(geticonpath(self,
                                            os.path.join(os.path.dirname(__file__),
                                                         "../Icons/NavigationBar/home.png"))))
        self.parameter.setIcon(QIcon(geticonpath(self, os.path.join(os.path.dirname(__file__),
                                                                    "../Icons/NavigationBar/param.png"))))
        self.tabWidget.addTabButton.setIcon(QIcon(geticonpath(self, os.path.join(os.path.dirname(__file__),
                                                                                 "../Icons/Tabs/tabs-add.png"))))
        self.parameterWindow.tabWidget.setTabIcon(0,
                                                  QIcon(geticonpath(self,
                                                                    os.path.join(os.path.dirname(__file__),
                                                                                 "../Icons/Parameters/General.png"))))
        self.parameterWindow.tabWidget.setTabIcon(1,
                                                  QIcon(geticonpath(self,
                                                                    os.path.join(os.path.dirname(__file__),
                                                                                 "../Icons/Parameters/History.png"))))
        self.parameterWindow.tabWidget.setTabIcon(2,
                                                  QIcon(geticonpath(self,
                                                                    os.path.join(os.path.dirname(__file__),
                                                                                 "../Icons/Parameters/Fav.png"))))
        raccourcisimg = "../Icons/Parameters/Raccourcis.png"
        self.parameterWindow.tabWidget.setTabIcon(3,
                                                  QIcon(geticonpath(self,
                                                                    os.path.join(os.path.dirname(__file__),
                                                                                 raccourcisimg))))
        self.parameterWindow.tabWidget.setTabIcon(4,
                                                  QIcon(geticonpath(self,
                                                                    os.path.join(os.path.dirname(__file__),
                                                                                 "../Icons/Parameters/Sessions.png"))))
        self.parameterWindow.tabWidget.setTabIcon(5,
                                                  QIcon(geticonpath(self,
                                                                    os.path.join(os.path.dirname(__file__),
                                                                                 "../Icons/Parameters/Download.png"))))
        self.parameterWindow.tabWidget.setTabIcon(6,
                                                  QIcon(geticonpath(self,
                                                                    os.path.join(os.path.dirname(__file__),
                                                                                 "../Icons/Parameters/Themes.png"))))
        addonimg = "../Icons/Parameters/Addons.png"
        self.parameterWindow.tabWidget.setTabIcon(7,
                                                  QIcon(geticonpath(self,
                                                                    os.path.join(os.path.dirname(__file__),
                                                                                 addonimg))))
        self.parameterWindow.tabWidget.setTabIcon(8,
                                                  QIcon(geticonpath(self,
                                                                    os.path.join(os.path.dirname(__file__),
                                                                                 "../Icons/Parameters/Info.png"))))

    def opennewongletwithurl(self, url, move=True):
        url, temp = getgoodurl(self.dbConnection, url)
        self.tabWidget.requestsaddtab(url, move)
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
        bookmarks = self.db.executewithreturn("""SELECT * FROM bookmarks""")
        find = False
        for i in bookmarks:
            if i[2] == self.browserWidget.url().toString():
                self.db.executewithoutreturn("""DELETE FROM bookmarks WHERE id = ?""", (i[0],))
                self.bookmark.setIcon(QIcon(geticonpath(self,
                                                        os.path.join(os.path.dirname(__file__),
                                                                     "../Icons/NavigationBar/noFav.png"))))
                find = True
        if not find:
            self.db.executewithoutreturn("""INSERT INTO bookmarks(name, url, date) VALUES(?, ?, ?)""", (
                self.browserWidget.title(), self.browserWidget.url().toString(),
                getdate()))
            self.bookmark.setIcon(QIcon(geticonpath(self,
                                                    os.path.join(os.path.dirname(__file__),
                                                                 "../Icons/NavigationBar/yesFav.png"))))
        self.parameterWindow.bookmarksPage.showupdate()
    
    def loadfinished(self, widget):
        self.addhistory(widget)
        self.checkbookmarkbutton()
        self.parameterWindow.bookmarksPage.showupdate()
        self.tabWidget.settitle(widget)

    def checkbookmarkbutton(self):
        bookmarks = self.db.executewithreturn("""SELECT * FROM bookmarks""")
        find = False
        for i in bookmarks:
            if i[2] == self.browserWidget.url().toString():
                self.bookmark.setIcon(QIcon(geticonpath(self,
                                                        os.path.join(os.path.dirname(__file__),
                                                                     "../Icons/NavigationBar/yesFav.png"))))
                find = True
        if not find:
            self.bookmark.setIcon(QIcon(geticonpath(self,
                                                    os.path.join(os.path.dirname(__file__),
                                                                 "../Icons/NavigationBar/noFav.png"))))
    
    def addhistory(self, widget):
        if not self.privateBrowsing:
            self.db.executewithoutreturn("""INSERT INTO history(name, url, date) VALUES(?, ?, ?)""", (
                widget.title(), widget.url().toString(),
                getdate()))
    
    def keyPressEvent(self, event):
        self.parameterWindow.addonsPage.launchaddons("keyPress", event)

    def checkmaj(self):
        page = urlopen('http://37.59.86.221/browthon/version.txt')
        strpage = page.read().decode("utf-8")
        newversion = strpage.split('.')
        version = self.version.split('.')
        if int(version[0]) < int(newversion[0]):
            QMessageBox.information(self, "Nouvelle MAJ", "Une nouvelle mise à jour est disponible : "+strpage+".\n"
                                                          "Vous pouvez l'avoir sur : https://github.com/Browthon/"
                                                          "Browthon-Reborn/releases")
        elif int(version[0]) == int(newversion[0]):
            if int(version[1]) < int(newversion[1]):
                QMessageBox.information(self, "Nouvelle MAJ", "Une nouvelle mise à jour est disponible.\n"
                                                              "Vous pouvez l'avoir sur : https://github.com/Browthon/"
                                                              "Browthon-Reborn/releases")
            elif int(version[1]) == int(newversion[1]):
                if int(version[2]) < int(newversion[2]):
                    QMessageBox.information(self, "Nouvelle MAJ", "Une nouvelle mise à jour est disponible.\n"
                                                                  "Vous pouvez l'avoir sur : https://github.com/Browthon/"
                                                                  "Browthon-Reborn/releases")

    def closeEvent(self, event):
        if self.tabWidget.count() == 0 or (self.tabWidget.count() == 1 and self.tabWidget.closer):
            self.dbConnection.disconnect()
            self.tabWidget.closer = False
            self.parameterWindow.addonsPage.launchaddons("unload")
            event.accept()
        elif self.tabWidget.count() != 1:
            if QMessageBox().question(self, "Quitter ?",
                                      "Voulez vous quitter les autres onglets ? \nDans tous les cas,"
                                      " l'onglet actuel sera fermé", QMessageBox.Yes,
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
                self.db.disconnect()
                self.parameterWindow.addonsPage.launchaddons("unload")
                event.accept()
            else:
                event.ignore()
