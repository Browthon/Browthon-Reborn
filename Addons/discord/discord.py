#!/usr/bin/python3.6
# coding: utf-8

import sys
import os

sys.path.append('..')

try:
    from pypresence import Presence, Activity
    import time
except ImportError:
    print("PyPresence n'est pas installé sur votre machine.")

class Discord:
    def __init__(self):
        self.launch = True
        
    def load(self, main):
        self.launch = True
        client_id = "526065920519700480"
        RPC = Presence(client_id)
        RPC.connect()
        ac = Activity(RPC, large_image="logo", large_text="Browthon",
                    small_image="logo", small_text=main.version,
                     details="Par LavaPower", state="Navigateur web en Python")
        ac.start = int(time.time())

instance = Discord
name = "discord"
