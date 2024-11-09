import socket
import _thread
import pickle

SERVER_TCP = "127.0.0.1"
PORT_TCP = 7777
ID = 0
lock = _thread.allocate_lock()

categorias = {
    1: "Esportes",
    2: "Novidades da Internet",
    3: "Eletrônicos",
    4: "Política",
    5: "Negócios",
    6: "Viagens"
}

class informacao:
    def __init__(self, seq, tipo, valor):
        self.seq = seq
        self.tipo = tipo
        self.valor = valor

def newRegister():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_TCP, PORT_TCP))
    inscricoes = input("Digite entre 1 e 6 (separado por espaço) para se inscrever nos assuntos pertinentes: ")
    numeros = list(map(int, inscricoes.split()))
    numeros.insert(0, -2)
    client.send(pickle.dumps(numeros))
    global ID
    ID += 1
    _thread.start_new_thread(receiveMessages, (client, ID))

def receiveMessages(client, ID):
     print("--------")
     while True:
        msg = client.recv(2048)
        if(msg):
            info = pickle.loads(msg)
            print(f"Sou a mensagem de sequência: {info.seq}: ")
            print(f"Recebi uma mensagem do tipo {categorias[info.tipo]}, contendo o valor {info.valor}")

def main():
    comando = input("Digite 'N' para cadastrar um novo usuário: ")
    if(comando == "N"):
        newRegister()
    encerrar = input("Pressione enter para encerrar!")


if __name__ == "__main__":
    main()