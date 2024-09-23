from socket import *
import json
#Estabelecendo conexão com o servidor
serverName = 'localhost'
serverPort = 12000
cliente = socket(AF_INET, SOCK_STREAM)
cliente.connect((serverName, serverPort))

#Recebendo o vetor de produtos do servidor em forma de um objeto json que converte para uma string
produtos = json.loads(cliente.recv(1024).decode())

#Criação de um contador para controlar as interações
contador = 0
limite = 3

while True:
    #Printa para o usuário a lista de produtos recebida por meio de um foreach
    print("Lista de produtos:")
    for produto in produtos:
        print("Código: {} | Nome: {} | Preço Inicial: {} | Estoque Disponível: {}".format(produto["codigo"], produto["nome"], produto["preco_inicial"], produto["estoque"]))

    #Inputs para saber qual produto o usuário quer comprar e qual preço ele quer pagar
    codigo = int(input("Digite o código do produto que deseja comprar: "))
    preco = float(input("Digite o preço que deseja pagar: "))

    #Verificação se o produto existe na lista de produtos
    produto_valido = next((p for p in produtos if p["codigo"] == codigo), None)
    if not produto_valido:
        print("Código de produto inválido. Tente novamente.")
        continue

    #Cria um vetor com o codigo e o preço que o cliente quer comprar
    oferta = {"codigo": codigo, "preco": preco, "produto": produto_valido["nome"]}

    #Envia o vetor em objeto json para o servidor, que recebe e converte em uma string
    cliente.send(json.dumps(oferta).encode())

    tab = cliente.recv(1024).decode()
    print(tab)
    resposta = cliente.recv(1024).decode()

    #Verifica se o cliente fez uma compra, se sim, o limite de interações dele é zerado, tendo mais 3 tentativas de comprar um produto.
    if resposta.startswith("Oferta aceita!"):
        contador = 0

    print(resposta)
    print(tab)
    contador += 1
    if contador >= limite:
        print("Você atingiu o limite de tentativas para realizar uma compra. Saindo...")
        break

cliente.close()
