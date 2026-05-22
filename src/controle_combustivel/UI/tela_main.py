import customtkinter as ctk
from datetime import datetime
from functions.veiculos import listar_veiculos
from functions.abastecimentos import inserir_abastecimento, contar_lancamentos_mes
from functions.utils import normalizar_data

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
    "accent":    "#FED7AA",
    "fundo":     "#F0F4F8",
}


class TelaMain(ctk.CTkFrame):
    def __init__(self, master, navegar):
        super().__init__(master)
        self.navegar = navegar
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
        ).pack(expand=True)

        self.lbl_contador = ctk.CTkLabel(
            header,
            text="carregando...",
            font=ctk.CTkFont(size=13),
            text_color="#9CA3AF",
        )
        self.lbl_contador.pack(side="right", padx=24)

        # ── Card central ─────────────────────────────────────
        card = ctk.CTkFrame(self, fg_color=("gray90", "gray17"), corner_radius=16)
        card.pack(padx=60, pady=40, fill="both", expand=True)

        ctk.CTkLabel(
            card,
            text="Novo Lançamento",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("gray10", "gray90"),
        ).pack(pady=(28, 20))

        # Campo DATA
        frame_data = ctk.CTkFrame(card, fg_color="transparent")
        frame_data.pack(fill="x", padx=40, pady=(0, 14))

        ctk.CTkLabel(
            frame_data,
            text="DATA",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray40", "gray60"),
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
            text_color=("gray40", "gray60"),
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
            text_color=("gray40", "gray60"),
        ).pack(anchor="w")

        self.entry_valor = ctk.CTkEntry(
            frame_valor,
            placeholder_text="0,00",
            height=44,
            font=ctk.CTkFont(size=15),
            border_color=CORES["borda"],
        )
        self.entry_valor.pack(fill="x", pady=(4, 0))

        # Label de feedback inline
        self.lbl_feedback = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=CORES["sucesso"],
        )
        self.lbl_feedback.pack(pady=(0, 6))

        # Botão LANÇAR
        self.btn_lancar = ctk.CTkButton(
            card,
            text="LANÇAR",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=CORES["primario"],
            hover_color=CORES["hover"],
            command=self._lancar,
        )
        self.btn_lancar.pack(fill="x", padx=40, pady=(0, 14))

        # Botões secundários
        frame_btns = ctk.CTkFrame(card, fg_color="transparent")
        frame_btns.pack(fill="x", padx=40, pady=(0, 28))
        frame_btns.columnconfigure((0, 1), weight=1)

        self.btn_veiculos = ctk.CTkButton(
            frame_btns,
            text="VEÍCULOS",
            height=42,
            font=ctk.CTkFont(size=13),
            fg_color="#374151",
            hover_color="#4B5563",
            command=lambda: self.navegar("veiculos"),
        )
        self.btn_veiculos.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        self.btn_relatorio = ctk.CTkButton(
            frame_btns,
            text="RELATÓRIO",
            height=42,
            font=ctk.CTkFont(size=13),
            fg_color="#374151",
            hover_color="#4B5563",
            command=lambda: self.navegar("relatorio"),
        )
        self.btn_relatorio.grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self._atualizar_contador()

        # ── Navegação por teclado ─────────────────────────────
        # Tab: data → veículo → valor → LANÇAR → VEÍCULOS → RELATÓRIO → data
        self.entry_data.bind("<Tab>", lambda e: (self.combo_veiculo.focus_set(), "break"))
        self.entry_data.bind("<Return>", lambda e: self.combo_veiculo.focus_set())

        self.combo_veiculo.bind("<Tab>", lambda e: (self.entry_valor.focus_set(), "break"))
        self.combo_veiculo.bind("<Down>", lambda e: self.combo_veiculo._open_dropdown_menu())

        self.entry_valor.bind("<Tab>", lambda e: (self.btn_lancar.focus_set(), "break"))
        self.entry_valor.bind("<Return>", lambda e: self._lancar())

        self.btn_lancar.bind("<Tab>", lambda e: (self.btn_veiculos.focus_set(), "break"))
        self.btn_lancar.bind("<Return>", lambda e: self._lancar())
        self.btn_lancar.bind("<FocusIn>", lambda e: self.btn_lancar.configure(fg_color=CORES["hover"]))
        self.btn_lancar.bind("<FocusOut>", lambda e: self.btn_lancar.configure(fg_color=CORES["primario"]))

        self.btn_veiculos.bind("<Tab>", lambda e: (self.btn_relatorio.focus_set(), "break"))
        self.btn_veiculos.bind("<Return>", lambda e: self.navegar("veiculos"))
        self.btn_veiculos.bind("<FocusIn>", lambda e: self.btn_veiculos.configure(fg_color="#4B5563"))
        self.btn_veiculos.bind("<FocusOut>", lambda e: self.btn_veiculos.configure(fg_color="#374151"))

        self.btn_relatorio.bind("<Tab>", lambda e: (self.entry_data.focus_set(), "break"))
        self.btn_relatorio.bind("<Return>", lambda e: self.navegar("relatorio"))
        self.btn_relatorio.bind("<FocusIn>", lambda e: self.btn_relatorio.configure(fg_color="#4B5563"))
        self.btn_relatorio.bind("<FocusOut>", lambda e: self.btn_relatorio.configure(fg_color="#374151"))

    def ao_exibir(self):
        self.combo_veiculo.configure(values=self._listar_veiculos())
        self.combo_veiculo.set("Selecione o veículo...")
        self._atualizar_contador()
        self.entry_data.focus()

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

    def _listar_veiculos(self):
        resultado = listar_veiculos()
        if isinstance(resultado, list):
            return [nome for id, nome, categoria in resultado]
        return []

    def _contar_lancamentos_mes(self):
        resultado = contar_lancamentos_mes()
        if isinstance(resultado, int):
            return resultado
        return 0

    def _lancar(self):
        data = self.entry_data.get().strip()
        veiculo = self.combo_veiculo.get()
        valor = self.entry_valor.get().strip()

        if not data or not valor or veiculo == "Selecione o veículo...":
            self._mostrar_feedback("Preencha todos os campos!", sucesso=False)
            return

        data_banco = normalizar_data(data)
        if data_banco is None:
            self._mostrar_feedback("Data inválida! Use DD/MM/AA", sucesso=False)
            return

        valor_float = float(valor.replace(",", "."))
        resultado = inserir_abastecimento(data_banco, veiculo, valor_float)

        if resultado["success"]:
            self._mostrar_feedback("Lançamento registrado!")
            self._limpar_campos()
            self._atualizar_contador()
        else:
            self._mostrar_feedback(resultado["message"], sucesso=False)