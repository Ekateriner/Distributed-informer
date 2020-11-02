import sqlite3

conn = sqlite3.connect('ARGUMENTS.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE ARGUMENTS (
             task_id    TEXT PRIMARY KEY,
             template   TEXT, 
             measurement    TEXT, 
             tag    TEXT,
             info   INTEGER, 
             warn   INTEGER,
             crit   INTEGER)''')

conn.commit()
conn.close()
