import sqlite3


def majdb(fichier, versionacc, versioncompa):
    while versionacc < versioncompa:
        eval("majdbto"+str(versionacc+1)+"("+fichier+")")
        versionacc += 1
    return versionacc


class DBConnection:
    def __init__(self, fichier):
        self.connection = sqlite3.connect(fichier)
        self.cursor = self.connection.cursor()

    def executewithoutreturn(self, query, tuples=""):
        self.cursor = self.connection.cursor()
        if tuples == "":
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, tuples)
        self.connection.commit()
    
    def executewithreturn(self, query, tuples = ""):
        self.cursor = self.connection.cursor()
        if tuples == "":
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, tuples)
        return self.cursor.fetchall()

    def reconnect(self, fichier):
        self.connection = sqlite3.connect(fichier)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()
    
    def createdb(self):
        self.executewithoutreturn("""
CREATE TABLE IF NOT EXISTS parameters(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    home TEXT,
    moteur TEXT,
    js TEXT,
    theme TEXT,
    first TEXT,
    private TEXT
)""")
        self.executewithoutreturn("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    url TEXT,
    date TEXT
)""")
        self.executewithoutreturn("""
CREATE TABLE IF NOT EXISTS bookmarks(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    url TEXT,
    date TEXT
)""")
        self.executewithoutreturn("""
CREATE TABLE IF NOT EXISTS raccourcis(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    url TEXT,
    date TEXT
)""")
        self.executewithoutreturn("""
CREATE TABLE IF NOT EXISTS sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    urls TEXT,
    date TEXT
)""")
        self.executewithoutreturn("""
CREATE TABLE IF NOT EXISTS informations(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    version INTEGER
)""")
        if not self.executewithreturn("""SELECT home FROM parameters"""):
            self.executewithoutreturn("""INSERT INTO parameters(home, moteur, js, theme, first, private) VALUES("http://google.com",
             "Google", "Activé", "default", "O", "Désactivé")""")
        if not self.executewithreturn("""SELECT version FROM informations"""):
            self.executewithoutreturn("""INSERT INTO informations(version) VALUES(1)""")
