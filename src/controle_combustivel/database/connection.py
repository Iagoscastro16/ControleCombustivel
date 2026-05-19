import sqlite3
from pathlib import Path
import sys

def pasta_app():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent.parent.parent

ROOT =pasta_app()
DB_PATH = ROOT/ "data" / "combustivel.db"
DATA_DIR = ROOT / "data"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
