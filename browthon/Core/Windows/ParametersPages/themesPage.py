#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtWidgets import QWidget, QGridLayout, QLabel
from PySide2.QtCore import Qt

from browthon.Core.Widgets.listWidget import ListWidget
from browthon.Core.Widgets.pushButton import PushButton

import os
import json


class ThemesPage(QWidget):
    def __init__(self, parent):
        super(ThemesPage, self).__init__()
        self.parent = parent
        self.grid = QGridLayout()

        self.title = QLabel("Thèmes")
        self.title.setAlignment(Qt.AlignHCenter)
        self.liste = []
        for i in os.listdir(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes")):
            if "theme.json" in os.listdir(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes", i)):
                fichier = open(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes", i, "theme.json"),
                               "r")
                jsonfile = json.load(fichier)
                jsonfile["folder"] = i
                self.liste.append(jsonfile)
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
                    self.parent.parent.theme = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes",
                                                            i["folder"])
                    self.parent.parent.applytheme()
                    parameters = self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM parameters""")
                    self.parent.parent.dbConnection.executewithoutreturn(
                        """UPDATE parameters SET theme = ? WHERE id = ?""", (i["folder"], parameters[0][0]))
                    break

    def showupdate(self):
        self.listeW.deleteallitems()
        self.liste = []
        for i in os.listdir(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes")):
            if "theme.json" in os.listdir(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes", i)):
                fichier = open(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes", i, "theme.json"),
                               "r")
                jsonfile = json.load(fichier)
                jsonfile["folder"] = i
                self.liste.append(jsonfile)
                fichier.close()
            else:
                print("ERREUR : Le theme du dossier "+i+" n'a pas de json.")
        self.listeW.updatelist(self.liste)
        self.show()

    def delete(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i["folder"] == self.listeW.currentItem().text(3):
                    if self.parent.parent.theme == os.path.join(os.path.dirname(__file__),
                                                                "..", "..", "..", "Themes", i["folder"]):
                        self.parent.parent.theme = ""
                        self.parent.parent.applytheme()
                    contenu = os.listdir(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes",
                                                      i["folder"]))
                    for x in contenu:
                        os.remove(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes",
                                               i["folder"], x))
                    os.rmdir(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes", i["folder"]))
        self.showupdate()

    def deleteall(self):
        self.parent.parent.theme = ""
        self.parent.parent.applytheme()
        for i in self.liste:
            contenu = os.listdir(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes", i["folder"]))
            for x in contenu:
                os.remove(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes", i["folder"], x))
            os.rmdir(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Themes", i["folder"]))
        self.showupdate()
