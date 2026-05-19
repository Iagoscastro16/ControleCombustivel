import customtkinter as ctk
from database.setup import inicializar_db
from UI.tela_main import TelaMain
from UI.tela_veiculos import TelaVeiculos
from UI.tela_relatorio import TelaRelatorio

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

inicializar_db()

janela = ctk.CTk()
janela.title("Controle de Combustível")
janela.state("zoomed")  # abre maximizado no Windows

telas = {}
tela_atual = None

def navegar(nome):
    global tela_atual
    if tela_atual:
        tela_atual.pack_forget()
    telas[nome].pack(fill="both", expand=True)
    tela_atual = telas[nome]

telas["main"]      = TelaMain(janela, navegar)
telas["veiculos"]  = TelaVeiculos(janela, navegar)
telas["relatorio"] = TelaRelatorio(janela, navegar)

navegar("main")

janela.mainloop()