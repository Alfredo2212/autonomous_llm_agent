'''
Handles logging using sqlite
Aim to produce clear audit train of LLM queries and outputs
Output is query_logs.db 
'''
import sqlite3
from datetime import datetime, timezone
import os

DB_PATH = "query_logs.db"

# Connects to SQLite database, if not file -> create file
# Defines table called logs with id, timestamp, query, answer and sources
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

# Logging new query. Captures current time, converts list of filenames
# into string ' ' separated and connects to DB to insert new record
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