import customtkinter as ctk 
from database import inicializar_db


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
inicializar_db()

janela = ctk.CTk()
janela.title("Controle de combustivel")
janela.mainloop()