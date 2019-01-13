#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSpacerItem, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

from browthon.Core.Widgets.listWidget import ListWidget
from browthon.Core.Widgets.pushButton import PushButton
from browthon.Core.Utils.dateUtils import getdate


class SessionsPage(QWidget):
    def __init__(self, parent):
        super(SessionsPage, self).__init__()
        self.parent = parent
        self.grid = QGridLayout()

        self.title = QLabel("Sessions")
        self.title.setAlignment(Qt.AlignHCenter)
        self.listeW = ListWidget(self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM sessions"""))
        self.liste = self.listeW.liste
        self.supp = PushButton("Supprimer")
        self.suppAll = PushButton("Tout supprimer")
        self.spacerItem = QSpacerItem(20, 20)
        self.tEntryString = "Nom de la session"
        self.tEntry = QLineEdit(self.tEntryString)
        self.addSession = PushButton("Ajouter une session")

        self.listeW.itemDoubleClicked.connect(self.launch)
        self.suppAll.clicked.connect(self.deleteall)
        self.supp.clicked.connect(self.delete)
        self.addSession.clicked.connect(self.addsession)

        self.grid.addWidget(self.title, 1, 1, 1, 2)
        self.grid.addWidget(self.listeW, 2, 1, 1, 2)
        self.grid.addWidget(self.supp, 3, 1)
        self.grid.addWidget(self.suppAll, 3, 2)
        self.grid.addItem(self.spacerItem, 4, 1, 1, 2)
        self.grid.addWidget(self.tEntry, 5, 1, 1, 2)
        self.grid.addWidget(self.addSession, 6, 1, 1, 2)

        self.setLayout(self.grid)

    def launch(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if str(i[0]) == self.listeW.currentItem().text(3):
                    self.parent.close()
                    for z in i[2].split(" | "):
                        self.parent.parent.opennewongletwithurl(z)
                    break

    def addsession(self):
        sessions = self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM sessions""")
        for i in sessions:
            if i[1] == self.tEntry.text():
                QMessageBox.warning(self, "Erreur", "Cette session existe déjà.")
                return

        tentrybool = self.tEntry.text() != "" and self.tEntry.text() != self.tEntryString
        if tentrybool:
            urls = ""
            for i in range(self.parent.parent.tabWidget.count()):
                urls += self.parent.parent.tabWidget.widget(i).url().toString() + " | "
            self.parent.parent.dbConnection.executewithoutreturn(
                """INSERT INTO sessions(name, urls, date) VALUES(?, ?, ?)""",
                (self.tEntry.text(), urls[:-3], getdate())
            )
            self.showupdate()

    def showupdate(self):
        self.listeW.deleteallitems()
        self.liste = self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM sessions""")
        self.listeW.updatelist(self.liste)

    def delete(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if str(i[0]) == self.listeW.currentItem().text(3):
                    self.parent.parent.dbConnection.executewithoutreturn(
                        """DELETE FROM sessions WHERE id = ?""", (i[0],))
        self.showupdate()

    def deleteall(self):
        self.parent.parent.dbConnection.executewithoutreturn("""DELETE FROM sessions""")
        self.showupdate()
