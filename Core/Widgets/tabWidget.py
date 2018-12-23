#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QTabWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from Core.Widgets.browserWidget import BrowserWidget
from Core.Utils.themeUtils import geticonpath


class TabWidget(QTabWidget):
    def __init__(self, parent):
        super(TabWidget, self).__init__(parent)
        self.parent = parent
        self.closer = False
        self.changedOnce = False
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
    
    def settitle(self):
        if self.parent.browserWidget.title() != "":
            titre = self.parent.browserWidget.title()
            self.setTabText(self.currentIndex(), titre)
    
    def seticon(self):
        if not self.parent.browserWidget.icon().isNull():
            self.setTabIcon(self.currentIndex(), self.parent.browserWidget.icon())
    
    def ontabchange(self):
        self.parent.browserWidget = self.currentWidget()
        self.parent.urlInput.seturl()
        try:
            self.parent.forward.disconnect()
            self.parent.back.disconnect()
            self.parent.reload.disconnect()
        except Exception:
            pass
        if self.changedOnce:
            self.parent.addhistory()
        else:
            self.changedOnce = True
        self.parent.back.clicked.connect(self.parent.browserWidget.back)
        self.parent.forward.clicked.connect(self.parent.browserWidget.forward)
        self.parent.reload.clicked.connect(self.parent.browserWidget.reload)
        self.parent.settitle()
        self.seticon()
    
    def requestsaddtab(self):
        browserwidget = BrowserWidget(self.parent)
        self.addTab(browserwidget, QIcon('logo.png'), "Nouvel Onglet")
        browserwidget.show()
        self.changedOnce = False
        self.setCurrentWidget(browserwidget)
