"""Database helpers for the Task Manager app (SQLite)."""
import sqlite3

DB_PATH = "tasks.db"


def get_connection(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    conn = get_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            due_date    TEXT,
            completed   INTEGER DEFAULT 0,
            created_at  TEXT
        )
        """
    )
    conn.commit()
    conn.close()
