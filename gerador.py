import socket
import _thread
import time
import random
from queue import Queue

lock = _thread.allocate_lock()
SERVER = '127.0.0.1'
PORT = 5002
VALOR_MAX = 10
VALOR_MIN = 3
T_MAX = 5
T_MIN = 2

class informacao:
    def __init__(self, tipo, valor):
        self.seq = 0
        self.tipo = tipo
        self.valor = valor

def thread_geradora(fila, tipo, info_max, info_min, t_max, t_min):
    while(True):
        valor_aleatorio = random.randint(info_min, info_max)
        fila.put(informacao(tipo, valor_aleatorio))
        time.sleep(random.randint(t_min, t_max))


def gerador(id, lista):
    fila = Queue()
    for i in range(len(lista)):
        if(lista[i]>0):
            _thread.start_new_thread(thread_geradora, (fila, i+1, VALOR_MAX, VALOR_MIN, T_MAX, T_MIN))
    while(True):
        if(not fila.empty()):
            lock.acquire()
            info = fila.get()
            print("-------")
            print(f"Sou o gerador: {id}")
            print(info.tipo)
            print(info.valor)
            print("-------")
            lock.release()

def main():    
    num_geradores = int(input("Digite o número de geradores: "))
    for i in range(num_geradores):
        lista = [random.randint(0,1) for _ in range(6)]
        _thread.start_new_thread(gerador, (i, lista))
    while(True):
        time.sleep(10)

if __name__ == "__main__":
    main()