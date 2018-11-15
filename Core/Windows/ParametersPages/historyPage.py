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
        self.listeW = ListWidget(self.parent.parent.dbConnection.executeWithReturn("""SELECT * FROM history"""))
        self.supp = PushButton("Supprimer")
        self.suppAll = PushButton("Tout supprimer")
        
        self.listeW.itemDoubleClicked.connect(self.launch)
        self.suppAll.clicked.connect(self.deleteAll)
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
                    self.parent.parent.openNewOngletWithUrl(i[2])
                    break

    def showUpdate(self):
        self.listeW.deleteAllItems()
        self.liste = self.parent.parent.dbConnection.executeWithReturn("""SELECT * FROM history""")
        self.listeW.updateList(self.liste)
        self.show()

    def delete(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i[1] == self.listeW.currentItem().text():
                    self.parent.parent.dbConnection.executeWithoutReturn("""DELETE FROM history WHERE id = ?""", (i[0],))
        self.showUpdate()
    
    def deleteAll(self):
        self.parent.parent.dbConnection.executeWithoutReturn("""DELETE FROM history""")
        self.showUpdate()