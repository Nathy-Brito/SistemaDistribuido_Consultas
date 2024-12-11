import socket
import json

# configurações do servidor
HOST = '127.0.0.1'
PORT = 65432

# catálogo inicial 
catalogo = {
    "Notebook": {"preco": 3589.90, "quantidade": 53},
    "Mouse": {"preco": 215.00, "quantidade": 24},
    "teclado": {"preco": 245.98, "quantdade": 490},
}

def processar_solicitacao(solicitacao):
    operacao = solicitacao.get("operacao")
    if operacao == "conultar_nome":
        nome = solicitacao.get("nome")
        return catalogo.get(nome, "Produto nãp encontrado")
    elif operacao == "consultar_preco_inferior":
        valor = solicitacao.get("valor")
        return {nome: info for nome, info in catalogo.items() if info["preco"] < valor}
    elif operacao == "atualizar_estoque":
        nome = solicitacao.get("nome")  
        quantidade = solicitacao.get("quantidade")
        if nome in catalogo:
            catalogo[nome]["quantidade"] = quantidade
            return f"Estoque do produto '{nome}' atuallizado para {quantidade}."
        else:
            return "Produto não encontrado para atualizar."
    else: 
        return "Operação Inválida."
    
    def servidor():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Servidor escutando em {HOST}:{PORT}")
            while True:
                conn, addr = s.accept()
                with conn:
                    printf(f"Conexão estabelicida com {addr}.")
                    data = conn.recv(1024)
                    if not data:
                        break
                    solicitacao = json.loads(data.decode)
                    resposta = processar_solicitacao(solicitacao)
                    conn.sendall(json.dumps(resposta).encode())
                    
if __name__ == "__main__":    
    servidor()