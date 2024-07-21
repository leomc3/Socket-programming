import socket
import ssl
import threading

# Caminhos para os arquivos de certificado e chave privada
CERT_FILE = "client_certificate.pem"
KEY_FILE = "client_key.pem"
SERVER_CERT_FILE = "server_certificate.pem"

# Função para criar o contexto SSL
def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT_FILE)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    return context

# Função para receber mensagens do servidor
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

# Função principal do cliente
def main():
    # Cria o contexto SSL
    context = create_ssl_context()
    
    # Conecta ao servidor
    server_address = ('localhost', 1234)
    with socket.create_connection(server_address) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:
            print("Conectado ao servidor")

            # Inicia uma thread para receber mensagens do servidor
            threading.Thread(target=receive_messages, args=(ssock,)).start()

            # Aguarda o comando LOGIN
            while True:
                mensagem = input()
                if mensagem.startswith("LOGIN"):
                    ssock.sendall(mensagem.encode('utf-8'))
                elif mensagem.startswith("LOGOFF"):
                    ssock.sendall(mensagem.encode('utf-8'))
                    break
                elif mensagem.startswith("MSG"):
                    ssock.sendall(mensagem.encode('utf-8'))
                else:
                    print("Comando não reconhecido. Use: LOGIN username password, LOGOFF username, MSG client-id text ou MSG ALL text")
            
            print("Desconectado do servidor")

if __name__ == "__main__":
    main()
