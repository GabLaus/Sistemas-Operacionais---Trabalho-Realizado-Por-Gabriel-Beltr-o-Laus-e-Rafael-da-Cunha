import pickle
import os
import time
from banco import Requisicao, Registro, TipoRequisicao, PIPE_NAME

# Função que envia uma requisição serializada para o servidor
def enviar_requisicao(req: Requisicao):
    with open(PIPE_NAME, 'wb') as pipe:  # Abre o pipe em modo escrita binária
        pickle.dump(req, pipe)  # Serializa a requisição e escreve no pipe

# Função principal do cliente
def main():
    print("Tipo (0: INSERT, 1: DELETE, 2: SELECT, 3: UPDATE): ", end='')
    tipo = int(input())  # Lê o tipo de requisição
    tipo = TipoRequisicao(tipo)  # Converte para enum

    req = Requisicao(tipo=tipo)  # Cria a requisição

    # Monta a requisição de acordo com o tipo
    if tipo == TipoRequisicao.INSERT:
        req.reg = Registro(id=int(input("ID: ")), nome=input("Nome: "))
    elif tipo in [TipoRequisicao.DELETE, TipoRequisicao.SELECT]:
        req.id_busca = int(input("ID: "))
    elif tipo == TipoRequisicao.UPDATE:
        req.id_busca = int(input("ID: "))
        req.novo_nome = input("Novo nome: ")

    # Mede o tempo de envio da requisição
    inicio = time.time()
    enviar_requisicao(req)
    fim = time.time()
    print(f"Tempo de envio (cliente): {(fim - inicio)*1_000_000:.0f} microssegundos")

if __name__ == "__main__":
    main()
