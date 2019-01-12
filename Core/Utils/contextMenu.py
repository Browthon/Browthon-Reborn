#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QApplication

from Core.Utils.downloadUtils import downloadfile


class ContextMenu(QMenu):
    def __init__(self, onglet, hittest):
        super(ContextMenu, self).__init__()
        self.onglet = onglet
        contextmenudata = self.onglet.page.contextMenuData()
        hittest.updatewithcontextmenudata(contextmenudata)
        self.addAction("Retour", self.onglet.back)
        self.addAction("Avancer", self.onglet.forward)
        self.addAction("Recharger", self.onglet.reload)
        self.addAction("Voir Source", self.onglet.page.vsource)
        self.addAction("Copier Lien", lambda: QApplication.clipboard().setText(self.onglet.url().toString()))
        self.addAction("Enregistrer Page", lambda: self.onglet.page.triggerAction(self.onglet.SavePage))
        self.addSeparator()
        bookmarks = self.onglet.parent.dbConnection.executewithreturn("""SELECT * FROM bookmarks""")
        find = False
        for i in bookmarks:
            if i[2] == self.onglet.parent.browserWidget.url().toString():
                find = True
        if find:
            self.addAction("Supprimer Favori", self.onglet.parent.fav)
        else:
            self.addAction("Ajouter Favori", self.onglet.parent.fav)
        if hittest.iscontenteditable():
            self.addSeparator()
            self.addAction("Couper", lambda: self.onglet.page.triggerAction(self.onglet.page.Cut))
            self.addAction("Copier", lambda: self.onglet.page.triggerAction(self.onglet.page.Copy))
            self.addAction("Coller", lambda: self.onglet.page.triggerAction(self.onglet.page.Paste))
        if hittest.imageurl() != "":
            self.addSeparator()
            self.addAction("Voir Image", lambda: self.onglet.parent.opennewongletwithurl(hittest.imageurl()))
            self.addAction("Copier Lien Image", lambda: QApplication.clipboard().setText(hittest.imageurl()))
            self.addAction("Enregistrer Image", lambda: downloadfile(self, hittest.imageurl()))
        self.addSeparator()
        clickedurl = hittest.linkurl()
        baseurl = hittest.baseurl()
        if clickedurl != baseurl and clickedurl != '':
            if 'http://' in clickedurl or 'https://' in clickedurl:
                url = clickedurl
            elif clickedurl == "#":
                url = baseurl + clickedurl
            else:
                url = "http://" + baseurl.split("/")[2] + clickedurl
            self.addAction("Copier Lien", lambda: QApplication.clipboard().setText(url))
            self.addAction("Enregistrer Lien", lambda: self.onglet.page.triggerAction(self.onglet.page.DownloadLinkToDisk))
            self.addAction("Ouvrir Nouvel Onglet", lambda: self.onglet.parent.opennewongletwithurl(url))
