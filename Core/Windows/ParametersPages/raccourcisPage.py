#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSpacerItem, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

from Core.Widgets.listWidget import ListWidget
from Core.Widgets.pushButton import PushButton


class RaccourcisPage(QWidget):
    def __init__(self, parent):
        super(RaccourcisPage, self).__init__()
        self.parent = parent
        self.grid = QGridLayout()

        self.title = QLabel("Raccourcis URL")
        self.title.setAlignment(Qt.AlignHCenter)
        self.listeW = ListWidget(self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM raccourcis"""),
                                 "Raccourcis")
        self.liste = self.listeW.liste
        self.supp = PushButton("Supprimer")
        self.suppAll = PushButton("Tout supprimer")
        self.spacerItem = QSpacerItem(20,20)
        self.tEntryString = "Nom du raccourci"
        self.uEntryString = "URL du raccourci"
        self.tEntry = QLineEdit(self.tEntryString)
        self.uEntry = QLineEdit(self.uEntryString)
        self.addRac = PushButton("Ajouter un raccourci URL")

        self.listeW.itemDoubleClicked.connect(self.launch)
        self.suppAll.clicked.connect(self.deleteall)
        self.supp.clicked.connect(self.delete)
        self.addRac.clicked.connect(self.addraccourci)

        self.grid.addWidget(self.title, 1, 1, 1, 2)
        self.grid.addWidget(self.listeW, 2, 1, 1, 2)
        self.grid.addWidget(self.supp, 3, 1)
        self.grid.addWidget(self.suppAll, 3, 2)
        self.grid.addItem(self.spacerItem, 4, 1, 1, 2)
        self.grid.addWidget(self.tEntry, 5, 1)
        self.grid.addWidget(self.uEntry, 5, 2)
        self.grid.addWidget(self.addRac, 6, 1, 1, 2)

        self.setLayout(self.grid)

    def launch(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i[1] == self.listeW.currentItem().text().split(" - ")[0]:
                    self.parent.close()
                    self.parent.parent.opennewongletwithurl(i[2])
                    break

    def addraccourci(self):
        raccourcis = self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM raccourcis""")
        for i in raccourcis:
            if i[1] == self.tEntry.text():
                QMessageBox.warning(self, "Erreur", "Ce raccourcis existe déjà.")
                return

        tentrybool = self.tEntry.text() != "" and self.tEntry.text() != self.tEntryString
        uentrybool = self.uEntry.text() != "" and self.uEntry.text() != self.uEntryString
        if tentrybool and uentrybool:
            self.parent.parent.dbConnection.executewithoutreturn(
                """INSERT INTO raccourcis(name, url) VALUES(?, ?)""",
                (self.tEntry.text(), self.uEntry.text())
            )
            self.showupdate()

    def showupdate(self):
        self.listeW.deleteallitems()
        self.liste = self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM raccourcis""")
        self.listeW.updatelist(self.liste)

    def delete(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i[1] == self.listeW.currentItem().text().split(" - ")[0]:
                    self.parent.parent.dbConnection.executewithoutreturn(
                        """DELETE FROM raccourcis WHERE id = ?""", (i[0],))
        self.showupdate()

    def deleteall(self):
        self.parent.parent.dbConnection.executewithoutreturn("""DELETE FROM raccourcis""")
        self.showupdate()
