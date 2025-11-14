"""
Classe modelo para a tabela pessoa
"""
from model.categoria import Categoria

class Pessoa:
    def __init__(self, id: int, nome: str, categoria: Categoria, email: str,
                 data_nascimento: str | None = None,
                 telefone: str | None = None):
        self.id = id
        self.nome = nome
        self.email = email
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.categoria = categoria

    def __str__(self):
        return (f"Pessoa(id={self.id}, nome='{self.nome}', "
                f"email='{self.email}', idade={self.idade}, "
                f"categoria_id={self.categoria.id})")

