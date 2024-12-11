# imprtação de bibliotecas
import socket
import json

# Configurações de cliente, deine o endereço e a porta do servidor para o cliente se CONECTAR
HOST = '127.0.0.1'
PORT = 65432

# exibição de opções disponíveis para o usuário, a opção escolhida é rotornada
def menu():
    print("Escolha uma operação:")
    print("1 - Consultar produto pelo nome")
    print("2 - Consultar produto com preço inferior a um valor")
    print("3 - Atualizar estoque de um produto")
    print("4 - Sair")
    return input("Opção: ")

def cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT)) #conecta o cliente ao servidor
        while True: 
            opcao = menu() #mostra as opções e processa a entrada 
            if opcao == "1":
                nome = input("Digite o nome do produto: ")
                solicitacao = {"operacao": "consultar_nome", "nome": nome}
            elif opcao == "2":
                try:
                    valor = float(input("Digite o valor máximo: "))
                except ValueError:
                    print("Valor inválido! Tente novamente.")
                    continue
                solicitacao = {"operacao": "consultar_preco_inferior", "valor": valor}
            elif opcao == "3":
                nome = input("Digite o nome do produto: ")
                try:
                    quantidade = int(input("Digite a nova quantidade em estoque: "))
                except ValueError:
                    print("Quantidade inválida! Tente novamente.")
                    continue
                solicitacao = {"operacao": "atualizar_estoque", "nome": nome, "quantidade": quantidade}
            elif opcao == "4":
                print("Encerrando o cliente.")
                break
            else:
                print("Opção inválida!")
                continue
            
            try:
                s.send(json.dumps(solicitacao).encode())
                resposta = json.loads(s.recv(1024).decode())
                print("Resposta do servidor:", resposta)
            except Exception as e:
                print("Erro ao comunicar com o servidor:", e)
                break

if __name__ == "__main__":
    cliente()
