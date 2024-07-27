import socket
import ssl
import threading
import argparse

CERT_FILE = "client_certificate.pem"
KEY_FILE = "client_key.pem"
SERVER_CERT_FILE = "ca_certificate.pem"

def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT_FILE)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    return context

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print(data.decode('utf-8'))
            else:
                break
        except Exception as e:
            print(f"Erro ao receber mensagem: {str(e)}")
            break

def main(ip, porta):
    context = create_ssl_context()
    server_address = (ip, porta)
    with socket.create_connection(server_address) as sock:
        with context.wrap_socket(sock, server_hostname=ip) as ssock:
            print("Conectado ao servidor")
            threading.Thread(target=receive_messages, args=(ssock,)).start()
            while True:
                mensagem = input()
                if mensagem.startswith("LOGIN") or mensagem.startswith("LOGOFF") or mensagem.startswith("MSG") or mensagem.startswith("CREATE-USER"):
                    ssock.sendall(mensagem.encode('utf-8'))
                    if mensagem.startswith("LOGOFF"):
                        break
                else:
                    print("Comando não reconhecido. Use: LOGIN username password, LOGOFF username, MSG client-id text, MSG ALL text ou CREATE-USER username password")
            print("Desconectado do servidor")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente argumentos")
        
    # Adicionar argumentos
    parser.add_argument('-i', '--ip', type=str, help="Endereço IP", required=True)
    parser.add_argument('-p', '--porta', type=int, help="Porta", required=True)
        
    # Analisar argumentos
    args = parser.parse_args()
    main(args.ip, args.porta)
