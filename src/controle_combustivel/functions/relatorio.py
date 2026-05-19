from database.connection import get_connection
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

MESES_ABREV=["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]

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
       
def exportar_excel(dados, ano, caminho):
    wb = Workbook()
    ws = wb.active
    ws.title = f"combustivel {ano}"
    
    ws.merge_cells("A1:N1")
    ws["A1"] = f"COMBUSTIVEL {ano} (POSTO/CAIXA)"
    ws["A1"].font = Font(bold=True, size=14)
    ws["A1"].alignment = Alignment(horizontal="center")
    
    cabecalhos = ["VEÍCULOS/PERÍODO"] + MESES_ABREV
    
    for col, titulo in enumerate(cabecalhos, start=1):
        cell = ws.cell(row=2, column=col, value=titulo)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor="1F4E79")
        cell.alignment = Alignment(horizontal="center")
    
    
    linha = 3
    
    for nome, categoria, valores in dados["veiculos"]:
        ws.cell(row=linha, column=1, value=nome)
        
        for col, valor in enumerate(valores, start=2):
            if valor:
                cell = ws.cell(row=linha, column=col, value=valor)
                cell.number_format = 'R$ #,##0.00'
                
        linha += 1
        
    ws.cell(row=linha, column=1, value="TOTAL MÊS")
    
    for col, valor in enumerate(dados["totais_mes"], start=2):
        if valor:
            cell = ws.cell(row=linha, column=col, value=valor)
            cell.number_format = 'R$ #,##0.00'
            
    for col in range(1,14):
        cell = ws.cell(row=linha, column=col)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor="375623")

    wb.save(caminho)