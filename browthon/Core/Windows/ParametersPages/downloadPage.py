#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QFileDialog, QVBoxLayout, QLabel, QScrollArea, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem
from PyQt5.QtCore import Qt

from browthon.Core.Widgets.downloadWidget import DownloadWidget


class DownloadPage(QWidget):
    def __init__(self, parent):
        super(DownloadPage, self).__init__()
        self.setMinimumSize(500, 300)
        self.parent = parent
        self.nbDownload = 0
        self.layoutMain = QVBoxLayout(self)
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.title = QLabel("Téléchargements")
        self.title.setAlignment(Qt.AlignHCenter)
        self.layoutMain.addWidget(self.title)
        self.layoutMain.addWidget(self.scroll)

        self.container = QWidget()
        self.scroll.setWidget(self.container)
        self.layout = QVBoxLayout(self.container)
        self.label = QLabel("Pas de téléchargement")
        self.label.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.label)

    def downloadrequested(self, download):
        if download:
            if download.state() == QWebEngineDownloadItem.DownloadRequested:
                path = QFileDialog.getSaveFileName(self, "Sauver comme", download.path())
                if path == "":
                    return
                else:
                    download.setPath(path[0])
                    download.accept()
                    self.add(DownloadWidget(download, self.parent.parent.browserWidget.url().toString(),
                                            self.parent.parent))

                    self.show()
            else:
                QMessageBox.warning(self, "ERREUR", "Le téléchargement n'a pas été demandé.")
        else:
            QMessageBox.warning(self, "ERREUR", "Le téléchargement est nul.")

    def add(self, downloadwidget):
        downloadwidget.downloadSignal.removeClicked.connect(self.remove)
        self.layout.addWidget(downloadwidget)
        self.layout.setAlignment(downloadwidget, Qt.AlignTop)
        self.nbDownload += 1
        if self.nbDownload >= 0:
            self.label.hide()

    def remove(self):
        downloadwidget = self.sender().parent
        self.layout.removeWidget(downloadwidget)
        downloadwidget.deleteLater()
        self.nbDownload -= 1
        if self.nbDownload <= 0:
            self.label.show()
