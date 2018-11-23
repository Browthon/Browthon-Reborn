#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWebEngineWidgets import QWebEngineContextMenuData

class WebHitTestResult():
    def __init__(self, page, pos):
        self.page = page
        self.pos = pos
        self.m_linkUrl = self.page.url().toString()
        self.m_baseUrl = self.page.url().toString()
        self.viewportPos = self.page.mapToViewport(self.pos)
        self.source = """(function() {
        let e = document.elementFromPoint(%1, %2);
        if (!e)
            return;
        function isMediaElement(e) {
            return e.tagName == 'AUDIO' || e.tagName == 'VIDEO';
        };
        function isEditableElement(e) {
            if (e.isContentEditable)
                return true;
            if (e.tagName === 'INPUT' || e.tagName === 'TEXTAREA')
                return e.getAttribute('readonly') != 'readonly';
            return false;
        };
        function isSelected(e) {
            let selection = window.getSelection();
            if (selection.type !== 'Range')
                return false;
            return window.getSelection().containsNode(e, true);
        };
        let res = {
            baseUrl: document.baseURI,
            alternateText: e.getAttribute('alt'),
            boundingRect: '',
            imageUrl: '',
            contentEditable: isEditableElement(e),
            contentSelected: isSelected(e),
            linkTitle: '',
            linkUrl: '',
            mediaUrl: '',
            tagName: e.tagName.toLowerCase()
        };
        let r = e.getBoundingClientRect();
        res.boundingRect = [r.top, r.left, r.width, r.height];
        if (e.tagName == 'IMG')
            res.imageUrl = e.getAttribute('src');
        if (e.tagName == 'A') {
            res.linkTitle = e.text;
            res.linkUrl = e.getAttribute('href');
        }
        while (e) {
            if (res.linkTitle === '' && e.tagName === 'A') {
                res.linkTitle = e.text;
                if(res.linkUrl === '') {
                res.linkUrl = e.getAttribute('href');
                }
            }
            if (res.mediaUrl === '' && isMediaElement(e)) {
                res.mediaUrl = e.currentSrc;
                res.mediaPaused = e.paused;
                res.mediaMuted = e.muted;
            }
            e = e.parentElement;
        }
        return res;
        })()"""

        self.js = self.source.replace("%1", str(self.viewportPos.x())).replace("%2", str(self.viewportPos.y()))
        self.dic = self.page.executeJavaScript(self.js)
        if self.dic is None:
            return

        self.m_isNull = False
        try:
            self.m_baseUrl = self.dic["baseUrl"]
            self.m_alternateText = self.dic["alternateText"]
            self.m_imageUrl = self.dic["imageUrl"]
            self.m_isContentEditable = self.dic["contentEditable"]
            self.m_isContentSelected = self.dic["contentSelected"]
            self.m_linkTitle = self.dic["linkTitle"]
            self.m_linkUrl = self.dic["linkUrl"]
            self.m_mediaUrl = self.dic["mediaUrl"]
            self.m_tagName = self.dic["tagName"]
        except:
            pass
        try:
            self.m_mediaPaused = self.dic["mediaPaused"]
            self.m_mediaMuted = self.dic["mediaMuted"]
        except:
            pass

    def linkUrl(self):
        return self.m_linkUrl

    def isContentEditable(self):
        return self.m_isContentEditable

    def isContentSelected(self):
        return self.m_isContentSelected

    def imageUrl(self):
        try:
            return self.m_imageUrl
        except:
            return ""

    def mediaUrl(self):
        return self.m_mediaUrl

    def baseUrl(self):
        return self.m_baseUrl

    def updateWithContextMenuData(self, data):
        if data.isValid():
            pass
        else:
            return

        self.m_linkTitle = data.linkText()
        self.m_linkUrl = data.linkUrl().toString()
        self.m_isContentEditable = data.isContentEditable()
        if data.selectedText() == "":
            self.m_isContentSelected = False
        else:
            self.m_isContentSelected = True

        if data.mediaType() == QWebEngineContextMenuData.MediaTypeImage:
            self.m_imageUrl = data.mediaUrl().toString()
        elif data.mediaType() == QWebEngineContextMenuData.MediaTypeAudio or data.mediaType() == QWebEngineContextMenuData.MediaTypeVideo:
            self.m_mediaUrl = data.mediaUrl().toString()