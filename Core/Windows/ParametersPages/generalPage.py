#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpacerItem, QMessageBox
from PyQt5.QtCore import Qt

from Core.Widgets.pushButton import PushButton

class GeneralPage(QWidget):
    def __init__(self, parent):
        super(GeneralPage, self).__init__()
        self.parent = parent
        self.grid = QVBoxLayout()
        self.lAccueil = QLabel("Page d'accueil")
        self.lAccueil.setAlignment(Qt.AlignHCenter)
        self.urlAccueil = QLineEdit(self.parent.parent.dbConnection.executeWithReturn("""SELECT home FROM parameters""")[0][0])
        self.urlAccueil.setAlignment(Qt.AlignHCenter)
        self.spacerItem = QSpacerItem(20,700)
        self.bValid = PushButton("Valider")

        self.bValid.clicked.connect(self.valider)

        self.grid.addWidget(self.lAccueil)
        self.grid.addWidget(self.urlAccueil)
        self.grid.addItem(self.spacerItem)
        self.grid.addWidget(self.bValid)
        self.setLayout(self.grid)
    
    def valider(self):
        parameters = self.parent.parent.dbConnection.executeWithReturn("""SELECT * FROM parameters""")
        self.parent.parent.dbConnection.executeWithoutReturn("""UPDATE parameters SET home = ? WHERE id = ?""", (self.urlAccueil.text(),parameters[0][0]))
        QMessageBox().about(self, "Enregistrement fait", "L'enregistrement des paramètres a été fait sans problème")        