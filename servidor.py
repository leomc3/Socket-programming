import socket
import ssl
import sqlite3
import threading
import hashlib

# Caminhos para os arquivos de certificado e chave privada
CERT_FILE = "server_certificate.pem"
KEY_FILE = "server_key.pem"

# Dicionário para rastrear conexões de clientes e autenticação
clientes_conectados = {}
clientes_autenticados = {}

# Função para criar a tabela de usuários, se não existir
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

# Função para autenticar usuário
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Hash da senha fornecida
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Consulta ao banco de dados
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row and row[0] == hashed_password:
        return True
    return False

# Função para registrar um novo usuário
def register_user(username, password, secret_key):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Hash da senha
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        cursor.execute("INSERT INTO users (username, password, secret_key) VALUES (?, ?, ?)", (username, hashed_password, secret_key))
        conn.commit()
        print(f"Usuário {username} registrado com sucesso.")
    except sqlite3.IntegrityError:
        print("Nome de usuário já existe.")
    finally:
        conn.close()

# Função para enviar mensagem para todos os clientes
def enviar_mensagem_para_todos(mensagem):
    for client_id, conn in clientes_conectados.items():
        try:
            conn.sendall(mensagem.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem para cliente {client_id}: {str(e)}")

# Função para enviar mensagem para um cliente específico
def enviar_mensagem_para_cliente(client_id, mensagem):
    if client_id in clientes_conectados:
        conn = clientes_conectados[client_id]
        try:
            conn.sendall(mensagem.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem para cliente {client_id}: {str(e)}")
    else:
        print(f"Cliente {client_id} não encontrado ou desconectado.")

# Função para realizar o logoff de um cliente específico
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
    client_id = None  # O client_id será o nome de usuário
    try:
        # Conectar ao banco de dados (ou criar se não existir)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        while True:
            # Recebe dados do cliente
            data = client_ssl_socket.recv(1024)
            if not data:
                break  # Se não houver dados, saia do loop

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
            else:
                response = "Comando não reconhecido"

            # Enviando uma resposta
            client_ssl_socket.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"Erro durante a comunicação com o cliente {addr}: {str(e)}")
    finally:
        # Fechar o cursor e o socket do cliente
        if client_id in clientes_conectados:
            cursor.close()
            client_ssl_socket.close()
            # Fechar a conexão com o banco de dados
            conn.close()
            # Remover o cliente do dicionário de clientes conectados
            if client_id in clientes_conectados:
                del clientes_conectados[client_id]
            if client_id in clientes_autenticados:
                del clientes_autenticados[client_id]
            print(f"Cliente {client_id} desconectado")

def create_server():
    # Cria um socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1234))
    server_socket.listen(5)

    print("Servidor em execução na porta 1234...")

    # Configurar contexto SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    # Envolva o socket do servidor com SSL
    ssl_server_socket = context.wrap_socket(server_socket, server_side=True)

    # Looping de conexão com thread
    while True:
        client_ssl_socket, addr = ssl_server_socket.accept()
        # Inicie uma nova thread para lidar com o cliente
        threading.Thread(target=handle_client, args=(client_ssl_socket, addr)).start()

if __name__ == "__main__":
    create_table()
    create_server()
