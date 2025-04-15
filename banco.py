from enum import Enum
from dataclasses import dataclass

PIPE_NAME = "/tmp/banco_pipe"  # Caminho do pipe nomeado usado para comunicação entre cliente e servidor
MAX_NOME = 50  # Tamanho máximo do nome (não é usado diretamente, mas pode ser útil para validação)

# Enum que define os tipos de requisição que o cliente pode fazer
class TipoRequisicao(Enum):
    INSERT = 0
    DELETE = 1
    SELECT = 2
    UPDATE = 3

# Classe que representa um registro no banco de dados (id + nome)
@dataclass
class Registro:
    id: int
    nome: str

# Classe que representa uma requisição feita pelo cliente
@dataclass
class Requisicao:
    tipo: TipoRequisicao
    reg: Registro = None      # Usado no INSERT
    id_busca: int = None      # Usado no DELETE, SELECT e UPDATE
    novo_nome: str = None     # Usado no UPDATE
