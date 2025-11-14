"""
Classe modelo para a tabela inscricao
"""
from model.pessoa import Pessoa

class Inscricao:
    def __init__(self, id: int, aluno: str, nivel: str, data: str, posicao: str, aluno_id=int):
        self.id = id
        self.aluno = aluno
        self.nivel = nivel
        self.data = data
        self.posicao = posicao
        self.aluno_id = aluno_id

    def __str__(self):
        return (f"Turma(id={self.id}, aluno={self.aluno}, nivel={self.nivel}, data='{self.data}', "
                f"posicao='{self.posicao}')")