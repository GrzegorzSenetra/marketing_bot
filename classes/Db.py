import sqlite3

class Db: 
    con = None
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        self.con = sqlite3.connect(self.db_name)
        print("Connected to " + self.db_name)
    
    def close(self):
        self.con.close()
        print("Connection closed")
        
    def cursor(self):
        return self.con.cursor()
