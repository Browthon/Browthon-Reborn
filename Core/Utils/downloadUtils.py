#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtCore import QObject, pyqtSignal


class DownloadSignal(QObject):
    removeClicked = pyqtSignal()

    def __init__(self, parent):
        super(DownloadSignal, self).__init__()
        self.parent = parent
