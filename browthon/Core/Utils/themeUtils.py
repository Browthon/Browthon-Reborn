#!/usr/bin/python3.7
# coding: utf-8

import os


def parsetheme(bssstring, folder):
    bsslist = bssstring.split("\n")
    i = 0
    while i < len(bsslist):
        if bsslist[i] != "":
            if bsslist[i][0:1] == "//":
                del bsslist[i]
        i += 1
    bssstring = "\n".join(bsslist)
    bssstring = bssstring.replace("bproperty", "qproperty")
    bssstring = bssstring.replace("blineargradient", "qlineargradient")

    bssstring = bssstring.replace("\\4", "")
    folderlist = folder.split("/")
    if len(folderlist) == 1:
        folderlist = folder.split("\\")
    i=0
    while True:
        if folderlist[i] == "..":
            del folderlist[i]
            del folderlist[i-1]
        i += 1
        if i >= len(folderlist):
            break
    folder = "/".join(folderlist)
    bssstring = bssstring.replace("url(", "url("+folder+"/")

    return bssstring


def geticonpath(main, basicpath):
    if main.theme == "" or main.theme == "../../Themes/":
        return basicpath
    else:
        basicpathlist = basicpath.split("/")
        del basicpathlist[0]
        for i in range(0, len(basicpathlist)):
            if i == 0:
                if not basicpathlist[i] in os.listdir(main.theme):
                    return basicpath
            else:
                if not basicpathlist[i] in os.listdir(main.theme + "/" + "/".join(basicpathlist[:i])):
                    return basicpath
        folderlist = main.theme.split("/")
        if len(folderlist) == 1:
            folderlist = main.theme.split("\\")
        i = 0
        while True:
            if folderlist[i] == "..":
                del folderlist[i]
                del folderlist[i - 1]
            i += 1
            if i >= len(folderlist):
                break
        folder = "/".join(folderlist)
        for i in basicpathlist:
            folder = os.path.join(folder, i)
        return folder
