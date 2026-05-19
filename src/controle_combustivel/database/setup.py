from database.connection import  get_connection


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
    
    return {"success": True, "message":"Tabelas criadas com sucesso"}

def popular_dados_iniciais():
    try:
        import importlib
        seed = importlib.import_module("database.seed")
        with get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM veiculos")
            if cursor.fetchone()[0] == 0:
                seed.popular(conn)
    except ModuleNotFoundError:
        pass
    
def inicializar_db():
    criar_tabelas()
    popular_dados_iniciais()