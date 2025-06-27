import sqlite3
from datetime import datetime
import os

DB_PATH = "query_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS logs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp TEXT,
              query TEXT,
              answer TEXT,
              sources TEXT
              )
              ''')
    conn.commit()
    conn.close()

init_db()