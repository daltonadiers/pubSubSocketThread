import socket
import pickle
import _thread
import time
from queue import Queue

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("127.0.0.1", 5002))
lock = _thread.allocate_lock()

class informacao:
    def __init__(self, tipo, valor):
        self.seq = 0
        self.tipo = tipo
        self.valor = valor


def ouvinte(filas):
    while(True):
        #print("Aguardando objeto...")
        data, endereco = udp_socket.recvfrom(1024)
        lock.acquire()
        objeto = pickle.loads(data)
        #print(f"Objeto recebido: seq={objeto.seq}, tipo={objeto.tipo}, valor={objeto.valor}")
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