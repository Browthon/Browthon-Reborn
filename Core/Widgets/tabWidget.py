#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QTabWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon

from Core.Widgets.browserWidget import BrowserWidget

class TabWidget(QTabWidget):
    def __init__(self, parent):
        super(TabWidget, self).__init__(parent)
        self.parent = parent
        self.addTabButton =  QPushButton(QIcon("Icons/Tabs/tabs-add.png"), "")

        self.tabCloseRequested.connect(self.requestsRemoveTab)
        self.currentChanged.connect(self.onTabChange)
        self.addTabButton.clicked.connect(self.requestsAddTab)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setCornerWidget(self.addTabButton)
        close_icon_path = "Icons/Tabs/tabs-close.png"
        self.setStyleSheet("QTabBar::close-button { image: url("+close_icon_path+"); }")
    
    def requestsRemoveTab(self, index):
        if self.count()==1:
            self.requestsAddTab()
        self.removeTab(index)
    
    def setTitle(self):
        if len(self.parent.browserWidget.title()) >= 13:
            titre = self.parent.browserWidget.title()[:9] + "..."
        else:
            titre = self.parent.browserWidget.title()
        self.setTabText(self.currentIndex(), titre)
    
    def setIcon(self):
        self.setTabIcon(self.currentIndex(), self.parent.browserWidget.icon())
    
    def onTabChange(self):
        self.parent.browserWidget = self.currentWidget()
        self.parent.urlInput.setUrl()
        self.parent.forward.disconnect()
        self.parent.back.disconnect()
        self.parent.reload.disconnect()
        self.parent.back.clicked.connect(self.parent.browserWidget.back)
        self.parent.forward.clicked.connect(self.parent.browserWidget.forward)
        self.parent.reload.clicked.connect(self.parent.browserWidget.reload)
    
    def requestsAddTab(self):
        browserWidget = BrowserWidget(self.parent)
        self.addTab(browserWidget, QIcon('logo.png'), "Nouvel Onglet")
        browserWidget.show()