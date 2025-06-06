import tkinter as tk
from tkinter import messagebox
import banco
import os
from datetime import datetime

os.makedirs("relatorios", exist_ok=True)
banco.criar_tabela_animais()
banco.criar_tabela_usuarios()

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

def abrir_menu(nome_usuario):
    limpar_janela()
    tk.Label(janela, text=f"🐾 Bem-vindo, {nome_usuario}!", font=("Arial", 20, "bold")).pack(pady=15)

    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM animais")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM animais WHERE situacao='Adotado'")
    adotados = cursor.fetchone()[0]
    conn.close()

    tk.Label(janela, text=f"📋 Animais cadastrados: {total}", font=("Arial", 12)).pack()
    tk.Label(janela, text=f"🏠 Já adotados: {adotados}", font=("Arial", 12)).pack(pady=(0, 20))

    tk.Button(janela, text="➕ Cadastrar Animal", width=20, command=cadastrar).pack(pady=5)
    tk.Button(janela, text="📄 Ver Animais", width=20, command=ver_animais).pack(pady=5)
    tk.Button(janela, text="📝 Gerar Relatório", width=20, command=relatorio).pack(pady=5)
    tk.Button(janela, text="Logout", width=20, command=tela_login).pack(pady=20)

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    tk.Label(janela, text=f"Acesso em: {agora}", font=("Arial", 10), fg="gray").pack(side="bottom", pady=10)

def cadastrar():
    limpar_janela()
    tk.Label(janela, text="Nome:").pack()
    nome = tk.Entry(janela)
    nome.pack()

    tk.Label(janela, text="Espécie:").pack()
    especie = tk.Entry(janela)
    especie.pack()

    tk.Label(janela, text="Idade:").pack()
    idade = tk.Entry(janela)
    idade.pack()

    tk.Label(janela, text="Situação:").pack()
    situacao = tk.StringVar()
    situacao.set("Disponível")
    tk.OptionMenu(janela, situacao, "Disponível", "Adotado").pack()

    def salvar():
        if not (nome.get().strip() and especie.get().strip() and idade.get().strip()):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        if not idade.get().isdigit():
            messagebox.showerror("Erro", "Idade deve ser um número.")
            return

        conn = banco.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO animais (nome, especie, idade, situacao) VALUES (?, ?, ?, ?)",
            (nome.get().strip(), especie.get().strip(), int(idade.get().strip()), situacao.get())
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Animal cadastrado!")
        abrir_menu("Usuário")

    tk.Button(janela, text="Salvar", width=15, command=salvar).pack(pady=5)
    tk.Button(janela, text="Voltar", width=15, command=lambda: abrir_menu("Usuário")).pack(pady=5)

def ver_animais():
    limpar_janela()
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animais")
    dados = cursor.fetchall()
    conn.close()

    for animal in dados:
        texto = f"ID: {animal[0]} | {animal[1]} - {animal[2]} ({animal[3]} anos) | Situação: {animal[4]}"
        tk.Label(janela, text=texto).pack()

    tk.Label(janela, text="Digite o ID para Editar ou Remover:").pack(pady=10)
    id_entrada = tk.Entry(janela)
    id_entrada.pack()

    def editar():
        editar_animal(id_entrada.get())

    def remover():
        id_animal = id_entrada.get()
        if not id_animal.isdigit():
            messagebox.showerror("Erro", "ID inválido.")
            return

        confirmacao = messagebox.askyesno("Confirmar Remoção", "Tem certeza que deseja remover este animal?")
        if confirmacao:
            conn = banco.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM animais WHERE id=?", (int(id_animal),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Removido", "Animal removido.")
            ver_animais()

    tk.Button(janela, text="Editar", width=15, command=editar).pack(pady=5)
    tk.Button(janela, text="Remover", width=15, command=remover).pack(pady=5)
    tk.Button(janela, text="Voltar", width=15, command=lambda: abrir_menu("Usuário")).pack(pady=5)

