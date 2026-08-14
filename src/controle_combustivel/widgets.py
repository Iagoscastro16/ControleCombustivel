"""
Widgets reutilizáveis entre as telas — evita duplicação de diálogos
que se repetem (confirmação de ação, por exemplo).
"""
import customtkinter as ctk
from theme import CORES


def confirmar_acao(master, titulo, mensagem, funcao_sim, texto_botao="Confirmar",
                    cor_botao=None):
    """
    Abre um diálogo modal de confirmação genérico.

    Parâmetros:
        master       — widget pai (geralmente a tela atual, self)
        titulo       — texto principal em negrito (ex: "Deseja excluir este veículo?")
        mensagem     — texto secundário menor (ex: "Essa ação não pode ser desfeita.")
        funcao_sim   — função chamada se o usuário confirmar (sem argumentos)
        texto_botao  — texto do botão de confirmação (padrão "Confirmar")
        cor_botao    — cor do botão de confirmação (padrão CORES["perigo"])

    Uso:
        confirmar_acao(
            self,
            titulo="Deseja excluir este lançamento?",
            mensagem="Essa ação não pode ser desfeita.",
            funcao_sim=lambda: self._excluir(id),
        )
    """
    cor_botao = cor_botao or CORES["perigo"]

    dialog = ctk.CTkToplevel(master)
    dialog.title("Confirmação")
    dialog.resizable(False, False)

    dialog.update_idletasks()
    w, h = 340, 180
    x = (dialog.winfo_screenwidth() // 2) - (w // 2)
    y = (dialog.winfo_screenheight() // 2) - (h // 2)
    dialog.geometry(f"{w}x{h}+{x}+{y}")
    dialog.after(100, lambda: [dialog.grab_set(), dialog.lift(), dialog.focus_force()])

    ctk.CTkLabel(
        dialog,
        text=titulo,
        font=ctk.CTkFont(size=14, weight="bold"),
        wraplength=280,
    ).pack(pady=(24, 8))

    ctk.CTkLabel(
        dialog,
        text=mensagem,
        font=ctk.CTkFont(size=12),
        text_color=("gray40", "gray60"),
    ).pack()

    frame_btns = ctk.CTkFrame(dialog, fg_color="transparent")
    frame_btns.pack(pady=16)

    ctk.CTkButton(
        frame_btns, text="Cancelar", width=110,
        fg_color="#374151", hover_color="#4B5563",
        command=dialog.destroy,
    ).pack(side="left", padx=6)

    ctk.CTkButton(
        frame_btns, text=texto_botao, width=110,
        fg_color=cor_botao, hover_color="#DC2626" if cor_botao == CORES["perigo"] else CORES["hover"],
        command=lambda: [dialog.destroy(), funcao_sim()],
    ).pack(side="left", padx=6)

    return dialog