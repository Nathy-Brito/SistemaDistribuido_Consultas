import socket
import json

# configurações de cliente
HOST = '127.0.0.1'
PORT = 65432

def menu():
    print("Escolha uma operação:")
    print("1 - Consultar produto pelo nome")
    print("2 - Consultar produto com preço inferior a um valor")
    print("3 - Atualizar estoque de um produto")
    return input("Opção")

def cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            opcao = menu()
            if opcao == "1":
                nome = input("Digite o nome do produto: ")
                solicitacao = {"operacao": "consultar_nome", "nome": nome}
            elif opcao == "2":
                valor = float(input("Digite o valor máximo: "))
                solicitacao = {"operacao": "consultar_preco_inferior", "valor": valor}
            elif opcao == "3":
                nome = input("digite o nome do produto: ")
                quantidade = int(input("Digite a nova quantidade em estoque: "))
                solicitacao = {"operacao": "atualizar_estoque", "nome": nome, "quantidade": quantidade}
            else:
                print("Opção inválida!")
                continue
            
            s.s((json.dump(solicitacao).encode))
            resposta=json.loads(S.recv(1024).decode())
            print("Resposta ao servidor:", resposta)
if __name__ == "__main__":
    cliente()