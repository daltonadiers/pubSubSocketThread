# Simulador Pub/Sub com Sockets

Este projeto é uma implementação de um sistema de comunicação Pub/Sub utilizando sockets em Python. Ele consiste em três componentes principais:

1. **Gerador de Informações**: Gera diferentes tipos de informações e envia para o difusor.
2. **Difusor de Informações**: Recebe as informações dos geradores via protocolo UDP e distribui para os consumidores via protocolo TCP com base em seus interesses.
3. **Consumidor de Informações**: Inscreve-se no difusor para consumir tipos específicos de informações e exibe os dados recebidos.

## Funcionalidades

- **Gerador**: Cria múltiplos geradores de informação em threads e envia informações ao difusor através de sockets UDP.
- **Difusor**: Recebe informações dos geradores, atribui um número de sequência e distribui para os consumidores via TCP.
- **Consumidor**: Recebe as informações de interesse do difusor e as exibe em uma interface de texto.

### Tipos de Informações

Os tipos de informações geradas são:

1. Esportes
2. Novidades da Internet
3. Eletrônicos
4. Política
5. Negócios
6. Viagens

## Pré-requisitos

- Python 3.x instalado na máquina.
- Bibliotecas padrão de Python (não são necessárias bibliotecas externas).

## Como Executar

### Gerador

1. Execute o script do gerador:

    ```bash
    python gerador.py
    ```

2. Informe o número de geradores que deseja criar. O script irá gerar threads de geradores automaticamente.

### Difusor

1. Execute o difusor:

    ```bash
    python difusor.py
    ```

O difusor receberá informações dos geradores e aguardará conexões dos consumidores.

### Consumidor

1. Execute o consumidor:

    ```bash
    python consumidor.py
    ```

2. Ao iniciar, o consumidor perguntará o tipo de informação que deseja consumir. Você pode rodar várias instâncias do consumidor, cada uma se inscrevendo em um tipo de notícia diferente.

## Estrutura de Código

- `gerador.py`: Contém a lógica de criação dos geradores de informação e comunicação com o difusor via UDP.
- `difusor.py`: Centraliza as informações enviadas pelos geradores e repassa aos consumidores interessados.
- `consumidor.py`: Inscreve-se no difusor para receber informações de tipos específicos e exibe na tela.

## Exemplo de Fluxo de Trabalho

1. Execute o difusor (`difusor.py`).
2. Execute um ou mais geradores (`gerador.py`).
3. Execute um ou mais consumidores (`consumidor.py`) e inscreva-os em diferentes tipos de informação.
4. O difusor enviará as informações para os consumidores conforme os dados forem gerados.
5. Para encerrar qualquer um dos processos, pressione 'ENTER' no terminal respectivo.

## Contato

Para dúvidas ou sugestões, entre em contato pelo [dalton-adiers@outlook.com](mailto:dalton-adiers@outlook.com) ou [193570@upf.br](mailto:193570@upf.br)

## Autores

- [Carlos Eduardo Rosa Batista](https://github.com/CarlosEduardoBatista)
- [Dalton Oberdan Adiers](https://github.com/daltonadiers)