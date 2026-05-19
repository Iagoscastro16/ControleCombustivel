from database. connection import get_connection
from datetime import datetime

def inserir_abastecimento(data,veiculo_nome, valor):
    try:
        with get_connection() as conn:
            cursor = conn.execute("SELECT id FROM veiculos WHERE nome = ?", (veiculo_nome,))
            veiculo_id = cursor.fetchone()[0]
            
            
            conn.execute('''
                
                INSERT INTO abastecimentos (data, veiculo_id, valor) VALUES (?,?,?)
                                  ''',(data,veiculo_id,valor))
    except Exception as e:
        return {"success": False,
                "message": f"Erro ao inserir um novo registo: {e}"
                }
        
    return {"success": True,
            "message": "Registro criado com sucesso"}
    
    
    
    
def contar_lancamentos_mes():
    try:
        with get_connection() as conn:
            ano_mes = datetime.now().strftime("%Y-%m")
            
        cursor = conn.execute(
            "SELECT COUNT(*) FROM abastecimentos WHERE data LIKE ?",
            (f"{ano_mes}%",)
        )
        
        return cursor.fetchone()[0]
    
    except Exception as e:
        return {"success": False,
                "message": f"erro ao listar lançamentos do mes: {e}"
                }