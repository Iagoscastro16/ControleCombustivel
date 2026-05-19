from database.connection import get_connection

def listar_veiculos():
    try:
        with get_connection() as conn:
           cursor = conn.execute('''
                SELECT nome,categoria
                FROM veiculos
                ORDER BY categoria, nome ASC
                        ''')
            
        return cursor.fetchall() 
        
    except Exception as e:
        return {"success": False,
                "message": f"Erro ao selecionar Veiculos: {e}"}
        