#!/usr/bin/python3.7
# coding: utf-8

import os
import glob


class AddonsManager:
    def __init__(self, main):
        self.main = main
        self.LML = {}
        self.imported = []
        self.libs = []
        self.unimported = []

    def include_all_modules(self):
        if os.path.exists("Addons/"):
            filess = glob.glob("Addons/*/*.py")
        else:
            filess = []
            print("Aucun addon trouvé")
        ext_libs = ["Addons.{}.{}".format(f.split("\\")[1], os.path.basename(f).split('.')[0]) for f in filess]
        self.imported = []
        for module in ext_libs:
            try:
                exec("import {}".format(module))
                self.imported.append(module)
                exec("self.LML[{}.name] = {}.instance".format(module, module))

            except ImportError:
                pass
        return ext_libs, self.imported

    def loadaddons(self):
        self.libs, self.imported = self.include_all_modules()
        self.unimported = set(self.imported) ^ set(self.libs)
        if self.unimported:
            print("Des modules ont été mal importés : {}".format(", ".join(list(self.unimported))))
        if self.imported:
            print("Des modules ont été importés : {}".format(", ".join(list(self.imported))))

    def launchaddons(self, widgets, function, args):
        for i in self.LML:
            for j in widgets:
                if j.datas["NameCode"] == i and j.datas["Activation"] == "True":
                    try:
                        if function == "load":
                            self.LML[i].load(self.LML[i], self.main)
                        elif function == "unload":
                            self.LML[i].unload(self.LML[i], self.main)
                        elif function == "keyPress":
                            self.LML[i].keypress(self.LML[i], self.main, args)
                        elif function == "enterUrl":
                            self.LML[i].enterurl(self.LML[i], self.main, args)
                        elif function == "openOnglet":
                            self.LML[i].openonglet(self.LML[i], self.main, args)
                    except Exception:
                        pass
                    break

