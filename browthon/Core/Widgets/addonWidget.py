#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtWidgets import QWidget, QGridLayout, QLabel, QMessageBox
from PySide2.QtGui import QPixmap

from browthon.Core.Widgets.pushButton import PushButton

import json
import os


class AddonWidget(QWidget):
    def __init__(self, main, manager, dossier):
        super(AddonWidget, self).__init__()
        self.main = main
        self.manager = manager
        self.datas = {}
        folders = os.path.dirname(__file__).split("\\")
        if len(folders) == 1:
            folders = os.path.dirname(__file__).split("/")
        folders = folders[:-2]
        folder = os.sep
        for i in folders:
            if i[-1] == ":":
                i += os.sep
            folder = os.path.join(folder, i)
        self.dossier = os.path.join(folder, "Addons", dossier)
        try:
            with open(os.path.join(self.dossier, "addon.json"), 'r') as f:
                self.datas = json.load(f)
        except:
            print("Le fichier addon.json (" + os.path.join(self.dossier, "addon.json") + ") n'a pas été trouvé")
            self.datas["Activation"] = "False"
            self.datas["NameCode"] = ""
        else:
            self.grid = QGridLayout()

            self.logo = QPixmap(self.dossier + "/" + self.datas["Logo"])
            self.imageLabel = QLabel()
            self.imageLabel.setPixmap(self.logo)
            self.title = QLabel(self.datas["Name"])
            self.author = QLabel("By : " + self.datas["Author"])
            self.description = QLabel(self.datas["Description"])
            self.bUrl = PushButton("Site")
            self.bUrl.clicked.connect(self.openurl)
            if self.datas["Activation"] == "True":
                self.bAct = PushButton("Désactiver")
                self.bAct.clicked.connect(self.desactivate)
            else:
                self.bAct = PushButton("Activer")
                self.bAct.clicked.connect(self.activate)

            self.grid.addWidget(self.imageLabel, 1, 1, 3, 1)
            self.grid.addWidget(self.title, 1, 2, 1, 1)
            self.grid.addWidget(self.author, 1, 3, 1, 1)
            self.grid.addWidget(self.description, 2, 2, 1, 2)
            self.grid.addWidget(self.bUrl, 3, 2, 1, 1)
            self.grid.addWidget(self.bAct, 3, 3, 1, 1)

            self.setLayout(self.grid)

    def openurl(self):
        self.main.parameterWindow.close()
        self.main.opennewongletwithurl(self.datas["Url"])

    def desactivate(self):
        self.datas["Activation"] = "False"
        with open(os.path.join(self.dossier, "addon.json"), 'w') as f:
            f.write(json.dumps(self.datas, indent=4))
        QMessageBox.warning(self, "Addon désactivé", "L'addon " + self.datas["NameCode"] + " a été désactivé")
        self.bAct.setText("Activer")
        self.bAct.clicked.disconnect()
        self.bAct.clicked.connect(self.activate)
        try:
            self.manager.addonsManager.LML[self.datas["NameCode"]].unload(
                self.manager.addonsManager.LML[self.datas["NameCode"]], self.main)
        except AttributeError:
            pass

    def activate(self):
        self.datas["Activation"] = "True"
        with open(os.path.join(self.dossier, "addon.json"), 'w') as f:
            f.write(json.dumps(self.datas, indent=4))
        QMessageBox.warning(self, "Addon activé", "L'addon " + self.datas["NameCode"] + " a été activé")
        self.bAct.setText("Désactiver")
        self.bAct.clicked.disconnect()
        self.bAct.clicked.connect(self.desactivate)
        try:
            self.manager.addonsManager.LML[self.datas["NameCode"]].load(
                self.manager.addonsManager.LML[self.datas["NameCode"]], self.main)
        except AttributeError:
            pass
