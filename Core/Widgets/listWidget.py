#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class ListWidget(QTreeWidget):
    def __init__(self, liste):
        super(ListWidget, self).__init__()
        self.setColumnCount(4)
        self.setHeaderLabels(["Nom", "URL", "Date", "ID"])
        self.liste = liste
        self.listeItem = []
        for i in self.liste:
            item = QTreeWidgetItem(self, [i[1], i[2], i[3], str(i[0])])
            self.listeItem.append(item)
        self.insertTopLevelItems(0, self.listeItem)

    def deleteallitems(self):
        for i in range(len(self.listeItem) - 1, -1, -1):
            self.takeTopLevelItem(i)

    def updatelist(self, liste):
        self.liste = liste
        self.deleteallitems()
        self.listeItem = []
        for i in self.liste:
            item = QTreeWidgetItem(self, [i[1], i[2], i[3], str(i[0])])
            self.listeItem.append(item)
        self.insertTopLevelItems(0, self.listeItem)
