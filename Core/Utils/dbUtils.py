import sqlite3

class DBConnection():
    def __init__(self, fichier):
        self.connection = sqlite3.connect(fichier)

    def executeWithoutReturn(self, query, tuples = ""):
        self.cursor = self.connection.cursor()
        if tuples == "":
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, tuples)
        self.connection.commit()
    
    def executeWithReturn(self, query, tuples = ""):
        self.cursor = self.connection.cursor()
        if tuples == "":
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, tuples)
        return self.cursor.fetchall()

    def disconnect(self):
        self.connection.close()
    
    def createDB(self):
        self.executeWithoutReturn("""
CREATE TABLE IF NOT EXISTS parameters(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    home TEXT
)""")
        self.executeWithoutReturn("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    url TEXT
)""")
        self.executeWithoutReturn("""
CREATE TABLE IF NOT EXISTS bookmarks(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    url TEXT
)""")
        if self.executeWithReturn("""SELECT home FROM parameters""") == [] :
            self.executeWithoutReturn("""INSERT INTO parameters(home) VALUES("http://google.com")""")