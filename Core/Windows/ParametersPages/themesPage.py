#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt

from Core.Widgets.listWidget import ListWidget
from Core.Widgets.pushButton import PushButton

import os
import json


class ThemesPage(QWidget):
    def __init__(self, parent):
        super(ThemesPage, self).__init__()
        self.parent = parent
        self.grid = QGridLayout()

        self.title = QLabel("Thèmes")
        self.title.setAlignment(Qt.AlignHCenter)
        self.liste = [{"name": "Default",
                       "author": "LavaPower",
                       "description": "Theme par defaut",
                       "folder": ""}]
        for i in os.listdir("Themes"):
            if "theme.json" in os.listdir("Themes/"+i):
                fichier = open("Themes/"+i+"/theme.json", "r")
                self.liste.append(json.load(fichier))
            else:
                print("ERREUR : Le theme du dossier "+i+" n'a pas de json.")
        self.listeW = ListWidget(self.liste, "Themes")
        self.supp = PushButton("Supprimer")
        self.suppAll = PushButton("Tout supprimer")

        self.listeW.itemDoubleClicked.connect(self.launch)
        self.suppAll.clicked.connect(self.deleteall)
        self.supp.clicked.connect(self.delete)

        self.grid.addWidget(self.title, 1, 1, 1, 2)
        self.grid.addWidget(self.listeW, 2, 1, 1, 2)
        self.grid.addWidget(self.supp, 3, 1)
        self.grid.addWidget(self.suppAll, 3, 2)

        self.setLayout(self.grid)

    def launch(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i["folder"] == self.listeW.currentItem().text(3):
                    self.parent.close()
                    self.parent.parent.applytheme("Themes/"+i["folder"])
                    parameters = self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM parameters""")
                    self.parent.parent.dbConnection.executewithoutreturn(
                        """UPDATE parameters SET theme = ? WHERE id = ?""", (i["folder"], parameters[0][0]))
                    break

    def showupdate(self):
        self.listeW.deleteallitems()
        self.liste = []
        for i in os.listdir("Themes"):
            if "theme.json" in os.listdir("Themes/"+i):
                fichier = open("Themes/"+i+"/theme.json", "r")
                self.liste.append(json.load(fichier))
                fichier.close()
            else:
                print("ERREUR : Le theme du dossier "+i+" n'a pas de json.")
        self.listeW.updatelist(self.liste)
        self.show()

    def delete(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i["folder"] == self.listeW.currentItem().text(3):
                    contenu = os.listdir("Themes/"+i["folder"])
                    for x in contenu:
                        os.remove("Themes/"+i["folder"]+"/"+x)
                    os.rmdir("Themes/"+i["folder"])
        self.showupdate()

    def deleteall(self):
        for i in self.liste:
            contenu = os.listdir("Themes/" + i["folder"])
            for x in contenu:
                os.remove("Themes/"+i["folder"]+"/"+x)
            os.rmdir("Themes/" + i["folder"])
        self.showupdate()
