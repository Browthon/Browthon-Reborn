#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QMessageBox
from PySide2.QtCore import Qt

from browthon.Core.Widgets.addonWidget import AddonWidget
from browthon.Core.Utils.addonsUtils import AddonsManager


class AddonsPage(QWidget):
    def __init__(self, parent):
        super(AddonsPage, self).__init__()
        self.setMinimumSize(700, 500)
        self.main = parent.parent
        self.addonsManager = AddonsManager(self.main)
        self.addonsManager.loadaddons()
        self.widgets = []
        self.layoutMain = QVBoxLayout(self)
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.title = QLabel("Addons")
        self.title.setAlignment(Qt.AlignHCenter)
        self.layoutMain.addWidget(self.title)
        self.layoutMain.addWidget(self.scroll)

        self.container = QWidget()
        self.scroll.setWidget(self.container)
        self.layout = QVBoxLayout(self.container)
        self.label = QLabel("Pas de addons")
        self.label.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.label)
        for i in self.addonsManager.imported:
            self.addonW = AddonWidget(self.main, self, i.replace(".", "/").split("/")[-2])
            self.widgets.append(self.addonW)
            self.layout.addWidget(self.addonW)
            self.layout.setAlignment(self.addonW, Qt.AlignTop)
            self.label.hide()

    def launchaddons(self, function, args=None):
        self.addonsManager.launchaddons(self.widgets, function, args)


