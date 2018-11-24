#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt

from Core.Widgets.listWidget import ListWidget
from Core.Widgets.pushButton import PushButton


class HistoryPage(QWidget):
    def __init__(self, parent):
        super(HistoryPage, self).__init__()
        self.parent = parent
        self.grid = QGridLayout()

        self.title = QLabel("Historique")
        self.title.setAlignment(Qt.AlignHCenter)
        self.liste = self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM history""")
        self.listeW = ListWidget(self.liste)
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
                if i[1] == self.listeW.currentItem().text():
                    self.close()
                    self.parent.parent.opennewongletwithurl(i[2])
                    break

    def showupdate(self):
        self.listeW.deleteallitems()
        self.liste = self.parent.parent.dbConnection.executewithreturn("""SELECT * FROM history""")
        self.listeW.updatelist(self.liste)
        self.show()

    def delete(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i[1] == self.listeW.currentItem().text():
                    self.parent.parent.dbConnection.executewithoutreturn(
                        """DELETE FROM history WHERE id = ?""", (i[0],))
        self.showupdate()
    
    def deleteall(self):
        self.parent.parent.dbConnection.executewithoutreturn("""DELETE FROM history""")
        self.showupdate()
