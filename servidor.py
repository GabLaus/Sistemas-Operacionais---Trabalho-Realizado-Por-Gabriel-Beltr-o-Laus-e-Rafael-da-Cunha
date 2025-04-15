import os
import threading
import pickle
import time
from banco import Requisicao, Registro, TipoRequisicao, PIPE_NAME
from threading import Lock

banco = []  # Lista que simula o banco de dados na memória
mutex = Lock()  # Mutex para sincronização entre threads

# Carrega o banco a partir de um arquivo texto
def carregar_banco():
    if not os.path.exists("banco.txt"):
        return
    with open("banco.txt", "r") as f:
        for linha in f:
            id, nome = linha.strip().split()
            banco.append(Registro(int(id), nome))

# Salva o banco atual no arquivo
def salvar_banco():
    with open("banco.txt", "w") as f:
        for r in banco:
            f.write(f"{r.id} {r.nome}\n")

# processa a requisição recebida em uma nova thread
def processar(req: Requisicao):
    inicio = time.time()
    with mutex:  # garante que só uma thread por vez manipule o banco
        if req.tipo == TipoRequisicao.INSERT and req.reg:
            banco.append(req.reg)
            print(f"Inserido: {req.reg.id}", flush=True)
        elif req.tipo == TipoRequisicao.DELETE:
            banco[:] = [r for r in banco if r.id != req.id_busca]
            print(f"Deletado ID: {req.id_busca}", flush=True)
        elif req.tipo == TipoRequisicao.SELECT:
            for r in banco:
                if r.id == req.id_busca:
                    print(f"Encontrado: {r.nome}", flush=True)
        elif req.tipo == TipoRequisicao.UPDATE:
            for r in banco:
                if r.id == req.id_busca:
                    r.nome = req.novo_nome
                    print(f"Atualizado ID: {r.id}", flush=True)
        salvar_banco()
    fim = time.time()
    tempo = (fim - inicio) * 1_000_000
    with open("desempenho.log", "a") as log:
        log.write(f"Tempo de processamento (thread): {tempo:.0f} microssegundos\n")

# loop principal do servidor
def main():
    if not os.path.exists(PIPE_NAME):
        os.mkfifo(PIPE_NAME)  # cria o pipe nomeado, se não existir

    carregar_banco()
    print("Servidor esperando requisições...")

    while True: #cada requisição que chegue seja criado mais uma thread
        with open(PIPE_NAME, 'rb') as pipe:  # abre o pipe para leitura
            req = pickle.load(pipe)  # desserializa a requisição recebida
            t = threading.Thread(target=processar, args=(req,))  # cria uma nova thread para processar a requisição
            t.daemon = True  # define como daemon (encerra junto com o programa principal)
            t.start()  # inicia a thread

if __name__ == "__main__":
    main()
