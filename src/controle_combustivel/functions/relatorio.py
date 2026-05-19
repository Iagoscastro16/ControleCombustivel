from database.connection import get_connection

def gerar_relatorio(ano):
    try:
        with get_connection() as conn:
            cursor = conn.execute('''
                SELECT v.nome, v.categoria, strftime('%m', a.data) as mes, sum(a.valor)
                FROM abastecimentos a
                JOIN veiculos v ON a.veiculo_id = v.id
                WHERE strftime('%Y', a.data) = ?
                GROUP BY v.nome, mes
                ORDER BY categoria, v.nome,mes
            ''',(ano,))
             
            return cursor.fetchall()
    except Exception as e:
        return {"success": False,
                "message": f"Erro ao gerar relatório: {e}"
                }   
       