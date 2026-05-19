from database.connection import get_connection

def listar_veiculos(mostrar_inativos=False):
    try:
        with get_connection() as conn:
            if mostrar_inativos:
                cursor = conn.execute('''
                    SELECT id, nome, categoria, ativo
                    FROM veiculos
                    ORDER BY categoria, nome ASC
                    ''')
            else:
                cursor = conn.execute('''
                    SELECT id,nome,categoria
                    FROM veiculos
                    WHERE ativo = 1
                    ORDER BY categoria, nome ASC 
                        ''')
            
        return cursor.fetchall() 
        
    except Exception as e:
        return {"success": False,
                "message": f"Erro ao selecionar Veiculos: {e}"}
        
        
def adicionar_veiculo(nome,categoria):
    try:
        with get_connection() as conn:
            conn.execute('''
                INSERT INTO veiculos (nome,categoria) VALUES (?,?)
                                  ''',(nome,categoria))
    except Exception as e:
        return {"success": False,
                "message": f"Erro ao adicionar veiculo: {e}"
                }
        
    return {"success": True,
            "message": "Veiculo registrado com sucesso"
            }
    
def remover_veiculo(id):
    try:
        with get_connection() as conn:
            conn.execute("UPDATE veiculos SET ativo = 0 WHERE id = ?",(id,))
    
    except Exception as e:
        return {"success": False,
                "message": f"Erro ao inativar veículo: {e}"
                }
        
    return {"success": True,
            "message": "Veículo removido com sucesso"
            }
            
def ativar_veiculo(id):
    try:
        with get_connection() as conn:
            conn.execute("UPDATE veiculos SET ativo = 1 WHERE id = ?",(id,))
            
    except Exception as e:
        return {"success": False,
                "message": f"Erro ao ativar veículo: {e}"
                }
        
    return {"success": True,
            "message": "Veículo reativado com sucesso"
            }