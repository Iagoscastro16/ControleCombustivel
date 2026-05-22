from database.connection import get_connection
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.page import PageMargins

MESES_ABREV = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]


def gerar_relatorio(ano, mostrar_inativo=False):
        try:
            if mostrar_inativo == 1:
                with get_connection() as conn:
                    cursor = conn.execute('''
                        SELECT v.nome, v.categoria, strftime('%m', a.data) as mes, sum(a.valor)
                        FROM abastecimentos a
                        JOIN veiculos v ON a.veiculo_id = v.id
                        WHERE strftime('%Y', a.data) = ?
                        GROUP BY v.nome, mes
                        ORDER BY categoria, v.nome, mes
                    ''', (ano,))
                    return cursor.fetchall()
            else:
                with get_connection() as conn:
                    cursor = conn.execute('''
                        SELECT v.nome, v.categoria, strftime('%m', a.data) as mes, sum(a.valor)
                        FROM abastecimentos a
                        JOIN veiculos v ON a.veiculo_id = v.id
                        WHERE strftime('%Y', a.data) = ?
                        AND v.ativo = 1
                        GROUP BY v.nome, mes
                        ORDER BY categoria, v.nome, mes
                    ''', (ano,))
                    return cursor.fetchall()
        except Exception as e:
            return {"success": False,
                    "message": f"Erro ao gerar relatório: {e}"}


