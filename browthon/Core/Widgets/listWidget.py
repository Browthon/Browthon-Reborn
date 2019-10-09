#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem


class ListWidget(QTreeWidget):
    def __init__(self, liste, typedata="Default"):
        super(ListWidget, self).__init__()
        self.setColumnCount(4)
        self.typedata = typedata
        if self.typedata == "Themes":
            self.setHeaderLabels(["Nom", "Auteur", "Description", "Dossier"])
        else:
            self.setHeaderLabels(["Nom", "URL", "Date", "ID"])
        self.liste = liste
        self.listeItem = []
        for i in self.liste:
            if self.typedata == "Themes":
                item = QTreeWidgetItem(self, [i["name"], i["author"], i["description"], i["folder"]])
            else:
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
            if self.typedata == "Themes":
                item = QTreeWidgetItem(self, [i["name"], i["author"], i["description"], i["folder"]])
            else:
                item = QTreeWidgetItem(self, [i[1], i[2], i[3], str(i[0])])
            self.listeItem.append(item)
        self.insertTopLevelItems(0, self.listeItem)
