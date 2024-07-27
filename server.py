import socket
import ssl
import sqlite3
import threading
import hashlib

CERT_FILE = "server_certificate.pem"
KEY_FILE = "server_key.pem"

clientes_conectados = {}
clientes_autenticados = {}
server_running = True

def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            secret_key TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and row[0] == hashed_password:
        return True
    return False

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    secret_key = hashlib.sha256((username + password).encode()).hexdigest()  # Gerar chave secreta com base no username e password
    try:
        cursor.execute("INSERT INTO users (username, password, secret_key) VALUES (?, ?, ?)", (username, hashed_password, secret_key))
        conn.commit()
        return f"Usuário {username} registrado com sucesso."
    except sqlite3.IntegrityError:
        return "Nome de usuário já existe."
    finally:
        conn.close()

def enviar_mensagem_para_todos(mensagem):
    for client_id, conn in clientes_conectados.items():
        try:
            conn.sendall(mensagem.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem para cliente {client_id}: {str(e)}")

def enviar_mensagem_para_cliente(client_id, mensagem):
    if client_id in clientes_conectados:
        conn = clientes_conectados[client_id]
        try:
            conn.sendall(mensagem.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem para cliente {client_id}: {str(e)}")
    else:
        print(f"Cliente {client_id} não encontrado ou desconectado.")

def logoff_cliente(client_id):
    if client_id in clientes_conectados:
        conn = clientes_conectados[client_id]
        try:
            conn.sendall("Você foi desconectado pelo servidor.".encode())
            conn.close()
        except Exception as e:
            print(f"Erro ao desconectar cliente {client_id}: {str(e)}")
        finally:
            username = clientes_autenticados[client_id]
            del clientes_conectados[client_id]
            del clientes_autenticados[client_id]
            print(f"Cliente {username} desconectado")
    else:
        print(f"Cliente {client_id} não encontrado ou já desconectado.")

def handle_client(client_ssl_socket, addr):
    client_id = None
    global server_running
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        while True:
            data = client_ssl_socket.recv(1024)
            if not data:
                break
            mensagem = data.decode('utf-8')
            print(f"Recebido de {addr}: {mensagem}")
            if mensagem.startswith("MSG"):
                parts = mensagem.split(' ', 2)
                if len(parts) < 3:
                    response = "Erro: Sintaxe inválida. Use: MSG client-id text ou MSG ALL text"
                else:
                    target = parts[1]
                    text = parts[2]
                    if target == "ALL":
                        enviar_mensagem_para_todos(text)
                        response = "Mensagem enviada para todos os clientes"
                    else:
                        enviar_mensagem_para_cliente(target, text)
                        response = f"Mensagem enviada para {target}"
            elif mensagem.startswith("LOGIN"):
                parts = mensagem.split(' ', 2)
                if len(parts) != 3:
                    response = "Erro: Sintaxe inválida. Use: LOGIN username password"
                else:
                    username = parts[1]
                    password = parts[2]
                    if authenticate_user(username, password):
                        client_id = username
                        clientes_conectados[client_id] = client_ssl_socket
                        clientes_autenticados[client_id] = username
                        response = f"Login bem-sucedido para {username}"
                    else:
                        response = "Erro: Nome de usuário ou senha inválidos"
            elif mensagem.startswith("LOGOFF"):
                parts = mensagem.split(' ', 1)
                if len(parts) != 2:
                    response = "Erro: Sintaxe inválida. Use: LOGOFF username"
                else:
                    logoff_id = parts[1]
                    if client_id == logoff_id:
                        logoff_cliente(client_id)
                        response = f"Cliente {logoff_id} desconectado"
                        break
                    else:
                        response = "Erro: Usuário não autenticado ou inválido"
            elif mensagem.startswith("CREATE-USER"):
                parts = mensagem.split(' ', 2)
                if len(parts) != 3:
                    response = "Erro: Sintaxe inválida. Use: CREATE-USER username password"
                else:
                    username = parts[1]
                    password = parts[2]
                    response = register_user(username, password)
            elif mensagem == "EXIT":
                response = "Servidor desligando..."
                server_running = False
                break
            else:
                response = "Comando não reconhecido"
            client_ssl_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Erro durante a comunicação com o cliente {addr}: {str(e)}")
    finally:
        if client_id in clientes_conectados:
            cursor.close()
            client_ssl_socket.close()
            conn.close()
            if client_id in clientes_conectados:
                del clientes_conectados[client_id]
            if client_id in clientes_autenticados:
                del clientes_autenticados[client_id]
            print(f"Cliente {client_id} desconectado")

def create_server():
    global server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1234))
    server_socket.listen(5)
    print("Servidor em execução na porta 1234...")
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    ssl_server_socket = context.wrap_socket(server_socket, server_side=True)
    while server_running:
        try:
            client_ssl_socket, addr = ssl_server_socket.accept()
            threading.Thread(target=handle_client, args=(client_ssl_socket, addr)).start()
        except Exception as e:
            if server_running:
                print(f"Erro ao aceitar conexão: {str(e)}")
            break
    ssl_server_socket.close()
    print("Servidor desligado.")

if __name__ == "__main__":
    create_table()
    create_server()
