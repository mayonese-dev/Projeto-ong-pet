import tkinter as tk
from tkinter import messagebox
import banco
import cadastro_page

def tela_login(janela, abrir_menu):
    def login():
        nome_usuario = entrada_usuario.get()
        senha = entrada_senha.get()
        if nome_usuario and senha:
            nome_real = banco.validar_login(nome_usuario, senha)
            if nome_real:
                abrir_menu(nome_usuario)
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

    def suporte():
        messagebox.showinfo("Esqueceu a Senha", "Contate o suporte online.")

    limpar_janela(janela)
    tk.Label(janela, text="Login", font=("Arial", 25, "bold")).pack(pady=20)

    tk.Label(janela, text="Nome de Usuário:").pack()
    entrada_usuario = tk.Entry(janela)
    entrada_usuario.pack()

    tk.Label(janela, text="Senha:").pack()
    entrada_senha = tk.Entry(janela, show="*")
    entrada_senha.pack()

    tk.Button(janela, text="Entrar", width=15, command=login).pack(pady=10)
    tk.Button(janela, text="Cadastrar", width=15, command=lambda: cadastro_page.tela_cadastro(janela, tela_login, abrir_menu)).pack()
    tk.Button(janela, text="Esqueceu a senha?", width=20, fg="black", command=suporte).pack(pady=10)

def limpar_janela(janela):
    for widget in janela.winfo_children():
        widget.destroy()
