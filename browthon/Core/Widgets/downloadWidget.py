#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QProgressBar
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem
from PyQt5.QtCore import QFileInfo

from browthon.Core.Widgets.pushButton import PushButton
from browthon.Core.Utils.downloadUtils import DownloadSignal


class DownloadWidget(QWidget):
    def __init__(self, download, url, main):
        super(DownloadWidget, self).__init__()
        self.layout = QGridLayout()
        self.title = QLabel("NAME")
        self.cancel = PushButton("Cancel")
        self.progressBar = QProgressBar()
        self.setupui()
        self.download = download
        self.url = url
        self.main = main
        self.downloadSignal = DownloadSignal(self)
        self.title.setText(QFileInfo(self.download.path()).fileName())

        self.cancel.clicked.connect(self.canceldownload)
        self.download.downloadProgress.connect(self.updatewidget)
        self.download.stateChanged.connect(self.updatewidget)

        self.updatewidget()

    def updatewidget(self):
            totalbytes = self.download.totalBytes()
            receivedbytes = self.download.receivedBytes()

            state = self.download.state()
            if state == QWebEngineDownloadItem.DownloadRequested:
                pass
            elif state == QWebEngineDownloadItem.DownloadInProgress:
                if totalbytes > 0:
                    self.progressBar.setValue(int(100 * receivedbytes / totalbytes))
                    self.progressBar.setDisabled(False)
                    self.progressBar.setFormat("%p% - {} téléchargés sur {}".format(self.withunit(receivedbytes),
                                                                                    self.withunit(totalbytes)))
                else:
                    self.progressBar.setValue(0)
                    self.progressBar.setDisabled(False)
                    self.progressBar.setFormat("Taille inconnue - {} téléchargés".format(self.withunit(receivedbytes)))
            elif state == QWebEngineDownloadItem.DownloadCompleted:
                self.progressBar.setValue(100)
                self.progressBar.setDisabled(True)
                self.progressBar.setFormat("Complété - {} téléchargés".format(self.withunit(receivedbytes)))
            elif state == QWebEngineDownloadItem.DownloadCancelled:
                self.progressBar.setValue(0)
                self.progressBar.setDisabled(True)
                self.progressBar.setFormat("Annulé - {} téléchargés".format(self.withunit(receivedbytes)))
            elif state == QWebEngineDownloadItem.DownloadInterrupted:
                self.progressBar.setValue(0)
                self.progressBar.setDisabled(True)
                self.progressBar.setFormat("Interrompu - {}".format(self.download.interruptReasonString()))

            if state == QWebEngineDownloadItem.DownloadInProgress:
                self.cancel.setText("Arrêter")
                self.cancel.setToolTip("Stopper le téléchargement")
            else:
                self.cancel.setText("Supprimer")
                self.cancel.setToolTip("Enlever le téléchargement")

    def canceldownload(self):
        if self.download.state() == QWebEngineDownloadItem.DownloadInProgress:
            self.download.cancel()
        else:
            self.downloadSignal.removeClicked.emit()

    def withunit(self, bytesnb):
        if bytesnb < 1 << 10:
            return str(round(bytesnb, 2)) + " B"
        elif bytesnb < 1 << 20:
            return str(round(bytesnb / (1 << 10), 2)) + " KiB"
        elif bytesnb < 1 << 30:
            return str(round(bytesnb / (1 << 20), 2)) + " MiB"
        else:
            return str(round(bytesnb / (1 << 30), 2)) + " GiB"

    def setupui(self):
        self.layout.addWidget(self.title, 1, 1)
        self.layout.addWidget(self.progressBar, 2, 1)
        self.layout.addWidget(self.cancel, 3, 1)
        self.setLayout(self.layout)
