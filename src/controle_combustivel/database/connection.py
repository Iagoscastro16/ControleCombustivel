import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
DB_PATH = ROOT/ "data" / "combustivel.db"
DATA_DIR = ROOT / "data"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
