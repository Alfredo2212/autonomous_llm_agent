import sqlite3
from datetime import datetime, timezone
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

def log_query(query: str, answer: str, sources: list):
    timestamp = datetime.now(timezone.utc).isoformat()
    sources_str = ". ".join(sources)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
              INSERT INTO logs (timestamp, query, answer, sources)
              VALUES (?, ?, ?, ?)
              ''', (timestamp, query, answer, sources_str))
    conn.commit()
    conn.close()