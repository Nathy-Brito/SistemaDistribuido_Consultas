import grpc
import catalogo_pb2
import catalogo_pb2_grpc

def menu():
    print("Escolha uma operação:")
    print("1 - Consultar produto pelo nome")
    print("2 - Consultar produto com preço inferior a um valor")
    print("3 - Atualizar estoque de um produto")
    return input("Opção")

def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = catalogo_pb2_grpc.CatlogoServiceStub(channel)
    while True:
        opcao = menu()
        if opcao == "1":
            nome = input("Digite o nome do produto: ")
            request = catalogo_pb2.ConsultaNomeRequest(nome = nome)
            try:
                response = stub.Consultlar_por_nome(request)
                print(f"Produto: {response.produto.nome}, Preço: {response.produto.preco}, Estoque: {response.prodto.quantidade}")
            except grpc.RpcError as e:
                print("Erro: {e.details()}")
        elif opcao == "2":
            valor = float(input("Digite o valor máximo: "))
            request = catalogo_pb2.ConsultarPrecoRequest(valor = valor)
            response = stub.Consultar_por_preco_inferior(request)
            for produto in response.produtos:
                print(f"Produto: {produto.nome}, Preço {produto.preco}, Estoque {produto.quantidade}")
        elif opcao == "3":
            nome = input("Digite o nome do produto: ")
            quantidade = int(input("Digite a nova quantidade em estoque: "))
            request = catalogo_pb2.Atualizar_estoque_request(nome = nome, quantidade = quantidade)
            try:
                response = stub.Atualizar_estoque(request)
                print(response.mensagem)
            except grpc.RpcError as e:
                print(F"Erro: {e.details()}")
        else:
            print("Opção inválida.")
            
if __name__ == "__main__":
    main()