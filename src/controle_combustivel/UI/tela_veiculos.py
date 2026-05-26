import customtkinter as ctk
from functions.veiculos import listar_veiculos, adicionar_veiculo, remover_veiculo, ativar_veiculo

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

CATEGORIAS = ["Utilitários", "Passeio", "Outros", "Diretoria"]


class TelaVeiculos(ctk.CTkFrame):
    def __init__(self, master, navegar):
        super().__init__(master)
        self.navegar = navegar
        self.mostrar_inativos = ctk.BooleanVar(value=False)
        self._construir()

    def _construir(self):
        # ── Header ───────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=CORES["header"], corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        self.btn_voltar = ctk.CTkButton(
            header,
            text="Voltar →",
            width=90,
            height=32,
            fg_color="transparent",
            hover_color="#2C2420",
            font=ctk.CTkFont(size=13),
            command=lambda: self.navegar("main"),
        )
        self.btn_voltar.pack(side="right", padx=16, pady=14)

        ctk.CTkLabel(
            header,
            text="Veículos Cadastrados",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF",
        ).pack(expand=True)

        # ── Lista de veículos ─────────────────────────────────
        card_lista = ctk.CTkFrame(self, fg_color=("gray90", "gray17"), corner_radius=12)
        card_lista.pack(padx=24, pady=(20, 10), fill="both", expand=True)

        frame_topo = ctk.CTkFrame(card_lista, fg_color="transparent")
        frame_topo.pack(fill="x", padx=16, pady=(16, 8))

        ctk.CTkLabel(
            frame_topo,
            text="Veículos",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray10", "gray90"),
        ).pack(side="left")

        ctk.CTkCheckBox(
            frame_topo,
            text="Mostrar inativos",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60"),
            variable=self.mostrar_inativos,
            command=self._atualizar_lista,
        ).pack(side="right")

        self.frame_lista = ctk.CTkScrollableFrame(
            card_lista, fg_color="transparent", height=220
        )
        self.frame_lista.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self._atualizar_lista()

        # ── Card adicionar ────────────────────────────────────
        card_add = ctk.CTkFrame(self, fg_color=("gray90", "gray17"), corner_radius=12)
        card_add.pack(padx=24, pady=(0, 24), fill="x")

        ctk.CTkLabel(
            card_add,
            text="Adicionar Veículo",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray10", "gray90"),
        ).pack(anchor="w", padx=16, pady=(16, 8))

        frame_inputs = ctk.CTkFrame(card_add, fg_color="transparent")
        frame_inputs.pack(fill="x", padx=16, pady=(0, 8))
        frame_inputs.columnconfigure(0, weight=2)
        frame_inputs.columnconfigure(1, weight=1)

        self.entry_nome = ctk.CTkEntry(
            frame_inputs,
            placeholder_text="Nome do veículo",
            height=42,
            font=ctk.CTkFont(size=13),
        )
        self.entry_nome.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.combo_categoria = ctk.CTkComboBox(
            frame_inputs,
            values=CATEGORIAS,
            height=42,
            font=ctk.CTkFont(size=13),
            state="readonly",
        )
        self.combo_categoria.grid(row=0, column=1, sticky="ew")
        self.combo_categoria.set("Categoria")

        self.lbl_feedback = ctk.CTkLabel(
            card_add,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=CORES["sucesso"],
        )
        self.lbl_feedback.pack(pady=(4, 0))

        self.btn_adicionar = ctk.CTkButton(
            card_add,
            text="ADICIONAR",
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=CORES["sucesso"],
            hover_color="#059669",
            command=self._adicionar,
        )
        self.btn_adicionar.pack(fill="x", padx=16, pady=(8, 16))

        # ── Navegação por teclado ─────────────────────────────
        # Tab: Voltar → nome → categoria → ADICIONAR → Voltar
        self.btn_voltar.bind("<Tab>", lambda e: (self.entry_nome.focus_set(), "break"))
        self.btn_voltar.bind("<Return>", lambda e: self.navegar("main"))
        self.btn_voltar.bind("<FocusIn>", lambda e: self.btn_voltar.configure(fg_color="#2C2420"))
        self.btn_voltar.bind("<FocusOut>", lambda e: self.btn_voltar.configure(fg_color="transparent"))

        self.entry_nome.bind("<Tab>", lambda e: (self.combo_categoria.focus_set(), "break"))
        self.entry_nome.bind("<Return>", lambda e: self.combo_categoria.focus_set())

        self.combo_categoria.bind("<Tab>", lambda e: (self.btn_adicionar.focus_set(), "break"))
        self.combo_categoria.bind("<Down>", lambda e: self.combo_categoria._open_dropdown_menu())

        self.btn_adicionar.bind("<Tab>", lambda e: (self.btn_voltar.focus_set(), "break"))
        self.btn_adicionar.bind("<Return>", lambda e: self._adicionar())
        self.btn_adicionar.bind("<FocusIn>", lambda e: self.btn_adicionar.configure(fg_color="#059669"))
        self.btn_adicionar.bind("<FocusOut>", lambda e: self.btn_adicionar.configure(fg_color=CORES["sucesso"]))

    def _atualizar_lista(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        veiculos = self._listar_veiculos()

        if not veiculos:
            ctk.CTkLabel(
                self.frame_lista,
                text="Nenhum veículo cadastrado",
                font=ctk.CTkFont(size=13),
                text_color=("gray40", "gray60"),
            ).pack(pady=24)
            return

        for registro in veiculos:
            if len(registro) == 4:
                id, nome, categoria, ativo = registro
            else:
                id, nome, categoria = registro
                ativo = 1

            row = ctk.CTkFrame(
                self.frame_lista,
                fg_color=("gray92", "gray20") if ativo else "#FEE2E2",
                corner_radius=8
            )
            row.pack(fill="x", pady=3)

            ctk.CTkLabel(
                row,
                text=nome,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=("gray10", "gray90") if ativo else CORES["texto_sec"],
            ).pack(side="left", padx=12, pady=10)

            ctk.CTkLabel(
                row,
                text=categoria,
                font=ctk.CTkFont(size=12),
                text_color=("gray40", "gray60"),
            ).pack(side="left", padx=(0, 8))

            if ativo:
                ctk.CTkButton(
                    row,
                    text="Remover",
                    width=76,
                    height=30,
                    font=ctk.CTkFont(size=11),
                    fg_color=CORES["perigo"],
                    hover_color="#DC2626",
                    command=lambda i=id: self._confirmar_remocao(i),
                ).pack(side="right", padx=8, pady=6)
            else:
                ctk.CTkButton(
                    row,
                    text="Ativar",
                    width=76,
                    height=30,
                    font=ctk.CTkFont(size=11),
                    fg_color=CORES["sucesso"],
                    hover_color="#059669",
                    command=lambda i=id: self._ativar(i),
                ).pack(side="right", padx=8, pady=6)

    def _confirmar_remocao(self, id):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmar remoção")
        dialog.resizable(False, False)

        dialog.update_idletasks()
        w, h = 340, 160
        x = (dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (dialog.winfo_screenheight() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")
        dialog.after(100, lambda: [dialog.grab_set(), dialog.lift(), dialog.focus_force()])

        ctk.CTkLabel(
            dialog,
            text="Deseja remover este veículo?",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=280,
        ).pack(pady=(24, 8))

        ctk.CTkLabel(
            dialog,
            text="Essa ação não pode ser desfeita.",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60"),
        ).pack()

        frame_btns = ctk.CTkFrame(dialog, fg_color="transparent")
        frame_btns.pack(pady=16)

        ctk.CTkButton(
            frame_btns,
            text="Cancelar",
            width=110,
            fg_color="#374151",
            hover_color="#4B5563",
            command=dialog.destroy,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            frame_btns,
            text="Remover",
            width=110,
            fg_color=CORES["perigo"],
            hover_color="#DC2626",
            command=lambda: [dialog.destroy(), self._remover(id)],
        ).pack(side="left", padx=6)

    def _mostrar_feedback(self, msg, sucesso=True):
        cor = CORES["sucesso"] if sucesso else CORES["perigo"]
        self.lbl_feedback.configure(text=msg, text_color=cor)
        self.after(2000, lambda: self.lbl_feedback.configure(text=""))

    def _listar_veiculos(self):
        resultado = listar_veiculos(mostrar_inativos=self.mostrar_inativos.get())
        if isinstance(resultado, list):
            return resultado
        return []

    def _adicionar(self):
        nome = self.entry_nome.get().strip()
        categoria = self.combo_categoria.get()

        if not nome or categoria == "Categoria":
            self._mostrar_feedback("Preencha todos os campos!", sucesso=False)
            return

        resultado = adicionar_veiculo(nome, categoria)
        if resultado["success"]:
            self._mostrar_feedback("Veículo adicionado!")
            self._atualizar_lista()
            self.entry_nome.delete(0, "end")
            self.combo_categoria.set("Categoria")
        else:
            self._mostrar_feedback(resultado["message"], sucesso=False)

    def _remover(self, id):
        resultado = remover_veiculo(id)
        if resultado["success"]:
            self._mostrar_feedback("Veículo removido!")
            self._atualizar_lista()
        else:
            self._mostrar_feedback(resultado["message"], sucesso=False)

    def _ativar(self, id):
        resultado = ativar_veiculo(id)
        if resultado["success"]:
            self._mostrar_feedback("Veículo reativado!")
            self._atualizar_lista()
        else:
            self._mostrar_feedback(resultado["message"], sucesso=False)
    
    def ao_exibir(self):
        self.entry_nome.focus()