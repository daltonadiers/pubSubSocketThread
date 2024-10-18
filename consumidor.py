import socket
import _thread
import pickle

SERVER_TCP = "127.0.0.1"
PORT_TCP = 7777
ID = 0
lock = _thread.allocate_lock()

class informacao:
    def __init__(self, tipo, valor):
        self.seq = 0
        self.tipo = tipo
        self.valor = valor

def newRegister():
        lock.acquire()
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_TCP, PORT_TCP))
            inscricoes = input("Digite entre 1 e 6 para se inscrever nos assuntos pertinentes: ")
            numeros = pickle.dumps(list(map(int, inscricoes.split())))
            client.send(numeros)
            ID += 1
            _thread.start_new_thread(receiveMessages, (client, ID))
        except:
            print("Não foi possível se conectar")
        lock.release()

def receiveMessages(client, ID):
     while True:
        try:
            info = pickle.load(client.recv(2048))
            print(f"Sou o cliente {ID}: ")
            print(f"Recebi uma mensagem do tipo {info.tipo}, contendo o valor {info.valor}")
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break

def main():
    while(True):
        comando = input("Digite 'N' para cadastrar um novo usuário: ")
        if(comando == "N"):
            _thread.start_new_thread(newRegister, ())


if __name__ == "__main__":
    main()