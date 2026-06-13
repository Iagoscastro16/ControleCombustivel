import os
import platform
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog
from functions.relatorio import gerar_relatorio, exportar_excel
from functions.utils import calcular_av, calcular_ah

CORES = {
    "header":    "#1C1917",
    "primario":  "#F97316",
    "hover":     "#EA6C0A",
    "sucesso":   "#10B981",
    "perigo":    "#EF4444",
    "texto":     "#1F2937",
    "texto_sec": "#6B7280",
    "borda":     "#D1D5DB",
    "card":      "#FFFFFF",
    "fundo":     "#F0F4F8",
}

MESES_ABREV = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
               "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]

MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro",
]

# Colunas fixas — só nome e A/V% têm tamanho definido
# As colunas de mês se esticam automaticamente via grid weight=1
COL_NOME  = 200
COL_TOTAL = 90
COL_AV    = 65


def _row_grid(parent, n_meses, fg_color, corner_radius=4):
    """
    Cria um frame filho com grid configurado:
      col 0        → nome (COL_NOME, sem stretch)
      col 1..N     → meses (weight=1, uniform="meses" — todas com exatamente o mesmo tamanho)
      col N+1      → TOTAL ANO (COL_TOTAL, sem stretch)
      col N+2      → A/V% (COL_AV, sem stretch)
    """
    frame = ctk.CTkFrame(parent, fg_color=fg_color, corner_radius=corner_radius)
    frame.pack(fill="x", pady=1)
    frame.columnconfigure(0, minsize=COL_NOME, weight=0)
    for c in range(1, n_meses + 1):
        frame.columnconfigure(c, weight=1, uniform="meses")
    frame.columnconfigure(n_meses + 1, minsize=COL_TOTAL, weight=0)
    frame.columnconfigure(n_meses + 2, minsize=COL_AV, weight=0)
    return frame


def _label(parent, text, col, row=0, font_size=10, bold=False, color=("gray10","gray90"),
           anchor="center", padx=4, pady=5, sticky="ew"):
    ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=font_size, weight="bold" if bold else "normal"),
        text_color=color,
        anchor=anchor,
    ).grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)


