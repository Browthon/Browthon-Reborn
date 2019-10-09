#!/usr/bin/python3.6
# coding: utf-8

import json
import os


class Blacklist:
    def __init__(self):
        with open(os.path.join(os.path.abspath(__file__), "addon.json"), "r") as f:
            data = json.load(f)
        self.sites = data["Sites"]

    def enterurl(self, main, url):
        for i in self.sites:
            if i in url:
                print("blacklist")


instance = Blacklist
name = "blacklist"
