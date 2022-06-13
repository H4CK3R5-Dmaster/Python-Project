import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self):

        self.conn = sqlite3.connect('database.db')
        if self.conn:
            print('connected')
            self.conn.execute("""CREATE TABLE IF NOT EXISTS pokemonshooter(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            victoire TEXT,
            defaite TEXT,
            score_victoire INTEGER,
            score_defaite INTEGER
            );
            """)
            print('table pokemon shooter ok')
            self.conn.execute("""CREATE TABLE IF NOT EXISTS tron(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                victoire TEXT,
                defaite TEXT,
                score_victoire INTEGER,
                score_defaite INTEGER
                );
                """)
            print('table tron ok')
            self.conn.execute("""CREATE TABLE IF NOT EXISTS pong(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                victoire TEXT,
                defaite TEXT,
                score_victoire INTEGER,
                score_defaite INTEGER
                );
                """)
            print('table pong ok')
            self.conn.execute("""CREATE TABLE IF NOT EXISTS joueur(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                joueur1 TEXT,
                joueur2 TEXT
                );
                """)
            print('table joueur ok')

            c = self.conn.cursor()
            c.execute('SELECT name from sqlite_master where type= "table"')
            print(c.fetchall())
        else:
            print('error with the file')

    def create_rq_insert(self, table, task):
        sql = """INSERT INTO {}(`victoire`, `defaite`, `score_victoire`, `score_defaite`) VALUES(?, ?, ?, ?)""".format(table)
        
        c = self.conn.cursor()
        c.execute(sql, task)
        self.conn.commit()
        c.execute('SELECT * from {}'.format(table))
        print(c.fetchall())
        return c.lastrowid
    
    def create_rq_insert_joueur(self,task):
        print(task)
        
        
        c = self.conn.cursor()
        c.execute('INSERT INTO joueur(`joueur1`, `joueur2`) VALUES(?, ?)', (task))
        self.conn.commit()
        c.execute('SELECT * from joueur')
        print(c.fetchall())
        return c.lastrowid
    
    
    
    def select(self, table, task):
        
        
        c = self.conn.cursor()
        c.execute('SELECT {} FROM {}'.format(task, table))
        self.ok = c.fetchall()
        
        return self.ok
    
    def select_limit(self, table, task):
        c = self.conn.cursor()
        c.execute('SELECT {} FROM {} WHERE id = (SELECT MAX(id) FROM {})ORDER BY {} LIMIT 1'.format(task, table, table, task))
        self.ok2 = c.fetchone()
        print(self.ok2)
        print("--------------------")
        return self.ok2
    
        
        
            

