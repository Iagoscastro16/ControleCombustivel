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
                "message": f"erro ao listar lançamentos do mês: {e}"
                }
    

def listar_abastecimentos(mes,ano):

    mes_formatado = str(mes).zfill(2)
    ano_formatado = str(ano).zfill(4)
    
    try:
        with get_connection() as conn:
            cursor = conn.execute('''
                SELECT a.id, a.data, v.nome, a.valor
                FROM abastecimentos a
                JOIN veiculos v ON a.veiculo_id = v.id
                WHERE strftime('%Y', a.data) = ?
                AND strftime('%m', a.data) = ?
                ORDER BY a.data                  
                
                

                ''',(f"{ano_formatado}", f"{mes_formatado}"))
            
            return cursor.fetchall()
            

    except Exception as e:
        return {"success": False,
                "message":f"erro ao listar lançamentos do mês: {e}"
                }
    
def excluir_abastecimento(id):
    try:
        with get_connection() as conn:
            cursor = conn.execute('''
                DELETE FROM abastecimentos WHERE id = ?
                                  ''',(id,))
            
            
            linhas_afetadas = cursor.rowcount
            if linhas_afetadas == 0:
                return {"success": False,
                        "message": "Erro ao deletar abastecimento"
                        }
            else:
                return {"success": True,
                        "message": "Abastecimento deletado"
                        }            

    except Exception as e:
        return {"success": False,
                "message": f"Erro ao deletar abastecimento:{e}"
                }
    
def editar_abastecimentos(id, data=None, veiculo_id=None, valor=None):
    try:
        with get_connection() as conn:
            # Constrói a query dinamicamente apenas para campos fornecidos
            campos = []
            valores = []
            if data is not None:
                campos.append("data = ?")
                valores.append(data)
            if veiculo_id is not None:
                campos.append("veiculo_id = ?")
                valores.append(veiculo_id)
            if valor is not None:
                campos.append("valor = ?")
                valores.append(valor)
            
            # Se nenhum campo foi fornecido, retorna erro
            if not campos:
                return {"success": False, "message": "Nenhum dado fornecido para atualização"}
            
            # Completa a query com a cláusula WHERE
            valores.append(id)
            sql = f"UPDATE abastecimentos SET {', '.join(campos)} WHERE id = ?"
            
            cursor = conn.execute(sql, valores)
            linhas_afetadas = cursor.rowcount
            
            if linhas_afetadas == 0:
                return {"success": False, "message": "Abastecimento não encontrado ou dados idênticos"}
            else:
                return {"success": True, "message": "Abastecimento atualizado com sucesso"}
                
    except Exception as e:
        return {"success": False, "message": f"Erro inesperado: {e}"}   