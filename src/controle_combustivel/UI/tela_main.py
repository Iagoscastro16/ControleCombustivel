import customtkinter as ctk
from datetime import datetime
from functions.abastecimentos import inserir_abastecimento, contar_lancamentos_mes

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
    "accent":    "#F59E0B",
    "fundo":     "#F0F4F8",
}


class TelaMain(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=CORES["fundo"])
        self.master = master
        self._construir()

    def _construir(self):
        # ── Header ───────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=CORES["header"], corner_radius=0, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Controle de Combustível",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFFFFF",
        ).pack(side="left", padx=24, pady=18)

        self.lbl_contador = ctk.CTkLabel(
            header,
            text="carregando...",
            font=ctk.CTkFont(size=13),
            text_color="#9CA3AF",
        )
        self.lbl_contador.pack(side="right", padx=24)

        # ── Card central ─────────────────────────────────────
        card = ctk.CTkFrame(self, fg_color=CORES["card"], corner_radius=16)
        card.pack(padx=60, pady=40, fill="both", expand=True)

        ctk.CTkLabel(
            card,
            text="Novo Lançamento",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=CORES["texto"],
        ).pack(pady=(28, 20))

        # Campo DATA
        frame_data = ctk.CTkFrame(card, fg_color="transparent")
        frame_data.pack(fill="x", padx=40, pady=(0, 14))

        ctk.CTkLabel(
            frame_data,
            text="DATA",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=CORES["texto_sec"],
        ).pack(anchor="w")

        self.entry_data = ctk.CTkEntry(
            frame_data,
            placeholder_text="DD/MM/AAAA",
            height=44,
            font=ctk.CTkFont(size=15),
            border_color=CORES["borda"],
        )
        self.entry_data.pack(fill="x", pady=(4, 0))

        # Campo VEÍCULO
        frame_veiculo = ctk.CTkFrame(card, fg_color="transparent")
        frame_veiculo.pack(fill="x", padx=40, pady=(0, 14))

        ctk.CTkLabel(
            frame_veiculo,
            text="VEÍCULO",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=CORES["texto_sec"],
        ).pack(anchor="w")

        self.combo_veiculo = ctk.CTkComboBox(
            frame_veiculo,
            values=self._listar_veiculos(),
            height=44,
            font=ctk.CTkFont(size=15),
            state="readonly",
        )
        self.combo_veiculo.pack(fill="x", pady=(4, 0))
        self.combo_veiculo.set("Selecione o veículo...")

        # Campo VALOR
        frame_valor = ctk.CTkFrame(card, fg_color="transparent")
        frame_valor.pack(fill="x", padx=40, pady=(0, 20))

        ctk.CTkLabel(
            frame_valor,
            text="VALOR (R$)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=CORES["texto_sec"],
        ).pack(anchor="w")

        self.entry_valor = ctk.CTkEntry(
            frame_valor,
            placeholder_text="0,00",
            height=44,
            font=ctk.CTkFont(size=15),
            border_color=CORES["borda"],
        )
        self.entry_valor.pack(fill="x", pady=(4, 0))

        # Label de feedback inline (não modal)
        self.lbl_feedback = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=CORES["sucesso"],
        )
        self.lbl_feedback.pack(pady=(0, 6))

        # Botão LANÇAR
        ctk.CTkButton(
            card,
            text="LANÇAR",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=CORES["primario"],
            hover_color=CORES["hover"],
            command=self._lancar,
        ).pack(fill="x", padx=40, pady=(0, 14))

        # Botões secundários
        frame_btns = ctk.CTkFrame(card, fg_color="transparent")
        frame_btns.pack(fill="x", padx=40, pady=(0, 28))
        frame_btns.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            frame_btns,
            text="VEÍCULOS",
            height=42,
            font=ctk.CTkFont(size=13),
            fg_color="#374151",
            hover_color="#4B5563",
            command=self._abrir_veiculos,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            frame_btns,
            text="RELATÓRIO",
            height=42,
            font=ctk.CTkFont(size=13),
            fg_color="#374151",
            hover_color="#4B5563",
            command=self._abrir_relatorio,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        # Atualiza contador ao abrir
        self._atualizar_contador()

    # ── Helpers de UI ────────────────────────────────────────

    def _mostrar_feedback(self, msg, sucesso=True):
        cor = CORES["sucesso"] if sucesso else CORES["perigo"]
        self.lbl_feedback.configure(text=msg, text_color=cor)
        self.after(2000, lambda: self.lbl_feedback.configure(text=""))

    def _limpar_campos(self):
        self.entry_data.delete(0, "end")
        self.entry_valor.delete(0, "end")
        self.combo_veiculo.set("Selecione o veículo...")
        self.entry_data.focus()

    def _atualizar_contador(self):
        qtd = self._contar_lancamentos_mes()
        self.lbl_contador.configure(text=f"{qtd} lançamentos este mês")

    def _abrir_veiculos(self):
        from UI.tela_veiculos import TelaVeiculos
        TelaVeiculos(self.master)

    def _abrir_relatorio(self):
        from UI.tela_relatorio import TelaRelatorio
        TelaRelatorio(self.master)

    # ── Backend — construir junto ─────────────────────────────

    def _listar_veiculos(self):
       from functions.veiculos import listar_veiculos
       resultado = listar_veiculos()
       if isinstance(resultado,list):
            return [nome for nome, categoria in resultado]
            return []

    def _contar_lancamentos_mes(self):
        resultado = contar_lancamentos_mes()
        if isinstance(resultado,int):
            return resultado
        return 0

    def _lancar(self):
        data   = self.entry_data.get().strip()
        veiculo = self.combo_veiculo.get()
        valor  = self.entry_valor.get().strip()
        
        if not data or not valor or veiculo == "Selecione o veiculo...":
            self._mostrar_feedback("Preencha todos os campos!", sucesso=False)
            return
        try:
            data_banco = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
        
        except ValueError:
            self._mostrar_feedback("Data Inválida! Use DD/MM/AAAA", sucesso=False)
            return
        
        valor_float = float(valor.replace(",","."))
        
        resultado = inserir_abastecimento(data_banco,veiculo,valor_float)
        
        if resultado["success"]:
            self._mostrar_feedback("Lançamento Registrado!")
            self._limpar_campos()
            self._atualizar_contador()
        else:
            self._mostrar_feedback(resultado["message"], sucesso=False)