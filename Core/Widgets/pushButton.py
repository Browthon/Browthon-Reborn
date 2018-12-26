#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtWidgets import QPushButton


class PushButton(QPushButton):
    def __init__(self, texte, icon="", objectname=""):
        if icon == "":
            super(PushButton, self).__init__(texte)
        else:
            super(PushButton, self).__init__(icon, texte)
        if objectname != "":
            self.setObjectName(objectname)
