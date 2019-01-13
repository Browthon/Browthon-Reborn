#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QTabWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl

from browthon.Core.Widgets.browserWidget import BrowserWidget
from browthon.Core.Utils.themeUtils import geticonpath

import os


class TabWidget(QTabWidget):
    def __init__(self, parent):
        super(TabWidget, self).__init__(parent)
        self.parent = parent
        self.closer = False
        self.addTabButton = QPushButton(QIcon(geticonpath(self.parent, "Icons/Tabs/tabs-add.png")), "")

        self.tabCloseRequested.connect(self.requestsremovetab)
        self.currentChanged.connect(self.ontabchange)
        self.addTabButton.clicked.connect(self.requestsaddtab)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.addTabButton.setFlat(True)
        self.setCornerWidget(self.addTabButton)
        self.setElideMode(Qt.ElideRight)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.requestsremovetab(self.tabBar().tabAt(event.pos()))
        super(TabWidget, self).mouseReleaseEvent(event)
    
    def requestsremovetab(self, index):
        if self.count() == 1:
            if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter Browthon ?",
                                      QMessageBox.Yes, QMessageBox.No) == 16384:
                self.closer = True
                self.parent.close()
        else:
            self.widget(index).deleteLater()
            self.removeTab(index)
    
    def settitle(self, widget):
        if widget.title() != "":
            self.setTabText(self.indexOf(widget), widget.title())

    def settitleloading(self, widget):
        self.setTabText(self.indexOf(widget), "Chargement...")
        self.setTabIcon(self.indexOf(widget), QIcon("logo.png"))
    
    def seticon(self, widget):
        if not widget.icon().isNull():
            self.setTabIcon(self.indexOf(widget), widget.icon())
    
    def ontabchange(self):
        self.parent.browserWidget = self.currentWidget()
        self.parent.urlInput.seturl()
        try:
            self.parent.forward.disconnect()
            self.parent.back.disconnect()
            self.parent.reload.disconnect()
        except Exception:
            pass
        self.parent.back.clicked.connect(self.parent.browserWidget.back)
        self.parent.forward.clicked.connect(self.parent.browserWidget.forward)
        self.parent.reload.clicked.connect(self.parent.browserWidget.reload)
        self.parent.settitle(self.parent.browserWidget)
        self.parent.checkbookmarkbutton()
    
    def requestsaddtab(self, url="", move=True):
        browserwidget = BrowserWidget(self.parent)
        self.addTab(browserwidget, QIcon(os.path.join(os.path.dirname(__file__), '../../logo.png')),
                    "Chargement...")
        browserwidget.show()
        index = self.currentIndex()
        self.setCurrentWidget(browserwidget)
        if not url:
            url = self.parent.dbConnection.executewithreturn("""SELECT home FROM parameters""")[0][0]
        browserwidget.load(QUrl(url))
        if not move:
            self.setCurrentIndex(index)
