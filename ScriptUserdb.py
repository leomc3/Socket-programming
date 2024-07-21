import sqlite3

def fetch_users():
    # Conectar ao banco de dados
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Executar a consulta
    cursor.execute("SELECT username, password FROM users")
    
    # Obter todos os resultados
    rows = cursor.fetchall()
    
    # Fechar a conexão com o banco de dados
    conn.close()
    
    return rows

def main():
    users = fetch_users()
    
    for user in users:
        print(f"Username: {user[0]}, Password: {user[1]}")

if __name__ == "__main__":
    main()
