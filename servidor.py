from socket import *
# importando o JSON -> necessário para transformar um vetor em String
import json


# funcao para criar um dicionário de produtos (contendo código, nome, preço inicial e um estoque)
def products():
    produtos = [
        {"codigo": 1, "nome": "Celular", "preco_inicial": 200.0, "estoque":5},
        {"codigo": 2, "nome": "Tablet", "preco_inicial": 400.0, "estoque":10},
        {"codigo": 3, "nome": "Computador", "preco_inicial": 700.0, "estoque":7}
    ]
    return produtos


# atribuindo o nome, a porta e o socket padrão para estabelecer conexão com o servidor
limite = 3

serverPort = 12000
servidor = socket(AF_INET, SOCK_STREAM)
servidor.bind(('', serverPort))
servidor.listen(1)
print("Servidor online. Aguardando conexões...")


# funcao para estabelecer a conexão e realizar a interação com o cliente
def conexao():
    contador = 0
    produtos = products()
    while True:
        # aceitando a conexão do clientes, retornando uma
        # tupla da conexão realizada (a variavel endereco recebe o IP da máquina do cliente)
        cliente, endereco = servidor.accept()
        print("Conexão estabelecida com {}".format(endereco))

        cliente.send(json.dumps(produtos).encode())

        while True:
            # recebendo a oferta do cliente e, caso
            # a oferta do cliente seja a mesma do preco_inicial, a proposta é aceita
            oferta = cliente.recv(1024).decode()
            if not oferta:
                break

            oferta = json.loads(oferta)
            produto = next(p for p in produtos if p["codigo"] == oferta["codigo"])

            # o cálculo da oferta é feito por: se a oferta é maior que o
            # preço inicial do produto - 10% do seu valor, a negociação
            # é bem sucedida. Ex: Preço inicial: 400
            # (a oferta só será aceita se o cliente oferecer um valor maior que 360)

            if oferta["preco"] < (produto["preco_inicial"] - produto["preco_inicial"] * 0.1):
                resposta = "Oferta rejeitada. O valor está muito distante do preço inicial."
            elif produto["estoque"] <= 0:
                resposta = "Desculpe, não há mais estoque disponível deste produto."
            else:
                produto["estoque"] -= 1
                resposta = "Oferta aceita! Você comprou um {} por {}".format(produto["nome"], oferta["preco"])

            cliente.send(resposta.encode())

            contador += 1
            if contador >= limite:
                break

    cliente.close()


conexao()