class TelaRelatorio(ctk.CTkFrame):
    def __init__(self, master, navegar):
        super().__init__(master)
        self.navegar = navegar
        self.mostrar_inativos = ctk.BooleanVar(value=False)
        self._construir()

    def _construir(self):
        header = ctk.CTkFrame(self, fg_color=CORES["header"], corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        self.btn_voltar = ctk.CTkButton(
            header,
            text="← Voltar",
            width=90, height=32,
            fg_color="transparent",
            hover_color="#2C2420",
            font=ctk.CTkFont(size=13),
            command=lambda: self.navegar("main"),
        )
        self.btn_voltar.pack(side="left", padx=16)

        ctk.CTkLabel(
            header,
            text="Relatório de Combustível",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF",
        ).pack(expand=True)

        card_ctrl = ctk.CTkFrame(self, fg_color=("gray90", "gray17"), corner_radius=12)
        card_ctrl.pack(padx=24, pady=(20, 10), fill="x")

        frame_ctrl = ctk.CTkFrame(card_ctrl, fg_color="transparent")
        frame_ctrl.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(
            frame_ctrl,
            text="ANO:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray10", "gray90"),
        ).pack(side="left", padx=(0, 10))

        self.combo_ano = ctk.CTkComboBox(
            frame_ctrl,
            values=self._listar_anos(),
            width=120, height=42,
            font=ctk.CTkFont(size=14),
            state="readonly",
        )
        self.combo_ano.pack(side="left", padx=(0, 14))
        self.combo_ano.set(str(datetime.now().year))

        self.btn_gerar = ctk.CTkButton(
            frame_ctrl, text="GERAR",
            width=100, height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=CORES["primario"], hover_color=CORES["hover"],
            command=self._gerar,
        )
        self.btn_gerar.pack(side="left", padx=(0, 8))

        self.btn_excel = ctk.CTkButton(
            frame_ctrl, text="EXPORTAR EXCEL",
            width=160, height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=CORES["sucesso"], hover_color="#059669",
            command=self._exportar_excel,
        )
        self.btn_excel.pack(side="left", padx=(0, 8))

        self.btn_imprimir = ctk.CTkButton(
            frame_ctrl, text="IMPRIMIR",
            width=110, height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#374151", hover_color="#4B5563",
            command=self._imprimir,
        )
        self.btn_imprimir.pack(side="left", padx=(0, 16))

        self.btn_historico = ctk.CTkButton(
            frame_ctrl, text="HISTÓRICO",
            width=110, height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#374151", hover_color="#4B5563",
            command=lambda: self.navegar("historico"),
        )
        self.btn_historico.pack(side="left", padx=(0, 16))

        ctk.CTkCheckBox(
            frame_ctrl,
            text="Mostrar inativos",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60"),
            variable=self.mostrar_inativos,
        ).pack(side="left")

        # ── Navegação por teclado ─────────────────────────────
        # Tab: Voltar → ANO → GERAR → EXCEL → IMPRIMIR → HISTÓRICO → Voltar
        self.btn_voltar.bind("<Tab>", lambda e: (self.combo_ano.focus_set(), "break"))
        self.btn_voltar.bind("<Return>", lambda e: self.navegar("main"))
        self.btn_voltar.bind("<FocusIn>", lambda e: self.btn_voltar.configure(fg_color="#2C2420"))
        self.btn_voltar.bind("<FocusOut>", lambda e: self.btn_voltar.configure(fg_color="transparent"))

        self.combo_ano.bind("<Tab>", lambda e: (self.btn_gerar.focus_set(), "break"))
        self.combo_ano.bind("<Down>", lambda e: self.combo_ano._open_dropdown_menu())

        self.btn_gerar.bind("<Tab>", lambda e: (self.btn_excel.focus_set(), "break"))
        self.btn_gerar.bind("<Return>", lambda e: self._gerar())
        self.btn_gerar.bind("<FocusIn>", lambda e: self.btn_gerar.configure(fg_color=CORES["hover"]))
        self.btn_gerar.bind("<FocusOut>", lambda e: self.btn_gerar.configure(fg_color=CORES["primario"]))

        self.btn_excel.bind("<Tab>", lambda e: (self.btn_imprimir.focus_set(), "break"))
        self.btn_excel.bind("<Return>", lambda e: self._exportar_excel())
        self.btn_excel.bind("<FocusIn>", lambda e: self.btn_excel.configure(fg_color="#059669"))
        self.btn_excel.bind("<FocusOut>", lambda e: self.btn_excel.configure(fg_color=CORES["sucesso"]))

        self.btn_imprimir.bind("<Tab>", lambda e: (self.btn_historico.focus_set(), "break"))
        self.btn_imprimir.bind("<Return>", lambda e: self._imprimir())
        self.btn_imprimir.bind("<FocusIn>", lambda e: self.btn_imprimir.configure(fg_color="#4B5563"))
        self.btn_imprimir.bind("<FocusOut>", lambda e: self.btn_imprimir.configure(fg_color="#374151"))

        self.btn_historico.bind("<Tab>", lambda e: (self.btn_voltar.focus_set(), "break"))
        self.btn_historico.bind("<Return>", lambda e: self.navegar("historico"))
        self.btn_historico.bind("<FocusIn>", lambda e: self.btn_historico.configure(fg_color="#4B5563"))
        self.btn_historico.bind("<FocusOut>", lambda e: self.btn_historico.configure(fg_color="#374151"))

        self.lbl_status = ctk.CTkLabel(
            card_ctrl, text="",
            font=ctk.CTkFont(size=12),
            text_color=CORES["sucesso"],
        )
        self.lbl_status.pack(pady=(0, 8))

        card_tabela = ctk.CTkFrame(self, fg_color=("gray90", "gray17"), corner_radius=12)
        card_tabela.pack(padx=24, pady=(0, 24), fill="both", expand=True)

        self.frame_tabela = ctk.CTkScrollableFrame(card_tabela, fg_color="transparent")
        self.frame_tabela.pack(fill="both", expand=True, padx=16, pady=16)

        self._mostrar_placeholder()

    def ao_exibir(self):
        if hasattr(self, '_ultimo_dados'):
            del self._ultimo_dados
        self._mostrar_placeholder()
        self.combo_ano.focus()

    def _mostrar_placeholder(self):
        for w in self.frame_tabela.winfo_children():
            w.destroy()
        ctk.CTkLabel(
            self.frame_tabela,
            text="Selecione o ano e clique em GERAR",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray60"),
        ).pack(pady=50)

    # ── Renderização ──────────────────────────────────────────────────────────

    def _renderizar_tabela(self, dados):
        for w in self.frame_tabela.winfo_children():
            w.destroy()

        if not dados:
            self._mostrar_placeholder()
            return

        # A/V% calculado UMA vez com total anual completo
        total_geral = sum(
            sum(v for v in vals if v)
            for _, _, vals in dados.get("veiculos", [])
        )
        totais_mes = dados.get("totais_mes", [0.0] * 12)
        ano = self.combo_ano.get()

        self._renderizar_bloco(dados, list(range(0, 6)),  total_geral, totais_mes, ano)
        ctk.CTkFrame(self.frame_tabela, fg_color="transparent", height=28).pack()
        self._renderizar_bloco(dados, list(range(6, 12)), total_geral, totais_mes, ano)

    def _renderizar_bloco(self, dados, meses_idx, total_geral, totais_mes, ano):
        n = len(meses_idx)  # sempre 6
        nomes = [MESES_ABREV[i] for i in meses_idx]

        # ── Título ────────────────────────────────────────────
        ctk.CTkLabel(
            self.frame_tabela,
            text=f"COMBUSTIVEL {ano} (POSTO/CAIXA)",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("gray20", "gray80"),
        ).pack(anchor="center", pady=(0, 4))

        # ── Cabeçalho ─────────────────────────────────────────
        hdr = _row_grid(self.frame_tabela, n, fg_color=CORES["header"], corner_radius=6)
        _label(hdr, "VEÍCULOS/PERÍODO", col=0, font_size=11, bold=True,
               color="#FFFFFF", anchor="w", padx=(8, 4))
        for i, mes in enumerate(nomes, start=1):
            _label(hdr, mes, col=i, font_size=11, bold=True, color="#FFFFFF", padx=0)
        _label(hdr, "TOTAL ANO", col=n+1, font_size=11, bold=True, color="#FFFFFF", padx=0)
        _label(hdr, "A/V %", col=n+2, font_size=11, bold=True, color="#FFFFFF", padx=0)

        # ── Veículos ──────────────────────────────────────────
        categoria_atual = None

        for nome, categoria, valores in dados.get("veiculos", []):

            # Separador de categoria
            if categoria != categoria_atual:
                categoria_atual = categoria
                cat = ctk.CTkFrame(self.frame_tabela, fg_color=("gray72", "gray30"), corner_radius=4)
                cat.pack(fill="x", pady=(6, 1))
                ctk.CTkLabel(
                    cat,
                    text=categoria.upper(),
                    font=ctk.CTkFont(size=10, weight="bold"),
                    text_color=("gray15", "gray85"),
                ).pack(side="left", padx=8, pady=4)

            total_veiculo = sum(v for v in valores if v)
            av_texto = f"{calcular_av(total_veiculo, total_geral):.1f}%" if total_veiculo > 0 else "-"
            av_cor   = "#60A5FA" if total_veiculo > 0 else ("gray50", "gray50")

            # Linha de valores
            row_v = _row_grid(self.frame_tabela, n, fg_color=("gray92", "gray20"))
            _label(row_v, nome, col=0, font_size=11, color=("gray10","gray90"),
                   anchor="w", padx=(8, 4), pady=5)
            for i, idx in enumerate(meses_idx, start=1):
                val = valores[idx]
                txt = (f"R$ {val:,.2f}".replace(",","X").replace(".","," ).replace("X",".")
                       if val else "-")
                _label(row_v, txt, col=i, font_size=10,
                       color=("gray10","gray90") if val else ("gray50","gray50"), pady=5, padx=0)

            total_txt = (f"R$ {total_veiculo:,.2f}".replace(",","X").replace(".","," ).replace("X",".")
                         if total_veiculo > 0 else "-")
            _label(row_v, total_txt, col=n+1, font_size=10, bold=True,
                   color=("gray10","gray90") if total_veiculo > 0 else ("gray50","gray50"), pady=5, padx=0)
            _label(row_v, av_texto, col=n+2, font_size=10, bold=True,
                   color=av_cor, pady=5, padx=0)



        # ── Separador ─────────────────────────────────────────
        ctk.CTkFrame(self.frame_tabela, fg_color=("gray75","gray35"), height=2).pack(
            fill="x", pady=(8, 2))

        # ── TOTAL MÊS ─────────────────────────────────────────
        row_t = _row_grid(self.frame_tabela, n, fg_color="#7C2D12", corner_radius=6)
        _label(row_t, "TOTAL MÊS", col=0, font_size=11, bold=True,
               color="#FFFFFF", anchor="w", padx=(8, 4), pady=7)
        for i, idx in enumerate(meses_idx, start=1):
            val = totais_mes[idx]
            txt = (f"R$ {val:,.2f}".replace(",","X").replace(".","," ).replace("X",".")
                   if val else "-")
            _label(row_t, txt, col=i, font_size=10, bold=True, color="#FFFFFF", pady=7, padx=0)

        total_ano = sum(totais_mes)
        total_ano_txt = (f"R$ {total_ano:,.2f}".replace(",","X").replace(".","," ).replace("X",".")
                         if total_ano > 0 else "-")
        _label(row_t, total_ano_txt, col=n+1, font_size=10, bold=True, color="#FFFFFF", pady=7, padx=0)
        _label(row_t, "100%", col=n+2, font_size=10, bold=True, color="#FFFFFF", pady=7, padx=0)

        # ── A/H % geral ───────────────────────────────────────
        row_ah_g = _row_grid(self.frame_tabela, n, fg_color="#1E293B", corner_radius=6)
        _label(row_ah_g, "A/H %", col=0, font_size=11, bold=True,
               color="#FFFFFF", anchor="w", padx=(8, 4), pady=6)
        for i, idx in enumerate(meses_idx, start=1):
            txt, cor = self._ah_total(totais_mes, idx)
            _label(row_ah_g, txt, col=i, font_size=10, bold=True, color=cor, pady=6, padx=0)
        _label(row_ah_g, "-", col=n+1, font_size=10, color="#FFFFFF", pady=6, padx=0)
        _label(row_ah_g, "-", col=n+2, font_size=10, color="#FFFFFF", pady=6, padx=0)

    # ── Helpers A/H ───────────────────────────────────────────────────────────

    def _ah_veiculo(self, valores, idx):
        if idx == 0:
            return "-", ("gray50", "gray50")
        val_a, val_p = valores[idx], valores[idx - 1]
        if not val_p:
            return "-", ("gray50", "gray50")
        if not val_a:
            return "-", ("gray50","gray50")
        ah = calcular_ah(val_a, val_p)
        if ah > 0:   return f"+{ah:.1f}%", "#FCA5A5"
        elif ah < 0: return f"{ah:.1f}%",  "#6EE7B7"
        return "0,0%", ("gray60", "gray50")

    def _ah_total(self, totais_mes, idx):
        if idx == 0:
            return "-", "#FFFFFF"
        val_a, val_p = totais_mes[idx], totais_mes[idx - 1]
        if not val_a:
            return "-", "#FFFFFF"
        if not val_p:
            return "-", "#FFFFFF"
        ah = calcular_ah(val_a, val_p)
        if ah > 0:   return f"+{ah:.1f}%", "#FCA5A5"
        elif ah < 0: return f"{ah:.1f}%",  "#6EE7B7"
        return "0%", "#FFFFFF"

    # ── Utilitários ───────────────────────────────────────────────────────────

    def _mostrar_status(self, msg, sucesso=True):
        cor = CORES["sucesso"] if sucesso else CORES["perigo"]
        self.lbl_status.configure(text=msg, text_color=cor)
        self.after(3000, lambda: self.lbl_status.configure(text=""))

    def _listar_anos(self):
        try:
            from database.connection import get_connection
            with get_connection() as conn:
                cursor = conn.execute(
                    "SELECT DISTINCT strftime('%Y', data) FROM abastecimentos ORDER BY 1 DESC"
                )
                anos = [row[0] for row in cursor.fetchall()]
                return anos if anos else [str(datetime.now().year)]
        except Exception:
            return [str(datetime.now().year)]

    def _gerar(self):
        ano = self.combo_ano.get()
        dados_crus = gerar_relatorio(ano, self.mostrar_inativos.get())

        if isinstance(dados_crus, dict):
            self._mostrar_status(dados_crus["message"], sucesso=False)
            return

        veiculos_dict = {}
        for nome, categoria, mes, valor in dados_crus:
            if nome not in veiculos_dict:
                veiculos_dict[nome] = {"categoria": categoria, "valores": [0.0] * 12}
            veiculos_dict[nome]["valores"][int(mes) - 1] = valor

        veiculos_lista = sorted(
            [(n, i["categoria"], i["valores"]) for n, i in veiculos_dict.items()],
            key=lambda x: (x[1], x[0])
        )

        totais_mes = [0.0] * 12
        for _, _, vals in veiculos_lista:
            for i, v in enumerate(vals):
                totais_mes[i] += v

        dados = {"veiculos": veiculos_lista, "totais_mes": totais_mes}
        self._ultimo_dados = dados
        self.after(50, lambda: self._renderizar_tabela(dados))

    def _exportar_excel(self):
        if not hasattr(self, '_ultimo_dados'):
            self._mostrar_status("Gere o relatório primeiro!", sucesso=False)
            return

        ano = self.combo_ano.get()
        caminho = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile=f"COMBUSTIVEL_{ano}_{datetime.now().strftime('%m')}.xlsx",
            title="Salvar relatório Excel"
        )
        if not caminho:
            return
        try:
            exportar_excel(self._ultimo_dados, ano, caminho)
            self._mostrar_status("Excel exportado com sucesso!")
        except Exception as e:
            self._mostrar_status(f"Erro ao exportar: {e}", sucesso=False)

    def _imprimir(self):
        if not hasattr(self, '_ultimo_dados'):
            self._mostrar_status("Gere o relatório primeiro!", sucesso=False)
            return
        try:
            caminho_xlsx = os.path.join(os.environ.get("TEMP", "/tmp"), "combustivel_temp.xlsx")
            exportar_excel(self._ultimo_dados, self.combo_ano.get(), caminho_xlsx)

            if platform.system() == "Windows":
                import win32com.client
                excel = win32com.client.Dispatch("Excel.Application")
                excel.Visible = True
                wb = excel.Workbooks.Open(caminho_xlsx)
                wb.PrintPreview()
            else:
                import subprocess
                subprocess.Popen(["xdg-open", caminho_xlsx])
                self._mostrar_status("Arquivo aberto! Use Ctrl+P para imprimir.")
        except Exception as e:
            self._mostrar_status(f"Erro ao imprimir: {e}", sucesso=False)