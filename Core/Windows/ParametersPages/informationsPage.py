#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QSpacerItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from Core.Widgets.pushButton import PushButton


class InformationsPage(QWidget):
    def __init__(self, parent):
        super(InformationsPage, self).__init__()
        self.parent = parent

        self.bsite = PushButton("Site")
        self.bwiki = PushButton("Wiki")
        self.ltitre = QLabel("Browthon Reborn")
        d = "Browthon Reborn est créé par LavaPower avec Python et PyQt\n" \
            "Version : 0.1.0\n\nMerci à Feldrise pour son aide\n\n\nLiens utiles :"
        self.ldescription = QLabel(d)
        self.image = QPixmap("logo.png")

        self.bsite.clicked.connect(self.openwebsite)
        self.bwiki.clicked.connect(self.openwiki)
        self.ltitre.setAlignment(Qt.AlignHCenter)
        self.ldescription.setAlignment(Qt.AlignHCenter)
        self.grid = QGridLayout()
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.image)
        self.imageLabel.setAlignment(Qt.AlignHCenter)
        self.titreSpacerItem = QSpacerItem(20, 25)
        self.endSpacerItem = QSpacerItem(20, 500)

        self.grid.addWidget(self.imageLabel, 1, 1)
        self.grid.addWidget(self.ltitre, 2, 1)
        self.grid.addItem(self.titreSpacerItem, 3, 1)
        self.grid.addWidget(self.ldescription, 4, 1)
        self.grid.addWidget(self.bsite, 5, 1)
        self.grid.addWidget(self.bwiki, 6, 1)
        self.grid.addItem(self.endSpacerItem, 7, 1)
        self.setLayout(self.grid)

    def openwebsite(self):
        self.parent.close()
        self.parent.parent.opennewongletwithurl("http://lavapower.github.io")

    def openwiki(self):
        self.parent.close()
        self.parent.parent.opennewongletwithurl("https://github.com/Browthon/Browthon-Reborn/wiki")
