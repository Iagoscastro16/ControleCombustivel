import customtkinter as ctk
from datetime import datetime
from functions.abastecimentos import listar_abastecimentos, excluir_abastecimento, editar_abastecimentos
from functions.veiculos import listar_veiculos

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


class TelaHistorico(ctk.CTkFrame):
    def __init__(self, master, navegar):
        super().__init__(master, fg_color=CORES["fundo"])
        self.navegar = navegar
        self._construir()

    def _construir(self):
        # ── Header ───────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=CORES["header"], corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Histórico de Lançamentos",
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
            command=lambda: self.navegar("relatorio"),
        ).pack(side="right", padx=16)

        # ── Filtros ───────────────────────────────────────────
        card_filtros = ctk.CTkFrame(self, fg_color=CORES["card"], corner_radius=12)
        card_filtros.pack(padx=24, pady=(20, 10), fill="x")

        frame_filtros = ctk.CTkFrame(card_filtros, fg_color="transparent")
        frame_filtros.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(
            frame_filtros,
            text="MÊS:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto"],
        ).pack(side="left", padx=(0, 8))

        self.combo_mes = ctk.CTkComboBox(
            frame_filtros,
            values=MESES,
            width=140,
            height=42,
            font=ctk.CTkFont(size=13),
            state="readonly",
        )
        self.combo_mes.pack(side="left", padx=(0, 14))
        self.combo_mes.set(MESES[datetime.now().month - 1])

        ctk.CTkLabel(
            frame_filtros,
            text="ANO:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto"],
        ).pack(side="left", padx=(0, 8))

        self.combo_ano = ctk.CTkComboBox(
            frame_filtros,
            values=self._listar_anos(),
            width=100,
            height=42,
            font=ctk.CTkFont(size=13),
            state="readonly",
        )
        self.combo_ano.pack(side="left", padx=(0, 14))
        self.combo_ano.set(str(datetime.now().year))

        ctk.CTkButton(
            frame_filtros,
            text="BUSCAR",
            width=100,
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=CORES["primario"],
            hover_color=CORES["hover"],
            command=self._buscar,
        ).pack(side="left")

        self.lbl_status = ctk.CTkLabel(
            card_filtros,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=CORES["sucesso"],
        )
        self.lbl_status.pack(pady=(0, 8))

        # ── Tabela ────────────────────────────────────────────
        card_tabela = ctk.CTkFrame(self, fg_color=CORES["card"], corner_radius=12)
        card_tabela.pack(padx=24, pady=(0, 24), fill="both", expand=True)

        # Cabeçalho fixo da tabela
        header_tabela = ctk.CTkFrame(card_tabela, fg_color=CORES["header"], corner_radius=6)
        header_tabela.pack(fill="x", padx=16, pady=(16, 2))

        for titulo, largura in [("ID", 50), ("DATA", 100), ("VEÍCULO", 300), ("VALOR", 120), ("AÇÕES", 160)]:
            ctk.CTkLabel(
                header_tabela,
                text=titulo,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#FFFFFF",
                width=largura,
                anchor="w" if titulo == "VEÍCULO" else "center",
            ).pack(side="left", padx=(8, 0), pady=6)

        self.frame_lista = ctk.CTkScrollableFrame(
            card_tabela, fg_color="transparent"
        )
        self.frame_lista.pack(fill="both", expand=True, padx=16, pady=(2, 16))

        self._mostrar_placeholder()

    def ao_exibir(self):
        self._buscar()

    def _mostrar_placeholder(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.frame_lista,
            text="Selecione o mês e ano e clique em BUSCAR",
            font=ctk.CTkFont(size=14),
            text_color=CORES["texto_sec"],
        ).pack(pady=50)

    def _buscar(self):
        mes = MESES.index(self.combo_mes.get()) + 1
        ano = self.combo_ano.get()
        resultado = listar_abastecimentos(mes, ano)

        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        if isinstance(resultado, dict):
            self._mostrar_status(resultado["message"], sucesso=False)
            return

        if not resultado:
            ctk.CTkLabel(
                self.frame_lista,
                text="Nenhum lançamento encontrado",
                font=ctk.CTkFont(size=13),
                text_color=CORES["texto_sec"],
            ).pack(pady=40)
            return

        for id, data, nome, valor in resultado:
            data_fmt = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
            valor_fmt = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            row = ctk.CTkFrame(self.frame_lista, fg_color="#F9FAFB", corner_radius=4)
            row.pack(fill="x", pady=1)

            ctk.CTkLabel(row, text=str(id), width=50, anchor="center",
                font=ctk.CTkFont(size=11), text_color=CORES["texto_sec"]).pack(side="left", padx=(8,0), pady=8)

            ctk.CTkLabel(row, text=data_fmt, width=100, anchor="center",
                font=ctk.CTkFont(size=11), text_color=CORES["texto"]).pack(side="left", padx=(8,0), pady=8)

            ctk.CTkLabel(row, text=nome, width=300, anchor="w",
                font=ctk.CTkFont(size=11), text_color=CORES["texto"]).pack(side="left", padx=(8,0), pady=8)

            ctk.CTkLabel(row, text=valor_fmt, width=120, anchor="center",
                font=ctk.CTkFont(size=11), text_color=CORES["texto"]).pack(side="left", padx=(8,0), pady=8)

            frame_acoes = ctk.CTkFrame(row, fg_color="transparent", width=160)
            frame_acoes.pack(side="left", padx=(8,8), pady=4)

            ctk.CTkButton(
                frame_acoes,
                text="Editar",
                width=70,
                height=28,
                font=ctk.CTkFont(size=11),
                fg_color=CORES["primario"],
                hover_color=CORES["hover"],
                command=lambda i=id, d=data, n=nome, v=valor: self._abrir_edicao(i, d, n, v),
            ).pack(side="left", padx=(0, 4))

            ctk.CTkButton(
                frame_acoes,
                text="Excluir",
                width=70,
                height=28,
                font=ctk.CTkFont(size=11),
                fg_color=CORES["perigo"],
                hover_color="#DC2626",
                command=lambda i=id: self._confirmar_exclusao(i),
            ).pack(side="left")

    def _confirmar_exclusao(self, id):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmar exclusão")
        dialog.resizable(False, False)

        dialog.update_idletasks()
        w, h = 340, 180
        x = (dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (dialog.winfo_screenheight() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")
        dialog.after(100, lambda: [dialog.grab_set(), dialog.lift(), dialog.focus_force()])

        ctk.CTkLabel(
            dialog,
            text="Deseja excluir este lançamento?",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=280,
        ).pack(pady=(24, 8))

        ctk.CTkLabel(
            dialog,
            text="Essa ação não pode ser desfeita.",
            font=ctk.CTkFont(size=12),
            text_color=CORES["texto_sec"],
        ).pack()

        frame_btns = ctk.CTkFrame(dialog, fg_color="transparent")
        frame_btns.pack(pady=16)

        ctk.CTkButton(
            frame_btns, text="Cancelar", width=110,
            fg_color="#374151", hover_color="#4B5563",
            command=dialog.destroy,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            frame_btns, text="Excluir", width=110,
            fg_color=CORES["perigo"], hover_color="#DC2626",
            command=lambda: [dialog.destroy(), self._excluir(id)],
        ).pack(side="left", padx=6)

    def _excluir(self, id):
        resultado = excluir_abastecimento(id)
        if resultado["success"]:
            self._mostrar_status("Lançamento excluído!")
            self._buscar()
        else:
            self._mostrar_status(resultado["message"], sucesso=False)

    def _abrir_edicao(self, id, data, nome, valor):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Editar Lançamento")
        dialog.resizable(False, False)

        dialog.update_idletasks()
        w, h = 420, 400
        x = (dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (dialog.winfo_screenheight() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")
        dialog.after(100, lambda: [dialog.grab_set(), dialog.lift(), dialog.focus_force()])

        ctk.CTkLabel(
            dialog,
            text="Editar Lançamento",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(pady=(20, 16))

        # Campo data
        frame_data = ctk.CTkFrame(dialog, fg_color="transparent")
        frame_data.pack(fill="x", padx=24, pady=(0, 10))
        ctk.CTkLabel(frame_data, text="DATA", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=CORES["texto_sec"]).pack(anchor="w")
        entry_data = ctk.CTkEntry(frame_data, height=38, font=ctk.CTkFont(size=13))
        entry_data.pack(fill="x", pady=(2, 0))
        entry_data.insert(0, datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y"))

        # Campo veículo
        frame_veiculo = ctk.CTkFrame(dialog, fg_color="transparent")
        frame_veiculo.pack(fill="x", padx=24, pady=(0, 10))
        ctk.CTkLabel(frame_veiculo, text="VEÍCULO", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=CORES["texto_sec"]).pack(anchor="w")
        veiculos = self._listar_veiculos()
        combo_veiculo = ctk.CTkComboBox(frame_veiculo, values=veiculos, height=38,
            font=ctk.CTkFont(size=13), state="readonly")
        combo_veiculo.pack(fill="x", pady=(2, 0))
        combo_veiculo.set(nome if nome in veiculos else veiculos[0])

        # Campo valor
        frame_valor = ctk.CTkFrame(dialog, fg_color="transparent")
        frame_valor.pack(fill="x", padx=24, pady=(0, 10))
        ctk.CTkLabel(frame_valor, text="VALOR (R$)", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=CORES["texto_sec"]).pack(anchor="w")
        entry_valor = ctk.CTkEntry(frame_valor, height=38, font=ctk.CTkFont(size=13))
        entry_valor.pack(fill="x", pady=(2, 0))
        entry_valor.insert(0, str(valor).replace(".", ","))

        lbl_erro = ctk.CTkLabel(dialog, text="", font=ctk.CTkFont(size=11),
            text_color=CORES["perigo"])
        lbl_erro.pack()

        def salvar():
            try:
                nova_data = datetime.strptime(entry_data.get().strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                lbl_erro.configure(text="Data inválida! Use DD/MM/AAAA")
                return

            novo_valor = entry_valor.get().strip().replace(",", ".")
            try:
                novo_valor = float(novo_valor)
            except ValueError:
                lbl_erro.configure(text="Valor inválido!")
                return

            novo_veiculo = combo_veiculo.get()
            from database.connection import get_connection
            with get_connection() as conn:
                cursor = conn.execute("SELECT id FROM veiculos WHERE nome = ?", (novo_veiculo,))
                veiculo_id = cursor.fetchone()[0]

            resultado = editar_abastecimentos(id, data=nova_data, veiculo_id=veiculo_id, valor=novo_valor)
            if resultado["success"]:
                dialog.destroy()
                self._mostrar_status("Lançamento atualizado!")
                self._buscar()
            else:
                lbl_erro.configure(text=resultado["message"])

        ctk.CTkButton(
            dialog,
            text="SALVAR",
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=CORES["sucesso"],
            hover_color="#059669",
            command=salvar,
        ).pack(fill="x", padx=24, pady=(4, 0))

    def _listar_veiculos(self):
        resultado = listar_veiculos()
        if isinstance(resultado, list):
            return [nome for id, nome, categoria in resultado]
        return []

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

    def _mostrar_status(self, msg, sucesso=True):
        cor = CORES["sucesso"] if sucesso else CORES["perigo"]
        self.lbl_status.configure(text=msg, text_color=cor)
        self.after(3000, lambda: self.lbl_status.configure(text=""))