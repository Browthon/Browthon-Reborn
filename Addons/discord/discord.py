#!/usr/bin/python3.6
# coding: utf-8

import sys

sys.path.append('..')


class Discord:
    def __init__(self):
        self.thread = 0

    def load(self, main):
        try:
            from pypresence import Presence
            import time
        except ImportError:
            print("PyPresence n'est pas installé sur votre machine.")
        else:
            client_id = "526065920519700480"
            self.RPC = Presence(client_id)
            self.RPC.connect()
            self.RPC.update(state="Navigateur internet en Python")

    def unload(self, main):
        self.thread.join(timeout=0)


instance = Discord
name = "discord"