def editar_animal(id_animal):
    limpar_janela()
    if not id_animal.isdigit():
        messagebox.showerror("Erro", "ID inválido.")
        ver_animais()
        return

    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animais WHERE id=?", (int(id_animal),))
    animal = cursor.fetchone()
    conn.close()

    if not animal:
        messagebox.showerror("Erro", "ID não encontrado.")
        ver_animais()
        return

    tk.Label(janela, text="Editar Nome:").pack()
    nome = tk.Entry(janela)
    nome.insert(0, animal[1])
    nome.pack()

    tk.Label(janela, text="Editar Espécie:").pack()
    especie = tk.Entry(janela)
    especie.insert(0, animal[2])
    especie.pack()

    tk.Label(janela, text="Editar Idade:").pack()
    idade = tk.Entry(janela)
    idade.insert(0, str(animal[3]))
    idade.pack()

    tk.Label(janela, text="Editar Situação:").pack()
    situacao = tk.StringVar()
    situacao.set(animal[4])
    tk.OptionMenu(janela, situacao, "Disponível", "Adotado").pack()

    def salvar():
        if not (nome.get().strip() and especie.get().strip() and idade.get().strip()):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        if not idade.get().isdigit():
            messagebox.showerror("Erro", "Idade deve ser um número.")
            return

        conn = banco.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE animais SET nome=?, especie=?, idade=?, situacao=? WHERE id=?",
            (nome.get().strip(), especie.get().strip(), int(idade.get().strip()), situacao.get(), int(id_animal))
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Salvo", "Animal atualizado!")
        ver_animais()

    tk.Button(janela, text="Salvar", width=15, command=salvar).pack(pady=5)
    tk.Button(janela, text="Voltar", width=15, command=ver_animais).pack(pady=5)

def relatorio():
    limpar_janela()
    conn = banco.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animais")
    dados = cursor.fetchall()
    conn.close()

    if not dados:
        messagebox.showinfo("Relatório", "Nenhum animal cadastrado.")
        abrir_menu("Usuário")
        return

    texto = "Relatório de Animais:\n\n"
    for a in dados:
        texto += f"ID: {a[0]} | {a[1]} - {a[2]} | {a[3]} anos | Situação: {a[4]}\n"

    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo = f"relatorios/relatorio_{agora}.txt"
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(texto)

    messagebox.showinfo("Relatório", f"Relatório salvo em:\n{arquivo}")
    abrir_menu("Usuário")

def limpar_janela():
    for widget in janela.winfo_children():
        widget.destroy()

def tela_login():
    limpar_janela()
    tk.Label(janela, text="Login", font=("Arial", 25, "bold")).pack(pady=20)

    tk.Label(janela, text="Nome de Usuário:").pack()
    global entrada_usuario
    entrada_usuario = tk.Entry(janela)
    entrada_usuario.pack()

    tk.Label(janela, text="Senha:").pack()
    global entrada_senha
    entrada_senha = tk.Entry(janela, show="*")
    entrada_senha.pack()

    tk.Button(janela, text="Entrar", width=15, command=login).pack(pady=10)
    tk.Button(janela, text="Cadastrar", width=15, command=tela_cadastro).pack()

    def suporte():
        messagebox.showinfo("Esqueceu a Senha", "Contate o suporte online.")

    tk.Button(janela, text="Esqueceu a senha?", width=20, fg="black", command=suporte).pack(pady=10)

def tela_cadastro():
    limpar_janela()
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

    def salvar_usuario():
        if not (nome.get() and sobrenome.get() and email.get() and usuario.get() and senha.get()):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        sucesso = banco.cadastrar_usuario(
            nome.get(),
            sobrenome.get(),
            email.get(),
            usuario.get(),
            senha.get()
        )

        if sucesso:
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            tela_login()
        else:
            messagebox.showerror("Erro", "Email ou nome de usuário já cadastrado.")

    tk.Button(janela, text="Salvar", width=15, command=salvar_usuario).pack(pady=10)
    tk.Button(janela, text="Voltar", width=15, command=tela_login).pack()

janela = tk.Tk()
janela.title("Adote com Amor")
janela.geometry("400x550")
tela_login()
janela.mainloop()