"""
Classe modelo para a tabela turma
"""
from model.nivel import Nivel

class Turma:
    def __init__(self, id: int, horario: str, nivel: Nivel, professor: str):
        self.__id = id
        self.__horario = horario
        self.__nivel = nivel
        self.__professor = professor

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def horario(self):
        return self.__horario
    
    @horario.setter
    def horario(self, value):
        self.__horario = value
    
    @property
    def nivel(self):
        return self.__nivel
    
    @nivel.setter
    def nivel(self, value):
        self.__nivel = value

    @property
    def professor(self):
        return self.__professor
    
    @professor.setter
    def professor(self, value):
        self.__professor = value

    def __str__(self):
        return (f"Turma(id={self.id}, horario='{self.horario}', "
                f"nivel='{self.nivel.nome}', professor='{self.professor}')")