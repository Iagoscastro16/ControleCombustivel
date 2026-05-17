import customtkinter as ctk
from database import inicializar_db
from tela_main import TelaMain

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

inicializar_db()

janela = ctk.CTk()
janela.title("Controle de Combustível")
janela.update_idletasks()
janela.minsize(500, janela.winfo_reqheight())

tela = TelaMain(janela)
tela.pack(fill="both", expand=True)

janela.mainloop()