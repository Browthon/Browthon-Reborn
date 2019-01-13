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
        if os.path.exists(os.path.join(os.path.dirname(__file__), "../../Addons/")):
            filess = glob.glob(os.path.join(os.path.dirname(__file__), "../../Addons/*/*.py"))
        else:
            filess = []
            print("Aucun addon trouvé")
        ext_libs = []
        for f in filess:
            liste = f.split("\\")
            if len(liste) == 1:
                liste = f.split("/")
            ext_libs.append("browthon.Addons.{}.{}".format(liste[1], os.path.basename(f).split('.')[0]))
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

