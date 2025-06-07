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
    senha.pack()

    def confirmar_cadastro():
        if not (nome.get().strip() and sobrenome.get().strip() and email.get().strip() and usuario.get().strip() and senha.get().strip()):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        sucesso = banco.cadastrar_usuario(
            nome.get().strip(),
            sobrenome.get().strip(),
            email.get().strip(),
            usuario.get().strip(),
            senha.get().strip()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            voltar_login(janela, abrir_menu)
        else:
            messagebox.showerror("Erro", "Usuário já existe ou erro ao cadastrar.")

    tk.Button(janela, text="Confirmar Cadastro", width=20, command=confirmar_cadastro).pack(pady=10)
    tk.Button(janela, text="Voltar", width=20, command=lambda: voltar_login(janela, abrir_menu)).pack()

def limpar_janela(janela):
    for widget in janela.winfo_children():
        widget.destroy()
