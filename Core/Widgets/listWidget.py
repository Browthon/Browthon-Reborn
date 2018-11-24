#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QListWidget


class ListWidget(QListWidget):
    def __init__(self, liste):
        super(ListWidget, self).__init__()
        self.liste = liste
        for i in self.liste:
            self.addItem(i[1])

    def deleteallitems(self):
        for i in range(self.count() - 1, -1, -1):
            self.takeItem(i)

    def updatelist(self, liste):
        self.liste = liste
        self.deleteallitems()
        for i in self.liste:
            self.addItem(i[1])
