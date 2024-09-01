from socket import *
import json

serverName = 'localhost'
serverPort = 12000
cliente = socket(AF_INET, SOCK_STREAM)
cliente.connect((serverName, serverPort))

produtos = json.loads(cliente.recv(1024).decode())

contador = 0
limite = 3

def conexao():
    while True:
        print("Lista de produtos:")
        for produto in produtos:
            print("Código: {} | Nome: {} | Preço Inicial: {} | Estoque Disponível: {}".format(produto["codigo"], produto["nome"], produto["preco_inicial"], produto["estoque"]))

        codigo = int(input("Digite o código do produto que deseja comprar: "))
        preco = float(input("Digite o preço que deseja pagar: "))

        produto_valido = next((p for p in produtos if p["codigo"] == codigo), None)
        if not produto_valido:
            print("Código de produto inválido. Tente novamente.")
            continue

        oferta = {"codigo": codigo, "preco": preco}
        cliente.send(json.dumps(oferta).encode())

        tab = cliente.recv(1024).decode()
        print(tab)
        resposta = cliente.recv(1024).decode()
        print(resposta)
        tab = cliente.recv(1024).decode()
        print(tab)

        contador += 1
        if contador >= limite:
            print("Você atingiu o limite de compras. Saindo...")
            break

conexao()
