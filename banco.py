import sqlite3
import hashlib

def conectar():
    return sqlite3.connect("banco.db")

def criar_tabela_animais():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especie TEXT NOT NULL,
            idade INTEGER NOT NULL,
            situacao TEXT NOT NULL -- 'adotado' ou 'disponível'
        )
    """)
    conn.commit()
    conn.close()

def criar_tabela_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            nome_usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario(nome, sobrenome, email, nome_usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    try:
        senha_hash = hash_senha(senha)
        cursor.execute("""
            INSERT INTO usuarios (nome, sobrenome, email, nome_usuario, senha)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, sobrenome, email, nome_usuario, senha_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validar_login(nome_usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    senha_hash = hash_senha(senha)
    cursor.execute("""
        SELECT nome FROM usuarios WHERE nome_usuario = ? AND senha = ?
    """, (nome_usuario, senha_hash))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def recuperar_senha(email):
    """
    Função para teste. Em produção, implemente recuperação via e-mail.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

if __name__ == "__main__":
    criar_tabela_animais()
    criar_tabela_usuarios()
