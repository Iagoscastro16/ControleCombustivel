import customtkinter as ctk

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

CATEGORIAS = ["Utilitários", "Passeio", "Outros", "Diretoria"]


class TelaVeiculos(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Veículos Cadastrados")
        self.geometry("620x620")
        self.after(100, self.grab_set)
        self._construir()

    def _construir(self):
        # ── Header ───────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=CORES["header"], corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Veículos Cadastrados",
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

        # ── Lista de veículos ─────────────────────────────────
        card_lista = ctk.CTkFrame(self, fg_color=CORES["card"], corner_radius=12)
        card_lista.pack(padx=24, pady=(20, 10), fill="both", expand=True)

        ctk.CTkLabel(
            card_lista,
            text="Veículos",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto"],
        ).pack(anchor="w", padx=16, pady=(16, 8))

        self.frame_lista = ctk.CTkScrollableFrame(
            card_lista, fg_color="transparent", height=220
        )
        self.frame_lista.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self._atualizar_lista()

        # ── Card adicionar ────────────────────────────────────
        card_add = ctk.CTkFrame(self, fg_color=CORES["card"], corner_radius=12)
        card_add.pack(padx=24, pady=(0, 24), fill="x")

        ctk.CTkLabel(
            card_add,
            text="Adicionar Veículo",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CORES["texto"],
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

        ctk.CTkButton(
            card_add,
            text="ADICIONAR",
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=CORES["sucesso"],
            hover_color="#059669",
            command=self._adicionar,
        ).pack(fill="x", padx=16, pady=(8, 16))

    # ── Helpers de UI ────────────────────────────────────────

    def _atualizar_lista(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        veiculos = self._listar_veiculos()

        if not veiculos:
            ctk.CTkLabel(
                self.frame_lista,
                text="Nenhum veículo cadastrado",
                font=ctk.CTkFont(size=13),
                text_color=CORES["texto_sec"],
            ).pack(pady=24)
            return

        for nome, categoria in veiculos:
            row = ctk.CTkFrame(self.frame_lista, fg_color="#F9FAFB", corner_radius=8)
            row.pack(fill="x", pady=3)

            ctk.CTkLabel(
                row,
                text=nome,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=CORES["texto"],
            ).pack(side="left", padx=12, pady=10)

            ctk.CTkLabel(
                row,
                text=categoria,
                font=ctk.CTkFont(size=12),
                text_color=CORES["texto_sec"],
            ).pack(side="left", padx=(0, 8))

            ctk.CTkButton(
                row,
                text="Remover",
                width=76,
                height=30,
                font=ctk.CTkFont(size=11),
                fg_color=CORES["perigo"],
                hover_color="#DC2626",
                command=lambda n=nome: self._confirmar_remocao(n),
            ).pack(side="right", padx=8, pady=6)

    def _confirmar_remocao(self, nome):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmar remoção")
        dialog.geometry("340x160")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=f'Remover "{nome}"?',
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
            command=lambda: [dialog.destroy(), self._remover(nome)],
        ).pack(side="left", padx=6)

    def _mostrar_feedback(self, msg, sucesso=True):
        cor = CORES["sucesso"] if sucesso else CORES["perigo"]
        self.lbl_feedback.configure(text=msg, text_color=cor)
        self.after(2000, lambda: self.lbl_feedback.configure(text=""))

    # ── Backend — construir junto ─────────────────────────────

    def _listar_veiculos(self):
        # TODO: SELECT nome, categoria FROM veiculos ORDER BY categoria, nome
        return []

    def _adicionar(self):
        nome = self.entry_nome.get().strip()
        categoria = self.combo_categoria.get()

        # TODO: validar campos não vazios e categoria selecionada
        # TODO: INSERT INTO veiculos (nome, categoria) VALUES (?, ?)
        # TODO: self._atualizar_lista()
        # TODO: self._mostrar_feedback("Veículo adicionado!")
        # TODO: limpar campos
        pass

    def _remover(self, nome):
        # TODO: DELETE FROM veiculos WHERE nome = ?
        # TODO: self._atualizar_lista()
        # TODO: self._mostrar_feedback("Veículo removido!")
        pass