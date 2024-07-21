import socket
import ssl
import threading
import uuid
import hashlib
import sqlite3
import os

CERT_FILE = "certificate.pem"
KEY_FILE = "private_key.pem"

# Função para configurar o contexto SSL
def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
    return context

# Função para criar o servidor
def create_server():
    # Cria um socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1234))
    server_socket.listen(5)

    print("Servidor em execução na porta 1234...")

    # Configurar contexto SSL
    context = create_ssl_context()

    # Envolva o socket do servidor com SSL
    ssl_server_socket = context.wrap_socket(server_socket, server_side=True)

    # Looping de conexão com thread
    while True:
        client_ssl_socket, addr = ssl_server_socket.accept()
        # Inicie uma nova thread para lidar com o cliente
        threading.Thread(target=handle_client, args=(client_ssl_socket, addr)).start()

if __name__ == "__main__":
    create_server()
