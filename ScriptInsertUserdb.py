import sqlite3
import hashlib
import os  # Para gerar uma chave secreta única

def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            secret_key BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def generate_secret_key():
    """Gera uma chave secreta de 32 bytes (256 bits)."""
    return os.urandom(32)

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Hash da senha
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Gera uma chave secreta para o usuário
    secret_key = generate_secret_key()
    
    try:
        cursor.execute("INSERT INTO users (username, password, secret_key) VALUES (?, ?, ?)",
                       (username, hashed_password, secret_key))
        conn.commit()
        print(f"Usuário {username} registrado com sucesso.")
    except sqlite3.IntegrityError:
        print("Nome de usuário já existe.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_table()
    # Exemplo de registro de um novo usuário
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")
    register_user(username, password)
