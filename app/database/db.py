import sqlite3
import os
import os

DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "jobs.db"))


def get_connection():
    conn = sqlite3.connect(DB_Path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            title        TEXT NOT NULL,
            company      TEXT NOT NULL,
            location     TEXT,
            stipend      TEXT,
            duration     TEXT,
            url          TEXT UNIQUE,
            source       TEXT,
            keyword      TEXT,
            ai_score     INTEGER DEFAULT 0,
            ai_reason    TEXT,
            applied      INTEGER DEFAULT 0,
            scraped_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialised.")