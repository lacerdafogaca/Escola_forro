"""
Classe modelo para a tabela pessoa
"""
from model.categoria import Categoria

class Pessoa:
    def __init__(self, id: int, nome: str, categoria: Categoria, email: str,
                 data_nascimento: str | None = None,
                 telefone: str | None = None):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__data_nascimento = data_nascimento
        self.__telefone = telefone
        self.__categoria = categoria

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, value):
        self.__nome = value
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def data_nascimento(self):
        return self.__data_nascimento
    
    @data_nascimento.setter
    def data_nascimento(self, value):
        self.__data_nascimento = value

    @property
    def telefone(self):
        return self.__telefone
    
    @telefone.setter
    def telefone(self, value):
        self.__telefone = value
    
    def __str__(self):
        return (f"Pessoa(id={self.id}, nome='{self.nome}', "
                f"email='{self.email}', idade={self.idade}, "
                f"categoria_id={self.categoria.id})")

