import os
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog
from functions.relatorio import gerar_relatorio

CORES = {
    "header":    "#1A1A2E",
    "primario":  "#4F46E5",
    "hover":     "#4338CA",
    "sucesso":   "#10B981",
    "perigo":    "#EF4444",
    "texto":     "#1F2937",
    "texto_sec": "#6B7280",
    "borda":     "#D1D5DB",
    "card":      "#FFFFFF",
    "fundo":     "#F0F4F8",
}

MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro",
]


class TelaRelatorio(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Relatório de Combustível")
        self.geometry("960x720")
        self.resizable(True, True)
        self.after(100, self.grab_set)
        self._ultimo_excel = None
        self._construir()

    def _construir(self):
        header = ctk.CTkFrame(self, fg_color=CORES["header"], corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Relatório de Combustível",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF",
        ).pack(side="left", padx=24, pady=16)

        ctk.CTkButton(
            header,
            text="← Voltar",
            width=90,
            height=32,
            fg_color="transparent",
            hover_color="#2D2D4E",
            font=ctk.CTkFont(size=13),
            command=self.destroy,
        ).pack(side="right", padx=16)

        card_ctrl = ctk.CTkFrame(self, fg_color=CORES["card"], corner_radius=12)
        card_ctrl.pack(padx=24, pady=(20, 10), fill="x")

        frame_ctrl = ctk.CTkFrame(card_ctrl, fg_color="transparent")
        frame_ctrl.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(
            frame_ctrl,
            text="ANO:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto"],
        ).pack(side="left", padx=(0, 10))

        self.combo_ano = ctk.CTkComboBox(
            frame_ctrl,
            values=self._listar_anos(),
            width=120,
            height=42,
            font=ctk.CTkFont(size=14),
            state="readonly",
        )
        self.combo_ano.pack(side="left", padx=(0, 14))
        self.combo_ano.set(str(datetime.now().year))

        ctk.CTkButton(
            frame_ctrl,
            text="GERAR",
            width=100,
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=CORES["primario"],
            hover_color=CORES["hover"],
            command=self._gerar,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            frame_ctrl,
            text="EXPORTAR EXCEL",
            width=160,
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=CORES["sucesso"],
            hover_color="#059669",
            command=self._exportar_excel,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            frame_ctrl,
            text="IMPRIMIR",
            width=110,
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#374151",
            hover_color="#4B5563",
            command=self._imprimir,
        ).pack(side="left")

        self.lbl_status = ctk.CTkLabel(
            card_ctrl,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=CORES["sucesso"],
        )
        self.lbl_status.pack(pady=(0, 8))

        card_tabela = ctk.CTkFrame(self, fg_color=CORES["card"], corner_radius=12)
        card_tabela.pack(padx=24, pady=(0, 24), fill="both", expand=True)

        self.frame_tabela = ctk.CTkScrollableFrame(
            card_tabela, fg_color="transparent"
        )
        self.frame_tabela.pack(fill="both", expand=True, padx=16, pady=16)
        self.frame_tabela.bind_all("<Button-4>", self._scroll_up)
        self.frame_tabela.bind_all("<Button-5>", self._scroll_down)

        self._mostrar_placeholder()

    def _scroll_up(self, event):
        try:
            self.frame_tabela._parent_canvas.yview_scroll(-1, "units")
        except Exception:
            pass

    def _scroll_down(self, event):
        try:
            self.frame_tabela._parent_canvas.yview_scroll(1, "units")
        except Exception:
            pass

    def _mostrar_placeholder(self):
        for widget in self.frame_tabela.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.frame_tabela,
            text="Selecione o ano e clique em GERAR",
            font=ctk.CTkFont(size=14),
            text_color=CORES["texto_sec"],
        ).pack(pady=50)

    def _renderizar_tabela(self, dados):
        for widget in self.frame_tabela.winfo_children():
            widget.destroy()

        if not dados:
            self._mostrar_placeholder()
            return

        header_frame = ctk.CTkFrame(self.frame_tabela, fg_color=CORES["header"], corner_radius=6)
        header_frame.pack(fill="x", pady=(0, 2))
        header_frame.columnconfigure(0, weight=3)
        for i in range(12):
            header_frame.columnconfigure(i + 1, weight=1)

        ctk.CTkLabel(
            header_frame,
            text="VEÍCULO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#FFFFFF",
        ).grid(row=0, column=0, padx=8, pady=6, sticky="w")

        for i, mes in enumerate(MESES):
            ctk.CTkLabel(
                header_frame,
                text=mes[:3].upper(),
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#FFFFFF",
            ).grid(row=0, column=i + 1, padx=4, pady=6)

        categoria_atual = None
        for nome, categoria, valores in dados.get("veiculos", []):
            if categoria != categoria_atual:
                categoria_atual = categoria
                sep = ctk.CTkFrame(self.frame_tabela, fg_color="#E5E7EB", corner_radius=0, height=2)
                sep.pack(fill="x", pady=(8, 2))
                ctk.CTkLabel(
                    self.frame_tabela,
                    text=categoria.upper(),
                    font=ctk.CTkFont(size=10, weight="bold"),
                    text_color=CORES["texto_sec"],
                ).pack(anchor="w", padx=8, pady=(2, 0))

            row = ctk.CTkFrame(self.frame_tabela, fg_color="#F9FAFB", corner_radius=4)
            row.pack(fill="x", pady=1)
            row.columnconfigure(0, weight=3)
            for i in range(12):
                row.columnconfigure(i + 1, weight=1)

            ctk.CTkLabel(
                row,
                text=nome,
                font=ctk.CTkFont(size=12),
                text_color=CORES["texto"],
                anchor="w",
            ).grid(row=0, column=0, padx=8, pady=6, sticky="w")

            for i, val in enumerate(valores):
                texto = f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if val else "-"
                ctk.CTkLabel(
                    row,
                    text=texto,
                    font=ctk.CTkFont(size=11),
                    text_color=CORES["texto"] if val else CORES["texto_sec"],
                ).grid(row=0, column=i + 1, padx=4, pady=6)

        total_frame = ctk.CTkFrame(self.frame_tabela, fg_color="#375623", corner_radius=6)
        total_frame.pack(fill="x", pady=(8, 0))
        total_frame.columnconfigure(0, weight=3)
        for i in range(12):
            total_frame.columnconfigure(i + 1, weight=1)

        ctk.CTkLabel(
            total_frame,
            text="TOTAL MÊS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#FFFFFF",
        ).grid(row=0, column=0, padx=8, pady=8, sticky="w")

        for i, val in enumerate(dados.get("totais_mes", [0] * 12)):
            texto = f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if val else "-"
            ctk.CTkLabel(
                total_frame,
                text=texto,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#FFFFFF",
            ).grid(row=0, column=i + 1, padx=4, pady=8)

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
        dados_crus = gerar_relatorio(ano)

        if isinstance(dados_crus, dict):
            self._mostrar_status(dados_crus["message"], sucesso=False)
            return

        veiculos_dict = {}
        for nome, categoria, mes, valor in dados_crus:
            if nome not in veiculos_dict:
                veiculos_dict[nome] = {
                    "categoria": categoria,
                    "valores": [0.0] * 12
                }
            indice = int(mes) - 1
            veiculos_dict[nome]["valores"][indice] = valor

        veiculos_lista = sorted(
            [(nome, info["categoria"], info["valores"]) for nome, info in veiculos_dict.items()],
            key=lambda x: (x[1], x[0])
        )

        totais_mes = [0.0] * 12
        for _, _, valores in veiculos_lista:
            for i, val in enumerate(valores):
                totais_mes[i] += val

        dados = {
            "veiculos": veiculos_lista,
            "totais_mes": totais_mes
        }

        self._ultimo_dados = dados
        self._renderizar_tabela(dados)

    def _exportar_excel(self):
        if not hasattr(self, '_ultimo_dados'):
            self._mostrar_status("Gere o relatório primeiro!", sucesso=False)
            return

        ano = self.combo_ano.get()
        mes_atual = datetime.now().strftime("%m")

        caminho = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile=f"COMBUSTIVEL_{ano}_{mes_atual}.xlsx",
            title="Salvar relatório Excel"
        )

        if not caminho:
            return

        try:
            from functions.relatorio import exportar_excel
            exportar_excel(self._ultimo_dados, ano, caminho)
            self._ultimo_excel = caminho
            self._mostrar_status("Excel exportado com sucesso!")
        except Exception as e:
            self._mostrar_status(f"Erro ao exportar: {e}", sucesso=False)

    def _imprimir(self):
        if not self._ultimo_excel:
            self._mostrar_status("Exporte o Excel primeiro!", sucesso=False)
            return

        try:
            os.startfile(self._ultimo_excel, "print")
        except Exception as e:
            self._mostrar_status(f"Erro ao imprimir: {e}", sucesso=False)