from socket import *
#importando o JSON -> necessário para transformar um vetor em String
import json

#atribuindo o nome, a porta e o socket padrão para estabelecer conexão com o servidor
serverName = 'localhost'
serverPort = 12000
cliente = socket(AF_INET, SOCK_STREAM)
cliente.connect((serverName, serverPort))

#recebendo a lista de produtos do servidor sem formatação
produtos = json.loads(cliente.recv(1024).decode())

#estabelecendo um limite de interações (máx 3 ofertas)
contador = 0
limite = 3

#função para receber a lista de produtos formatada e iniciar a negociação
def negociacao():
    while True:
        #formatação da lista de produtos
        print("Lista de produtos:")
        for produto in produtos:
            print("Código: {} | Nome: {} | Preço Inicial: {} | Estoque Disponível: {}".format(produto["codigo"], produto["nome"], produto["preco_inicial"], produto["estoque"]))

        codigo = int(input("Digite o código do produto que deseja comprar: "))
        preco = float(input("Digite o preço que deseja pagar: "))

        #validando se o código escolhido pelo cliente está na lista de produtos
        produto_valido = next((p for p in produtos if p["codigo"] == codigo), None)
        if not produto_valido:
            print("Código de produto inválido. Tente novamente.")
            continue
        
        #oferta do cliente sendo enviada pelo JSON
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

negociacao()
