from pathlib import Path
import sqlite3
from config import  DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn 

def criar_tabelas():
    try:
        with get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS veiculos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    categoria TEXT NOT NULL
                    )
            ''')
    except Exception as e:
        return {"success": False,
                "message": f"Erro na criação da tabela 'veiculos': {e}"
                }
    try:        
        with get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS abastecimentos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    veiculo_id INTEGER NOT NULL,
                    valor REAL NOT NULL,
                    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
                )
            ''')
    except Exception as e:
        return {"success": False,
                "message": f"Erro na criação da tabela 'abastecimentos': {e}"}
    
    return ("success": True, "message":"Tabelas criadas com sucesso")

def popular_dados_iniciais():
    try:
        importlib
        seed = importlib.import_module("seed")
        seed.popular()
    except ModuleNotFoundError:
        pass