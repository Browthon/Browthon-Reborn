#!/usr/bin/python3.6
# coding: utf-8

import sys

sys.path.append('..')


class Demo:
    def load(self, main):
        print("Chargement de l'addon Test")

    def keypress(self, main, event):
        print("Numéro Touche pressé :", event.key())

    def enterurl(self, main, url):
        print("Url entré : " + url)

    def openonglet(self, main, url):
        print("Nouvel onglet avec url : " + url)

    def unload(self, main):
        print("Déchargement de l'addon test")


instance = Demo
name = "demo"
