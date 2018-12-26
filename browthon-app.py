#!/usr/bin/python3.7
# coding: utf-8

import sys
import os

try:
    import PySide2
except Exception:
    input("Vous n'avez pas PySide2\nEssayez de faire 'pip install -r requirements.txt' dans le dossier de Browthon\n")
    sys.exit()
else:
    try:
        import PySide2.QtWebEngine
    except Exception:
        input("ERREUR : PySide2 ne comporte pas QtWebEngine.\nVérifiez si vous avez la version 64bits de Python.\n")
        sys.exit()
    else:
        from PySide2.QtWidgets import QApplication
        from PySide2.QtGui import QIcon

        from Core.browser import Browser


def launch(sys):
    os.putenv("QT_AUTO_SCREEN_SCALE_FACTOR", "1")

    app = QApplication(sys.argv)
    icon = QIcon('logo.png')
    app.setWindowIcon(icon)

    Browser()

    app.exec_()


if __name__ == '__main__':
    launch(sys)
