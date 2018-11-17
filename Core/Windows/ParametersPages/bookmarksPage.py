#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from Core.Widgets.listWidget import ListWidget
from Core.Widgets.pushButton import PushButton

class BookmarksPage(QWidget):
    def __init__(self, parent):
        super(BookmarksPage, self).__init__()
        self.parent = parent
        self.grid = QGridLayout()

        self.title = QLabel("Favoris")
        self.title.setAlignment(Qt.AlignHCenter)
        self.listeW = ListWidget(self.parent.parent.dbConnection.executeWithReturn("""SELECT * FROM bookmarks"""))
        self.supp = PushButton("Supprimer")
        self.suppAll = PushButton("Tout supprimer")
        self.addFav = PushButton("Ajouter la page aux Favoris")
        
        self.listeW.itemDoubleClicked.connect(self.launch)
        self.suppAll.clicked.connect(self.deleteAll)
        self.supp.clicked.connect(self.delete)
        self.addFav.clicked.connect(self.addFavF)

        self.grid.addWidget(self.title, 1, 1, 1, 2)
        self.grid.addWidget(self.listeW, 2, 1, 1, 2)
        self.grid.addWidget(self.supp, 3, 1)
        self.grid.addWidget(self.suppAll, 3, 2)
        self.grid.addWidget(self.addFav, 4, 1, 1, 2)

        self.setLayout(self.grid)

    def launch(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i[1] == self.listeW.currentItem().text():
                    self.close()
                    self.parent.parent.openNewOngletWithUrl(i[2])
                    break
    
    def addFavF(self):
        self.parent.parent.dbConnection.executeWithoutReturn("""INSERT INTO bookmarks(name, url) VALUES(?, ?)""", (self.parent.parent.browserWidget.title(), self.parent.parent.browserWidget.url().toString()))
        self.parent.parent.bookmark.setIcon(QIcon("Icons/NavigationBar/yesFav.png"))
        self.showUpdate()

    def showUpdate(self):
        self.listeW.deleteAllItems()
        self.liste = self.parent.parent.dbConnection.executeWithReturn("""SELECT * FROM bookmarks""")
        self.listeW.updateList(self.liste)

    def delete(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i[1] == self.listeW.currentItem().text():
                    self.parent.parent.dbConnection.executeWithoutReturn("""DELETE FROM bookmarks WHERE id = ?""", (i[0],))
                    if i[2] == self.parent.parent.browserWidget.url().toString():
                        self.parent.parent.bookmark.setIcon(QIcon("Icons/NavigationBar/noFav.png"))
        self.showUpdate()
    
    def deleteAll(self):
        self.parent.parent.dbConnection.executeWithoutReturn("""DELETE FROM bookmarks""")
        self.parent.parent.bookmark.setIcon(QIcon("Icons/NavigationBar/noFav.png"))
        self.showUpdate()