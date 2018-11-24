#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QTabWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from Core.Widgets.browserWidget import BrowserWidget

class TabWidget(QTabWidget):
    def __init__(self, parent):
        super(TabWidget, self).__init__(parent)
        self.parent = parent
        self.changedOnce = False
        self.addTabButton =  QPushButton(QIcon("Icons/Tabs/tabs-add.png"), "")

        self.tabCloseRequested.connect(self.requestsRemoveTab)
        self.currentChanged.connect(self.onTabChange)
        self.addTabButton.clicked.connect(self.requestsAddTab)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.addTabButton.setFlat(True)
        self.setCornerWidget(self.addTabButton)
        self.setStyleSheet("""
QTabBar::close-button {
    image: url("Icons/Tabs/tabs-close.png");
}
QTabBar::tab { 
    width: 200px; 
}""")
        self.setElideMode(Qt.ElideRight)
    
    def requestsRemoveTab(self, index):
        if self.count()==1:
            if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter Browthon ?", QMessageBox.Yes, QMessageBox.No) == 16384:
                self.parent.close()
        else:
            self.removeTab(index)
    
    def setTitle(self):
        titre = self.parent.browserWidget.title()
        self.setTabText(self.currentIndex(), titre)
    
    def setIcon(self):
        self.setTabIcon(self.currentIndex(), self.parent.browserWidget.icon())
    
    def onTabChange(self):
        self.parent.browserWidget = self.currentWidget()
        self.parent.urlInput.setUrl()
        try:
            self.parent.forward.disconnect()
            self.parent.back.disconnect()
            self.parent.reload.disconnect()
        except:
            pass
        if self.changedOnce:
            self.parent.addHistory()
        else:
            self.changedOnce = True
        self.parent.back.clicked.connect(self.parent.browserWidget.back)
        self.parent.forward.clicked.connect(self.parent.browserWidget.forward)
        self.parent.reload.clicked.connect(self.parent.browserWidget.reload)
    
    def requestsAddTab(self):
        browserWidget = BrowserWidget(self.parent)
        self.addTab(browserWidget, QIcon('logo.png'), "Nouvel Onglet")
        browserWidget.show()
        self.changedOnce = False
        self.setCurrentWidget(browserWidget)