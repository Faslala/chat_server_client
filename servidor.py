import socket
import threading

HOST = '127.0.0.1'
PORT = 55557

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

salas = {}

# Função para enviar uma mensagem para todos os clientes em uma sala
def broadcast(sala_recebida, mensagem):
    for i in salas[sala_recebida]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()
        i.send(mensagem)

# Função que lida com o envio de mensagens de um cliente para uma sala
def enviarMensagem(nome, sala_recebida, client):
    while True:
        try:
            mensagem = client.recv(1024).decode()
            mensagem = f'{nome}: {mensagem.decode()}\n'
            broadcast(sala_recebida, mensagem)
        except ConnectionResetError:
            # Remove o cliente da lista da sala e informa aos outros clientes
            salas[sala_recebida].remove(client)
            broadcast(sala_recebida, f'{nome} saiu da sala.')
            break
    

# Loop principal para aceitar novas conexões
while True:
    client, addr = server.accept()
    # Solicitação e recebimento do nome da sala e nome do cliente
    client.send(b'Sala que eu quero entrar')
    sala_recebida = client.recv(1024).decode()
    nome = client.recv(1024).decode()
    
    # Cria a sala se ela ainda não existir e adiciona o cliente à lista
    if sala_recebida not in salas.keys():
        salas[sala_recebida] = [] 
    salas[sala_recebida].append(client)
    
    # Informa aos outros clientes que um novo cliente entrou na sala
    broadcast(sala_recebida, f'{nome}: Entrou na sala!')
    
    # Inicia uma nova thread para lidar com as mensagens do cliente
    thread = threading.Thread(target=enviarMensagem, args=(nome, sala_recebida, client))
    thread.start()
