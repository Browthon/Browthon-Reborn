#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpacerItem, QMessageBox, QComboBox
from PyQt5.QtCore import Qt

from Core.Widgets.pushButton import PushButton


class GeneralPage(QWidget):
    def __init__(self, parent):
        super(GeneralPage, self).__init__()
        self.parent = parent
        self.grid = QVBoxLayout()

        self.listeMoteur = ["Google", "Duckduckgo", "Ecosia", "Yahoo", "Bing"]
        moteurAcc = self.parent.parent.dbConnection.executewithreturn("""SELECT moteur FROM parameters""")[0][0]
        for i in range(len(self.listeMoteur)):
            if self.listeMoteur[i] == moteurAcc:
                self.listeMoteur[i], self.listeMoteur[0] = self.listeMoteur[0], self.listeMoteur[i]

        self.lAccueil = QLabel("Page d'accueil")
        self.lAccueil.setAlignment(Qt.AlignHCenter)
        self.urlAccueil = QLineEdit(
            self.parent.parent.dbConnection.executewithreturn("""SELECT home FROM parameters""")[0][0])
        self.urlAccueil.setAlignment(Qt.AlignHCenter)
        self.lMoteur = QLabel("Moteur de recherche")
        self.lMoteur.setAlignment(Qt.AlignHCenter)
        self.moteurBox = QComboBox()
        self.moteurBox.addItems(self.listeMoteur)

        self.endSpacerItem = QSpacerItem(20,600)
        self.bValid = PushButton("Valider")

        self.bValid.clicked.connect(self.valider)

        self.grid.addWidget(self.lAccueil)
        self.grid.addWidget(self.urlAccueil)
        self.grid.addWidget(self.lMoteur)
        self.grid.addWidget(self.moteurBox)
        self.grid.addItem(self.endSpacerItem)
        self.grid.addWidget(self.bValid)
        self.setLayout(self.grid)
    
    def valider(self):
        parameters = self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM parameters""")
        self.parent.parent.dbConnection.executewithoutreturn(
            """UPDATE parameters SET home = ? WHERE id = ?""", (self.urlAccueil.text(),parameters[0][0]))
        self.parent.parent.dbConnection.executewithoutreturn(
            """UPDATE parameters SET moteur = ? WHERE id = ?""",
            (self.listeMoteur[self.moteurBox.currentIndex()],
             parameters[0][0]))
        QMessageBox().about(self, "Enregistrement fait", "L'enregistrement des paramètres a été fait sans problème")
