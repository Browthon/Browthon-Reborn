#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QListWidget


class ListWidget(QListWidget):
    def __init__(self, liste, typeData = ""):
        super(ListWidget, self).__init__()
        self.liste = liste
        self.typeData = typeData
        for i in self.liste:
            if self.typeData == "Raccourcis" or self.typeData == "Sessions":
                self.addItem(i[1] + " - " + i[2])
            else:
                self.addItem(i[1])

    def deleteallitems(self):
        for i in range(self.count() - 1, -1, -1):
            self.takeItem(i)

    def updatelist(self, liste):
        self.liste = liste
        self.deleteallitems()
        for i in self.liste:
            if self.typeData == "Raccourcis" or self.typeData == "Sessions":
                self.addItem(i[1] + " - " + i[2])
            else:
                self.addItem(i[1])
