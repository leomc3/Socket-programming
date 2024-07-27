import socket
import threading
import ssl
import argparse

#espera por mensagens do servidor

def listen_for_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print("\nMensagem do servidor:", message)
            else:
                break
        except:
            break

def main(ip, porta):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, porta))

    # Iniciando a thread para escutar as mensagens do servidor
    #as threas irão permitir que o servidor consiga enviar mensagens para o cliente, mesmo que ele esteja na função de input
    
    listen_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
    listen_thread.daemon = True
    listen_thread.start()

    while True:
        message = input("Você: ")
        if message.lower() == 'LOGOFF':
            break
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            print(f"Descontado do servidor: {ip}")
            break
    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente argumentos")
        
    # Adicionar argumentos
    parser.add_argument('-i', '--ip', type=str, help="Endereço IP", required=True)
    parser.add_argument('-p', '--porta', type=int, help="Porta", required=True)
        
    # Analisar argumentos
    args = parser.parse_args()
    
    main(args.ip, args.porta)
