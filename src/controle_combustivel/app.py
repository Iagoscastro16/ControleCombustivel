import customtkinter as ctk
from database.setup import inicializar_db
from UI.tela_main import TelaMain
from UI.tela_veiculos import TelaVeiculos
from UI.tela_relatorio import TelaRelatorio
from UI.tela_historico import TelaHistorico
from database.backup import fazer_backup



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

inicializar_db()

fazer_backup()


janela = ctk.CTk()
janela.title("Controle de Combustível")
janela.after(100, lambda: janela.state("zoomed"))

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