#!/usr/bin/python3.7
# coding: utf-8

import sys
import os

try:
    import PyQt5
except Exception:
    input("Vous n'avez pas PyQt5\nEssayez de faire 'pip install -r requirements.txt' dans le dossier de Browthon\n")
    sys.exit()
else:
    try:
        import PyQt5.QtWebEngine
    except Exception:
        input("ERREUR : PyQt ne comporte pas QtWebEngine.\nVérifiez si vous avez la version 64bits de Python.\n")
        sys.exit()
    else:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QIcon

        from browthon.Core.browser import Browser


def launch():
    os.putenv("QT_AUTO_SCREEN_SCALE_FACTOR", "1")

    app = QApplication(sys.argv)
    icon = QIcon('logo.png')
    app.setWindowIcon(icon)

    Browser()

    app.exec_()


if __name__ == '__main__':
    launch()
