import socket
import threading
import argparse
import sqlite3
import hashlib

clients = []

authenticated_clients = {}

# Função para enviar mensagem para um cliente específico
def enviar_mensagem_para_cliente(usuario, mensagem):
    for socket, user in authenticated_clients.items():
        if user == usuario:
            socket.send(mensagem.encode('utf-8'))
            return True
    return False

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

def authenticate(username, password, client_socket): 
    #client_socket.send("\nCREATE-USER username password\nLOGIN username password\n".encode('utf-8'))
    #credentials = client_socket.recv(1024).decode('utf-8').split()
    #if len(credentials) == 3 and credentials[0] == "LOGIN":
     #   username, password = credentials[1], credentials[2]
    if authenticate_user(username, password):  # Função para autenticar o usuário
        print(f'{username} Logado com sucesso')
        authenticated_clients[client_socket] = username
        #client_socket.send("Login bem-sucedido".encode('utf-8'))
        return True
    #client_socket.send("Erro: Nome de usuário ou senha inválidos".encode('utf-8'))
    return False

# Função para registrar um novo usuário
def register_user(username, password, client_socket): #ADICIONAR O SOCKET A LISTA
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Hash da senha
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        #msg = f"Usuário {username} registrado com sucesso."
        status = True
        authenticated_clients[client_socket] = username
    except sqlite3.IntegrityError:
        #msg = "Nome de usuário já existe."
        status = False
    finally:
        conn.close()
        return status

def handle_client(client_socket, client_address):
    client_socket.send("\nCREATE-USER username password\nLOGIN username password\n".encode('utf-8'))

    parts = client_socket.recv(1024).decode('utf-8').split()

    if parts[0] == "CREATE-USER":
            if len(parts) != 3:
                client_socket.send("Erro: Sintaxe inválida. Use: CREATE-USER username password. Desconetando cliente...".encode("utf-8"))
                client_socket.close()
            else:
                username = parts[1]
                password = parts[2]
                response = register_user(username, password, client_socket)
                print(response)
                if response:
                    client_socket.send(f"Usuário {username} registrado com sucesso.".encode('utf-8'))
                else:
                    client_socket.send("Nome de usuário já existe. Desconetando cliente...".encode('utf-8'))
                    client_socket.close()
                    return
        
    elif parts[0] =="LOGIN":
        if len(parts) != 3:
            client_socket.send("Erro: Sintaxe inválida. Use: LOGIN username password. Desconetando cliente...".encode('utf-8'))
            client_socket.close()
        else:
            username = parts[1]
            password = parts[2]
            response = authenticate(username, password, client_socket)
            if response:
                client_socket.send("Login bem-sucedido".encode('utf-8'))
            else:
                client_socket.send("Erro: Nome de usuário ou senha inválidos. Desconetando cliente...".encode('utf-8'))
                client_socket.close()
                return

    # if not authenticate(client_socket):
    #     client_socket.close()
    #     return

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                if client_socket in authenticated_clients:
                    parts = message.decode('utf-8').split()

                    msg = parts[0]
                    # if target == "ALL":
                    #     enviar_mensagem_para_todos(text)
                    #     response = "Mensagem enviada para todos os clientes"
                    # else:
                    #     enviar_mensagem_para_cliente(target, text)
                    #     response = f"Mensagem enviada para {target}"

                    if msg == 'MSG':
                        #target = parts[1]
                        #text = parts[2]
                        #print(len(parts))
                        if len(parts) > 2:
                            target = parts[1]
                            text = ' '.join(parts[2:])
                            
                            if target == 'ALL':
                                broadcast_message(f"Mensagem de {client_address}: {text}".encode('utf-8'), client_socket)
                            else:
                                enviar_mensagem_para_cliente(target, f"Mensagem de {client_address}: {text}".encode('utf-8'))
                        else:
                            client_socket.send("Erro: Sintaxe inválida. Use: MSG client-id text ou MSG ALL text".encode('utf-8'))

                    # remetente = f"Mensagem de {client_address}: {message.decode('utf-8')}"
                    # print(remetente)
                    # remetente_bytes = remetente.encode('utf-8')
                    elif msg == 'LOGOFF':
                        client_socket.send("Desconetando...".encode('utf-8'))
                        client_socket.close()
                        clients.remove(client_socket)
                        if client_socket in authenticated_clients:
                            del authenticated_clients[client_socket]
                else:
                    client_socket.send("Erro: Você não está autenticado.".encode('utf-8'))
            else:
                break
        except:
            break


    # while True:
    #     try:
    #         message = client_socket.recv(1024)
    #         if message:
    #             remetente = f"Mensagem de {client_address}: {message.decode('utf-8')}" 
    #             rementente_bytes = remetente.encode('utf-8')
    #             print(remetente)
    #             broadcast_message(rementente_bytes, client_socket)
    #         else:
    #             break
    #     except:
    #         break

    # client_socket.close()
    # clients.remove(client_socket)

#envia mensagem para todos os clientes ativos
def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def main(ip, porta):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, porta))
    server_socket.listen(5)

    print("Servidor está rodando e escutando por conexões...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Nova conexão de {client_address}")
        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Função para criar a tabela de usuários, se não existir
def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Servidor de mensagens")
        
    # Adicionar argumentos
    parser.add_argument('-i', '--ip', type=str, help="Endereço IP", required=True)
    parser.add_argument('-p', '--porta', type=int, help="Porta", required=True)
        
    # Analisar argumentos
    args = parser.parse_args()
    create_table()
    main(args.ip, args.porta)