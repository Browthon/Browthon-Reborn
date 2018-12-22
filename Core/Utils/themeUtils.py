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
    bssstring = bssstring.replace("url(", "url("+folder+"/")

    return bssstring


def geticonpath(main, basicpath):
    if main.theme == "" or main.theme == "Themes/":
        return basicpath
    else:
        basicpathlist = basicpath.split("/")
        for i in range(0, len(basicpathlist)):
            if i == 0:
                if not basicpathlist[i] in os.listdir(main.theme):
                    return basicpath
            else:
                if not basicpathlist[i] in os.listdir(main.theme + "/" + "/".join(basicpathlist[:i])):
                    return basicpath
        return main.theme + "/" + basicpath
