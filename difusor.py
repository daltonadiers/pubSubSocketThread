import socket
import pickle
import _thread
import time
from queue import Queue

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("127.0.0.1", 5002))
lock = _thread.allocate_lock()
clients = []
clients_interests = [[] for _ in range(1, 7)]
SERVERTCP = "127.0.0.1"
PORTTCP = 7777

class informacao:
    def __init__(self, tipo, valor):
        self.seq = 0
        self.tipo = tipo
        self.valor = valor

def tcpConection():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVERTCP, PORTTCP))
    server.listen()
    while(True):
        client, addr = server.accept()
        clients.append(client)
        _thread.start_new_thread(receiveRegister, (client,))

def receiveRegister(client):
     while True:
        msg = client.recv(2048)
        lista_numeros = pickle.loads(msg)
        if(lista_numeros[0]==-1):
            clients.remove(client)
            for i in clients_interests:
                i.remove(client)
            client.close()
            break
        elif(lista_numeros[0]==-2):
            for i in range(1,len(lista_numeros)):
                clients_interests[lista_numeros[i]].append(client)

def ouvinte(filas):
    while(True):
        data, endereco = udp_socket.recvfrom(1024)
        lock.acquire()
        objeto = pickle.loads(data)
        print(f"sou o tipo {objeto.tipo}")
        filas[objeto.tipo].put(objeto)
        lock.release()

def disseminador(fila, id):
    while(True):
        if not fila.empty():
            lock.acquire()
            info = fila.get()
            print(f"Sou a thread {id}: ")
            print(info.valor)
            lock.release()


def instancia_threads():
    _thread.start_new_thread(tcpConection, ())
    filas = [Queue() for _ in range(7)]
    _thread.start_new_thread(ouvinte,(filas,))
    for i in range(6):
        _thread.start_new_thread(disseminador, (filas[i], i))

def main():
    instancia_threads()
    while(True):
        time.sleep(100)


if __name__ == "__main__":
    main()