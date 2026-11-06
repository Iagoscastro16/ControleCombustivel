from database.connection import  get_connection


def criar_tabelas():
    try:
        with get_connection() as conn:
            # BEGIN explícito: sem ele o sqlite3 grava cada CREATE na hora
            # e o rollback do "with conn" não desfaz a tabela já criada
            conn.execute("BEGIN")
            conn.execute('''
                CREATE TABLE IF NOT EXISTS veiculos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    ativo INTEGER NOT NULL DEFAULT 1
                    )
            ''')
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
                "message": f"Erro na criação das tabelas: {e}"}
    
    return {"success": True, "message":"Tabelas criadas com sucesso"}

def popular_dados_iniciais():
    try:
        from database import seed
        with get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM veiculos")
            if cursor.fetchone()[0] == 0:
                seed.popular(conn)
    except (ModuleNotFoundError, ImportError):
        pass
    
def inicializar_db():
    resultado = criar_tabelas()
    if not resultado["success"]:
        return resultado

    popular_dados_iniciais()
    return resultado