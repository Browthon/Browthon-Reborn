#!/usr/bin/python3.7
# coding: utf-8

from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QFileDialog, QMessageBox

from urllib.request import urlopen


class DownloadSignal(QObject):
    removeClicked = Signal()

    def __init__(self, parent):
        super(DownloadSignal, self).__init__()
        self.parent = parent


def downloadfile(main, url):
    path = QFileDialog.getSaveFileName(main, "Sauver comme")
    if not path[0]:
        return
    else:
        try:
            with open(path[0], 'wb') as file:
                file.write(urlopen(url).read())
        except Exception:
            QMessageBox.warning(main, "Téléchargement arrêté", "Votre fichier (" + path[0] + ") a eu une erreur...")
        else:
            QMessageBox.information(main, "Téléchargement complété",
                                    "Votre fichier ("+path[0]+") a bien été enregistré")
