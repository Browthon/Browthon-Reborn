#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QPushButton

class PushButton(QPushButton):
    def __init__(self, texte, icon = ""):
        if icon == "":
            super(PushButton, self).__init__(texte)
        else:
            super(PushButton, self).__init__(icon, texte)