"""
Classe modelo para a tabela de niveis
"""

class Nivel:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome

    def __str__(self):
        return f"Nivel(id={self.id}, nome='{self.nome}')"