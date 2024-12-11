from concurrent import futures 
import grpc
import catalogo_pb2
import catalogo_pb2_grpc

# catalogo de produtos 
catalogo = {
    "Notebool": {"preco": 3589.90, "quantidade": 53},
    "Mouse": {"preco": 215.00, "quantidade": 24},
    "Teclado": {"preco": 245.98, "quantidade": 490},
}

class CatalogoService(catalogo_pb2_grpc.CatalogoServiceServicer):
    def Consultar_por_nome(self, request, context):
        produto = catalogo.get(request.nome)
        if produto:
            return catalogo_pb2.Produto_response(
                produto = catalogo_pb2.Produto_(
                    nome = request.nome,
                    preco = produto["preco"],
                    quantidade = produto["quantidade"]
                )
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Produto não encontrado.")
            return catalogo_pb2.Produto_response()
        
def Consultar_por_preco_inferior(self, request, context):
    produtos = [
        catalogo_pb2.Produto(nome = nome, preco = info["preco"], quantidade=info["quantidade"])
        for nome, info in catalogo.items() if info["preco"] < request.valor
    ]
    return catalogo_pb2.Lista_produtos_response(produtos = produtos)

def Atualizar_estoque(self, request, context):
   if request.nome in catalogo:
       catalogo[request.nome]["quantidade"] = request.quantidade
       return catalogo_pb2.Atualizar_estoque_response(
           mensagem= f"Estoque do produto '{request.nome}' atualizado para {request.quantidade}."
       ) 
   else:
       context.set_code(grpc.StatusCode.NOT_FOUND)
       context.set_details("Produto não encontrado.")
       return catalogo_pb2.Atualizar_estoque_response()

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    catalogo_pb2_grpc.add_CatlogoServiceServicer_to_server(CatalogoService(), server)
    server.add_insecure_port("[::]:50051")
    print("Servidor gRPC escutando na porta 50051")
    server.wait_for_termination()
    
if __name__ == "__main__":
    server()
