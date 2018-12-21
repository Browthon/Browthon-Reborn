#!/usr/bin/python3.7
# coding: utf-8

import os


def parsetheme(bssstring):
    bsslist = bssstring.split("\n")
    i = 0
    while i < len(bsslist):
        if bsslist[i] != "":
            if bsslist[i][0] == "#":
                del bsslist[i]
        i += 1
    bssstring = "\n".join(bsslist)
    bssstring.replace("bproperty", "qproperty")
    bssstring.replace("blineargradient", "qlineargradient")

    bssstring.replace("\\4", "")

    return bssstring


def geticonpath(main, basicpath):
    if main.theme == "" or main.theme == "Themes/":
        return basicpath
    else:
        if basicpath.split("/")[-1] in os.listdir(main.theme + "/" + "/".join(basicpath.split("/")[:-1])):
            return main.theme + "/" + basicpath
        else:
            return basicpath
        print()
