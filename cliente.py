import socket
import ssl
import threading

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

def main():
    context = create_ssl_context()
    server_address = ('20.186.15.152', 1234)
    with socket.create_connection(server_address) as sock:
        with context.wrap_socket(sock, server_hostname='20.186.15.152') as ssock:
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
    main()
