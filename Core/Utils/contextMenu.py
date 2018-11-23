#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QMenu

class ContextMenu(QMenu):
    def __init__(self, onglet, hitTest):
        super(ContextMenu, self).__init__()
        self.onglet = onglet
        contextMenuData = self.onglet.page.contextMenuData()
        hitTest.updateWithContextMenuData(contextMenuData)
        self.addAction("Retour", self.onglet.back)
        self.addAction("Avancer", self.onglet.forward)
        self.addAction("Recharger", self.onglet.reload)
        bookmarks = self.onglet.parent.dbConnection.executeWithReturn("""SELECT * FROM bookmarks""")
        find = False
        for i in bookmarks:
            if i[2] == self.onglet.parent.browserWidget.url().toString():
                find = True
        if find:
            self.addAction("Supprimer Favori", self.onglet.parent.fav)
        else:
            self.addAction("Ajouter Favori", self.onglet.parent.fav)
        if hitTest.isContentEditable():
            self.addSeparator()
            self.addAction("Couper", self.onglet.page.cutAction)
            self.addAction("Copier", self.onglet.page.copyAction)
            self.addAction("Coller", self.onglet.page.pasteAction)
        if hitTest.imageUrl() != "":
            self.addSeparator()
            self.addAction("Voir Image", lambda: self.onglet.parent.openNewOngletWithUrl(hitTest.imageUrl()))
        self.addSeparator()
        clickedUrl = hitTest.linkUrl()
        baseUrl = hitTest.baseUrl()
        if clickedUrl != baseUrl and clickedUrl != '':
            if 'http://' in clickedUrl or 'https://' in clickedUrl:
                url = clickedUrl
            elif clickedUrl == "#":
                url = baseUrl + clickedUrl
            else:
                url = "http://" + baseUrl.split("/")[2] + clickedUrl
            self.addAction("Ouvrir Nouvel Onglet", lambda: self.onglet.parent.openNewOngletWithUrl(url))