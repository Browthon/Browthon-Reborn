import sqlite3

class DBConnection():
    def __init__(self, fichier):
        self.connection = sqlite3.connect(fichier)

    def executeWithoutReturn(self, query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        self.connection.commit()
    
    def executeWithReturn(self, query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def disconnect(self):
        self.connection.close()