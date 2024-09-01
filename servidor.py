from socket import *
import json

def products():
    produtos = [
        {"codigo": 1, "nome": "Celular", "preco_inicial": 200.0, "estoque": 20},
        {"codigo": 2, "nome": "Tablet", "preco_inicial": 400.0, "estoque": 25},
        {"codigo": 3, "nome": "Computador", "preco_inicial": 700.0, "estoque": 15}
    ]
    return produtos

limite = 3
serverPort = 12000
servidor = socket(AF_INET,SOCK_STREAM)
servidor.bind(('',serverPort))
servidor.listen(1)
print("Servidor online. Aguardando conexões...")

def conexao ():
    produtos = products()
    while True:
        cliente, endereco = servidor.accept()
        print("Conexão estabelecida com {}".format(endereco))

        cliente.send(json.dumps(produtos).encode())

        contador = 0
        while True:
            oferta = cliente.recv(1024).decode()
            if not oferta:
                break

            oferta = json.loads(oferta)
            produto = next(p for p in produtos if p["codigo"] == oferta["codigo"])
            tab = "================================================================="
            cliente.send(tab.encode())
            if oferta["preco"] < (produto["preco_inicial"] - produto["preco_inicial"]*0.1):
                resposta = "Oferta rejeitada. O valor está muito distante do preço inicial."
            elif produto["estoque"] <= 0:
                resposta = "Desculpe, não há mais estoque disponível deste produto."
            else:
                produto["estoque"] -= 1
                resposta = "Oferta aceita! Você comprou um {} por {}".format(produto["nome"], oferta["preco"])

            cliente.send(resposta.encode())
            cliente.send(tab.encode())

            contador += 1

            if contador >= limite:
                break

        cliente.close()

conexao()