# imprortação das bibliotecas
import socket # permite a comunicação entre cliente e servidor através de sockets
import json # facilita a serialização e desserialização de objetos

# Configurações do servidor
HOST = '127.0.0.1' # define o endereço IP do servidor  (127.0.0.1 - está disponível apenas localmente)
PORT = 65432 # define a porta no qual o servidor escutará conexões

# Catálogo inicial - dicionário que armazena os produtos disponíveis
catalogo = {
    "Notebook": {"preco": 3589.90, "quantidade": 53},
    "Mouse": {"preco": 215.00, "quantidade": 24},
    "Teclado": {"preco": 245.98, "quantidade": 490},
}

# função de processamento da solicitação 
# ela processa as requisições recebidas do cliente
def processar_solicitacao(solicitacao):
    operacao = solicitacao.get("operacao") # obtem a operação de solicitação
    if operacao == "consultar_nome": # consultar_nome procura um produto no catálogo e retornas as informações
        nome = solicitacao.get("nome")
        return catalogo.get(nome, "Produto não encontrado")
    elif operacao == "consultar_preco_inferior": #consultar_por_preco_inferior  filtra produtos com preço inferior a um valor fornecido
        valor = solicitacao.get("valor")
        return {nome: info for nome, info in catalogo.items() if info["preco"] < valor}
    elif operacao == "atualizar_estoque": # atualizar_estoque atualiza a quantidade em estoque de um produto
        nome = solicitacao.get("nome")  
        quantidade = solicitacao.get("quantidade")
        if nome in catalogo:
            catalogo[nome]["quantidade"] = quantidade
            return f"Estoque do produto '{nome}' atualizado para {quantidade}."
        else:
            return "Produto não encontrado para atualizar." 
    else: 
        return "Operação Inválida." # retorna mensagem de erro
    
def servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # socket.AF_INET usa IPv4 ; socket.SOCK_STREAM usa o protocolo TCP
        s.bind((HOST, PORT)) # associa o socket ao endereço IP e porta
        s.listen() # coloca o socket em mode de escuta
        print(f"Servidor escutando em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept() # aceita uma nova conexão e retorna um objeto de conexão (cnn) e o endereço do cliente(addr)
            with conn:
                print(f"Conexão estabelecida com {addr}.")
                data = conn.recv(1024) #recebe dados do cliente
                if not data: 
                    break
                try:
                    solicitacao = json.loads(data.decode())
                    resposta = processar_solicitacao(solicitacao) # a solicitação  é enviada pra função processar_solicitação a resposta é enviada pro cliente
                except (json.JSONDecodeError, KeyError) as e:
                    resposta = f"Erro ao processar solicitação: {e}"
                conn.sendall(json.dumps(resposta).encode())

if __name__ == "__main__":    
    servidor()
