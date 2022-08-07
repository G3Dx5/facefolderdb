#!/usr/bin/env python3

import datetime
import sqlite3
import time

class Createdb:
    def dbrun(self):
        ''' creates the database '''
        conn = sqlite3.connect('facematch.db')
        curs = conn.cursor()
        try:
            curs.execute("""CREATE TABLE IF NOT EXISTS matches (date integer, time integer, match text, filemaster text, filecompared text)""")
        except sqlite3.OperationalError:
            print("sqlite error")
        pass

db = Createdb()
db.dbrun()
