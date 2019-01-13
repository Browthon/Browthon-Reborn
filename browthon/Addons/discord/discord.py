#!/usr/bin/python3.6
# coding: utf-8

import sys

sys.path.append('..')

try:
    from pypresence import Presence, Activity
    import time
    from threading import Thread
except ImportError:
    print("PyPresence n'est pas installé sur votre machine.")


class DiscordRPC(Thread):
    def __init__(self, addon, main, rpc):
        super(DiscordRPC, self).__init__()
        self.addon = addon
        self.main = main
        self.rpc = rpc

    def run(self):
        self.rpc.connect()
        ac = Activity(self.rpc, large_image="logo", large_text="Browthon",
                      small_image="logo", small_text=self.main.version,
                      details="Par LavaPower", state="Navigateur web en Python")
        ac.start = int(time.time())
        while self.addon.launch:
            pass
        self.rpc.close()


class Discord:
    def __init__(self):
        self.launch = True
        self.thread = 0

    def load(self, main):
        self.launch = True
        client_id = "526065920519700480"
        rpc = Presence(client_id)

        self.thread = DiscordRPC(self, main, rpc)
        self.thread.start()

    def unload(self, main):
        self.launch = False
        self.thread.join()

instance = Discord
name = "discord"
