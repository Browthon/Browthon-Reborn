#!/usr/bin/python3.7
# coding: utf-8

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from Core.browser import Browser


def launch(sys):
    app = QApplication(sys.argv)
    icon = QIcon('logo.png')
    app.setWindowIcon(icon)

    Browser()

    app.exec_()


if __name__ == '__main__':
    launch(sys)