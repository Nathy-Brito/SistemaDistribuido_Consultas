import socket
import json

# catálogo inicial 
catalogo = {
    "Primeiro_produto": {"preco": 527.98, "estoque": 53},
    "Segundo_produto": {"preco": 870.25, "estoque": 24},
    "Terceiro_produto": {"preco": 1299.90, "estoque": 30},
}

def handle_request(request):
    operacao = request.get("operacao")
    if operacao == "consultar_nome":
        nome = request.get("nome")
        return catalogo.get(nome, "Produto não encontrado.")
    elif operacao == "consultar_preco":
        max_preco = request.get("max_preco")
        