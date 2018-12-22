#!/usr/bin/python3.7
# coding: utf-8

import os


def parsetheme(bssstring, folder):
    bsslist = bssstring.split("\n")
    i = 0
    while i < len(bsslist):
        if bsslist[i] != "":
            if bsslist[i][0] == "#":
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
