from socket import *
import json

#Criação de um vetor que contém 3 produtos disponíveis
produtos = [
    {"codigo": 1, "nome": "Celular", "preco_inicial": 200.0, "estoque": 20},
    {"codigo": 2, "nome": "Tablet", "preco_inicial": 400.0, "estoque": 25},
    {"codigo": 3, "nome": "Computador", "preco_inicial": 700.0, "estoque": 15}
]

#Definindo limite de interações possíveis que o cliente poderá fazer
limite = 3

#Estabelecimento da conexão entre o servidor e o cliente
serverPort = 12000
servidor = socket(AF_INET,SOCK_STREAM)
servidor.bind(('',serverPort))
servidor.listen(1)
print("Servidor online. Aguardando conexões...")

#Parte onde ocorre as interações ofertas e etc.
while True:
    cliente, endereco = servidor.accept()
    print("Conexão estabelecida com {}".format(endereco))

    #Uso da biblioteca json para converter o vetor de produtos em uma string.
    cliente.send(json.dumps(produtos).encode())

    contador = 0
    while True:
        #Servidor recebe a oferta do cliente.
        oferta = cliente.recv(1024).decode()

        #Se não for uma oferta válida, a interação com o cliente é finalizada.
        if not oferta:
            break

        #Recebe a oferta e usa o json para receber a oferta e converte-la em uma string.
        oferta = json.loads(oferta)

        #Verifica se existe algum produto com o código requerido.
        produto = next(p for p in produtos if p["codigo"] == oferta["codigo"])

        #Apenas para formatação e melhorar o visual da resposta.
        tab = "=================================================================================="

        cliente.send(tab.encode())

        #Se o preço ofertado pelo cliente for menor do que o preço inicial - 5% do preço inicial, a oferta é recusada e é sugerido um preço minimo para o cliente se basear.
        if oferta["preco"] < (produto["preco_inicial"] - produto["preco_inicial"]*0.05):
            resposta = "Oferta rejeitada. O valor está muito distante do preço inicial. Preço minimo sugerido: {}".format((produto["preco_inicial"] - produto["preco_inicial"]*0.05))

        elif produto["estoque"] <= 0: #Verifica se há estoque do produto.
            resposta = "Desculpe, não há mais estoque disponível deste produto."

        else:#Caso ocorra a compra de um item, é diminuido 1 do valor do estoque do produto.
            produto["estoque"] -= 1
            resposta = "Oferta aceita! Você comprou um {} por {}".format(produto["nome"], oferta["preco"])

        #Envio da resposta para o cliente
        cliente.send(resposta.encode())

        #Controlando o limite de interações do usuário
        contador += 1
        if contador >= limite:
            break

    cliente.close()
