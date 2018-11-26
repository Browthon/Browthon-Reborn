import sqlite3


class DBConnection():
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

    def disconnect(self):
        self.connection.close()
    
    def createdb(self):
        self.executewithoutreturn("""
CREATE TABLE IF NOT EXISTS parameters(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    home TEXT,
    moteur TEXT,
    js TEXT
)""")
        self.executewithoutreturn("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    url TEXT
)""")
        self.executewithoutreturn("""
CREATE TABLE IF NOT EXISTS bookmarks(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    url TEXT
)""")
        self.executewithoutreturn("""
CREATE TABLE IF NOT EXISTS raccourcis(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    url TEXT
)""")
        if not self.executewithreturn("""SELECT home FROM parameters"""):
            self.executewithoutreturn("""INSERT INTO parameters(home, moteur, js) VALUES("http://google.com",
             "Google", "Activé")""")
