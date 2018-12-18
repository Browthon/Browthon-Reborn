#!/usr/bin/python3.7
# coding: utf-8


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
