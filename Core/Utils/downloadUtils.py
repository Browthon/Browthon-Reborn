#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtCore import QObject, Signal


class DownloadSignal(QObject):
    removeClicked = Signal()

    def __init__(self, parent):
        super(DownloadSignal, self).__init__()
        self.parent = parent