def exportar_excel(dados, ano, caminho):
    wb = Workbook()
    ws = wb.active
    ws.title = f"combustivel {ano}"

    veiculos = dados["veiculos"]
    totais_mes = dados["totais_mes"]

    # ── Helpers ───────────────────────────────────────────────
    COR_HEADER   = "1F4E79"  # azul escuro
    COR_TOTAL    = "7C2D12"  # laranja escuro
    COR_CAT      = "374151"  # cinza escuro pra categoria
    COR_BRANCO   = "FFFFFF"
    COR_LINHA_A  = "F9FAFB"  # linha clara
    COR_LINHA_B  = "F3F4F6"  # linha levemente diferente

    def estilo_header(cell):
        cell.font = Font(bold=True, color=COR_BRANCO, size=10)
        cell.fill = PatternFill(fill_type="solid", fgColor=COR_HEADER)
        cell.alignment = Alignment(horizontal="center", vertical="center")

    def estilo_total(cell, bold=True):
        cell.font = Font(bold=bold, color=COR_BRANCO, size=10)
        cell.fill = PatternFill(fill_type="solid", fgColor=COR_TOTAL)
        cell.alignment = Alignment(horizontal="center", vertical="center")

    def estilo_categoria(cell):
        cell.font = Font(bold=True, color=COR_BRANCO, size=9)
        cell.fill = PatternFill(fill_type="solid", fgColor=COR_CAT)
        cell.alignment = Alignment(horizontal="left", vertical="center")

    def formatar_valor(cell, valor, cor_fundo=None):
        cell.value = valor if valor else None
        cell.number_format = 'R$ #,##0.00'
        cell.alignment = Alignment(horizontal="center", vertical="center")
        if cor_fundo:
            cell.fill = PatternFill(fill_type="solid", fgColor=cor_fundo)

    # ── Função pra escrever um bloco (Jan-Jun ou Jul-Dez) ────
    def escrever_bloco(linha_inicio, meses_idx, meses_nomes):
        linha = linha_inicio

        # Título do bloco
        ws.merge_cells(f"A{linha}:H{linha}")
        ws[f"A{linha}"] = f"COMBUSTIVEL {ano} (POSTO/CAIXA)"
        ws[f"A{linha}"].font = Font(bold=True, size=13)
        ws[f"A{linha}"].alignment = Alignment(horizontal="center")
        linha += 1

        # Cabeçalho
        cell = ws.cell(row=linha, column=1, value="VEÍCULOS/PERÍODO")
        estilo_header(cell)
        for col, mes in enumerate(meses_nomes, start=2):
            estilo_header(ws.cell(row=linha, column=col, value=mes))
        # Coluna AV no final
        estilo_header(ws.cell(row=linha, column=len(meses_nomes)+2, value="A/V %"))
        linha += 1

        # Calcula total geral do período
        total_geral = sum(
            sum(v for i, v in enumerate(valores) if i in meses_idx and v)
            for _, _, valores in veiculos
        )

        # Agrupa por categoria
        categoria_atual = None
        for i_linha, (nome, categoria, valores) in enumerate(veiculos):
            # Separador de categoria
            if categoria != categoria_atual:
                categoria_atual = categoria
                cell = ws.cell(row=linha, column=1, value=categoria.upper())
                estilo_categoria(cell)
                ws.merge_cells(f"A{linha}:H{linha}")
                ws.row_dimensions[linha].height = 16
                linha += 1

            # Linha do veículo
            cor_bg = COR_LINHA_A if i_linha % 2 == 0 else COR_LINHA_B
            cell_nome = ws.cell(row=linha, column=1, value=nome)
            cell_nome.font = Font(size=9)
            cell_nome.fill = PatternFill(fill_type="solid", fgColor=cor_bg)
            cell_nome.alignment = Alignment(horizontal="left", vertical="center")

            total_veiculo = 0
            for col, idx in enumerate(meses_idx, start=2):
                val = valores[idx] if valores[idx] else None
                cell = ws.cell(row=linha, column=col)
                formatar_valor(cell, val, cor_bg)
                if val:
                    total_veiculo += val

            # AV
            av = (total_veiculo / total_geral * 100) if total_geral else 0
            cell_av = ws.cell(row=linha, column=len(meses_idx)+2)
            cell_av.value = av / 100 if av else None
            cell_av.number_format = '0.0%'
            cell_av.alignment = Alignment(horizontal="center", vertical="center")
            cell_av.fill = PatternFill(fill_type="solid", fgColor=cor_bg)

            ws.row_dimensions[linha].height = 15
            linha += 1

        # TOTAL MÊS
        cell = ws.cell(row=linha, column=1, value="TOTAL MÊS")
        estilo_total(cell)
        cell.alignment = Alignment(horizontal="left", vertical="center")

        for col, idx in enumerate(meses_idx, start=2):
            val = totais_mes[idx] if totais_mes[idx] else None
            cell = ws.cell(row=linha, column=col)
            cell.value = val
            if val:
                cell.number_format = 'R$ #,##0.00'
            estilo_total(cell, bold=False)

        # AV do total = 100%
        cell_av = ws.cell(row=linha, column=len(meses_idx)+2)
        cell_av.value = 1.0
        cell_av.number_format = '0.0%'
        estilo_total(cell_av, bold=True)

        ws.row_dimensions[linha].height = 16
        linha += 1

        # ── ANÁLISE HORIZONTAL ────────────────────────────────
        COR_AH = "1F4E79"

        cell = ws.cell(row=linha, column=1, value="A/H %")
        cell.font = Font(bold=True, color=COR_BRANCO, size=9)
        cell.fill = PatternFill(fill_type="solid", fgColor=COR_AH)
        cell.alignment = Alignment(horizontal="left", vertical="center")

        totais_bloco = [totais_mes[idx] for idx in meses_idx]
        for col, (atual, anterior) in enumerate(zip(totais_bloco[1:], totais_bloco[:-1]), start=3):
            if anterior and anterior != 0:
                ah = (atual / anterior - 1)
            else:
                ah = None

            cell = ws.cell(row=linha, column=col)
            cell.value = ah
            if ah is not None:
                cell.number_format = '+0.0%;-0.0%;0.0%'
            cell.font = Font(bold=False, color=COR_BRANCO, size=9)
            cell.fill = PatternFill(fill_type="solid", fgColor=COR_AH)
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # Preenche coluna 2 (primeiro mês não tem anterior)
        cell = ws.cell(row=linha, column=2)
        cell.value = "-"
        cell.font = Font(color=COR_BRANCO, size=9)
        cell.fill = PatternFill(fill_type="solid", fgColor=COR_AH)
        cell.alignment = Alignment(horizontal="center", vertical="center")

        # Preenche coluna AV com traço
        cell = ws.cell(row=linha, column=len(meses_idx)+2)
        cell.value = "-"
        cell.font = Font(color=COR_BRANCO, size=9)
        cell.fill = PatternFill(fill_type="solid", fgColor=COR_AH)
        cell.alignment = Alignment(horizontal="center", vertical="center")

        ws.row_dimensions[linha].height = 15
        linha += 1

        return linha

    # ── Bloco 1: Jan-Jun ─────────────────────────────────────
    linha_atual = 1
    linha_atual = escrever_bloco(linha_atual, list(range(0, 6)), MESES_ABREV[0:6])

    # Espaço entre blocos
    linha_atual += 1

    # ── Bloco 2: Jul-Dez ─────────────────────────────────────
    escrever_bloco(linha_atual, list(range(6, 12)), MESES_ABREV[6:12])

    # ── Largura das colunas ───────────────────────────────────
    ws.column_dimensions["A"].width = 28
    for col_letter in ["B", "C", "D", "E", "F", "G"]:
        ws.column_dimensions[col_letter].width = 13
    ws.column_dimensions["H"].width = 10  # AV

    # ── Página ───────────────────────────────────────────────
    ws.page_setup.orientation = 'portrait'
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0

    wb.save(caminho)