import sqlite3
from pathlib import Path
from contextlib import contextmanager
import sys

def pasta_app():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent.parent.parent

ROOT =pasta_app()
DB_PATH = ROOT/ "data" / "combustivel.db"
DATA_DIR = ROOT / "data"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        with conn:
            yield conn
    finally:
        conn.close()