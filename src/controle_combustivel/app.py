import sys
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from database.setup import inicializar_db
from UI.tela_main import TelaMain
from UI.tela_veiculos import TelaVeiculos
from UI.tela_relatorio import TelaRelatorio
from UI.tela_historico import TelaHistorico
from database.backup import fazer_backup



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

resultado_db = inicializar_db()
if not resultado_db["success"]:
    # Janela escondida só pra exibir a mensagem, já que a principal ainda não existe
    raiz = tk.Tk()
    raiz.withdraw()
    messagebox.showerror("Erro ao iniciar", resultado_db["message"])
    raiz.destroy()
    sys.exit(1)


janela = ctk.CTk()
janela.after(2000, fazer_backup)
janela.after(100, lambda: janela.state("zoomed"))
janela.title("Controle de Combustível")


telas = {}
tela_atual = None

def navegar(nome):
    global tela_atual
    if tela_atual:
        tela_atual.pack_forget()
    telas[nome].pack(fill="both", expand=True)
    tela_atual = telas[nome]

    if hasattr(tela_atual, "ao_exibir"):
        tela_atual.ao_exibir()

telas["main"]      = TelaMain(janela, navegar)
telas["veiculos"]  = TelaVeiculos(janela, navegar)
telas["relatorio"] = TelaRelatorio(janela, navegar)
telas["historico"] = TelaHistorico(janela, navegar)

navegar("main")

janela.mainloop()