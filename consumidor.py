import sys
import socket
import _thread
import pickle
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt

SERVER_TCP = "127.0.0.1"
PORT_TCP = 7777
ID = 0
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

class ConsumerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cliente Consumidor - Pub/Sub")
        self.setGeometry(300, 300, 500, 400)
        self.client = None
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Inscreva-se em um ou mais tópicos:\n1 - Esportes\n2 - Novidades da Internet\n3 - Eletrônicos\n4 - Política\n5 - Negócios\n6 - Viagens")
        self.label.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.label)
        
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Exemplo: 1 2 3")
        self.category_input.setFont(QFont("Arial", 10))
        self.layout.addWidget(self.category_input)
        
        self.connect_button = QPushButton("Conectar e Receber Mensagens")
        self.connect_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.connect_button.clicked.connect(self.new_register)
        self.layout.addWidget(self.connect_button)
        
        self.stop_button = QPushButton("Parar")
        self.stop_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.stop_button.clicked.connect(self.stop_client)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)
        
        self.messages_area = QTextEdit()
        self.messages_area.setReadOnly(True)
        self.messages_area.setFont(QFont("Courier", 10))
        self.layout.addWidget(self.messages_area)
        
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f2f2f2;
            }
            QLabel {
                color: #333333;
                padding: 5px;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                padding: 5px;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 10px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #66a3ff;
            }
            QPushButton:disabled {
                background-color: #aaaaaa;
                color: #ffffff;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                padding: 10px;
                border-radius: 4px;
                background-color: #ffffff;
                color: #333333;
            }
        """)

    def new_register(self):
        inscricoes = self.category_input.text()
        numeros = list(map(int, inscricoes.split()))
        numeros.insert(0, -2)
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER_TCP, PORT_TCP))
        self.client.send(pickle.dumps(numeros))
        
        global ID
        ID += 1
        _thread.start_new_thread(self.receive_messages, (self.client, ID))
        
        self.stop_button.setEnabled(True)
        self.connect_button.setEnabled(False)

    def receive_messages(self, client, ID):
        while True:
            try:
                msg = client.recv(2048)
                if msg:
                    info = pickle.loads(msg)
                    message = f"Mensagem de sequência {info.seq}:\n"
                    message += f"Tipo: {categorias[info.tipo]}\nConteúdo: {info.valor}\n\n"
                    
                    self.messages_area.insertPlainText(message + '\n')
                    self.messages_area.moveCursor(QTextCursor.Start)
            except OSError:
                break

    def stop_client(self):
        if self.client:
            self.client.close() 
            self.client = None
        
        self.stop_button.setEnabled(False)
        self.connect_button.setEnabled(True)
        
        self.messages_area.moveCursor(QTextCursor.Start)
        self.messages_area.insertPlainText("Conexão encerrada.\n\n")

    def closeEvent(self, event):
        """Sobrescreve o método de fechamento para garantir que o cliente seja desconectado ao fechar a janela."""
        self.stop_client()
        event.accept()

def main():
    app = QApplication(sys.argv)
    consumer_app = ConsumerApp()
    consumer_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
