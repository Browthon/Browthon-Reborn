#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QPushButton

class MyPushButton(QPushButton):
    def __init__(self, texte, icon = ""):
        if icon == "":
            super(MyPushButton, self).__init__(texte)
        else:
            super(MyPushButton, self).__init__(icon, texte)