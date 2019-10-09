#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpacerItem, QMessageBox, QComboBox
from PySide2.QtCore import Qt
from PySide2.QtWebEngineWidgets import QWebEngineSettings, QWebEngineProfile

from browthon.Core.Widgets.pushButton import PushButton


class GeneralPage(QWidget):
    def __init__(self, parent):
        super(GeneralPage, self).__init__()
        self.parent = parent
        self.grid = QVBoxLayout()

        self.listeMoteur = ["Google", "Duckduckgo", "Ecosia", "Yahoo", "Bing"]
        moteuracc = self.parent.parent.dbConnection.executewithreturn("""SELECT moteur FROM parameters""")[0][0]
        for i in range(len(self.listeMoteur)):
            if self.listeMoteur[i] == moteuracc:
                self.listeMoteur[i], self.listeMoteur[0] = self.listeMoteur[0], self.listeMoteur[i]
        jsacc = self.parent.parent.dbConnection.executewithreturn("""SELECT js FROM parameters""")[0][0]
        if jsacc == "Activé":
            self.listejs = ["Activé", "Désactivé"]
        else:
            self.listejs = ["Désactivé", "Activé"]
        privateacc = self.parent.parent.dbConnection.executewithreturn("""SELECT private FROM parameters""")[0][0]
        if privateacc == "Activé":
            self.listeprivate = ["Activé", "Désactivé"]
        else:
            self.listeprivate = ["Désactivé", "Activé"]

        self.lAccueil = QLabel("Page d'accueil")
        self.lAccueil.setAlignment(Qt.AlignHCenter)
        self.urlAccueil = QLineEdit(
            self.parent.parent.dbConnection.executewithreturn("""SELECT home FROM parameters""")[0][0])
        self.urlAccueil.setAlignment(Qt.AlignHCenter)
        self.lMoteur = QLabel("Moteur de recherche")
        self.lMoteur.setAlignment(Qt.AlignHCenter)
        self.moteurBox = QComboBox()
        self.moteurBox.addItems(self.listeMoteur)
        self.lJS = QLabel("Javascript")
        self.lJS.setAlignment(Qt.AlignHCenter)
        self.jsbox = QComboBox()
        self.jsbox.addItems(self.listejs)
        self.lPrivate = QLabel("Navigation Privée")
        self.lPrivate.setAlignment(Qt.AlignHCenter)
        self.privatebox = QComboBox()
        self.privatebox.addItems(self.listeprivate)

        self.endSpacerItem = QSpacerItem(20, 600)
        self.paramSpacerItem = QSpacerItem(20, 25)
        self.bValid = PushButton("Valider")

        self.bValid.clicked.connect(self.valider)

        self.grid.addWidget(self.lAccueil)
        self.grid.addWidget(self.urlAccueil)
        self.grid.addItem(self.paramSpacerItem)
        self.grid.addWidget(self.lMoteur)
        self.grid.addWidget(self.moteurBox)
        self.grid.addItem(self.paramSpacerItem)
        self.grid.addWidget(self.lJS)
        self.grid.addWidget(self.jsbox)
        self.grid.addItem(self.paramSpacerItem)
        self.grid.addWidget(self.lPrivate)
        self.grid.addWidget(self.privatebox)
        self.grid.addItem(self.endSpacerItem)
        self.grid.addWidget(self.bValid)
        self.setLayout(self.grid)
    
    def valider(self):
        parameters = self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM parameters""")
        self.parent.parent.dbConnection.executewithoutreturn(
            """UPDATE parameters SET home = ? WHERE id = ?""", (self.urlAccueil.text(), parameters[0][0]))
        self.parent.parent.dbConnection.executewithoutreturn(
            """UPDATE parameters SET moteur = ? WHERE id = ?""",
            (self.listeMoteur[self.moteurBox.currentIndex()],
             parameters[0][0]))
        self.parent.parent.dbConnection.executewithoutreturn(
            """UPDATE parameters SET js = ? WHERE id = ?""",
            (self.listejs[self.jsbox.currentIndex()],
             parameters[0][0]))
        if self.listejs[self.jsbox.currentIndex()] == "Activé":
            QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        else:
            QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
        self.parent.parent.dbConnection.executewithoutreturn(
            """UPDATE parameters SET private = ? WHERE id = ?""",
            (self.listeprivate[self.privatebox.currentIndex()],
             parameters[0][0]))
        if self.listeprivate[self.privatebox.currentIndex()] == "Activé":
            QWebEngineProfile.defaultProfile().setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
            self.parent.parent.privateBrowsing = True
        else:
            QWebEngineProfile.defaultProfile().setHttpCacheType(QWebEngineProfile.DiskHttpCache)
            self.parent.parent.privateBrowsing = False
        QMessageBox().about(self, "Enregistrement fait", "L'enregistrement des paramètres a été fait sans problème")
