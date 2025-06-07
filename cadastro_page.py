# cadastro_page.py
import tkinter as tk
from tkinter import messagebox
import banco

def tela_cadastro(janela, voltar_login, abrir_menu):
    limpar_janela(janela)
    tk.Label(janela, text="Cadastro de Usuário", font=("Arial", 25, "bold")).pack(pady=20)

    tk.Label(janela, text="Nome:").pack()
    nome = tk.Entry(janela)
    nome.pack()

    tk.Label(janela, text="Sobrenome:").pack()
    sobrenome = tk.Entry(janela)
    sobrenome.pack()

    tk.Label(janela, text="Email:").pack()
    email = tk.Entry(janela)
    email.pack()

    tk.Label(janela, text="Nome de Usuário:").pack()
    usuario = tk.Entry(janela)
    usuario.pack()

    tk.Label(janela, text="Senha:").pack()
    senha = tk.Entry(janela, show="*")
    senha.pack
