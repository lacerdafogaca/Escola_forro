"""
DAO (Data Access Object) para operações de banco de dados da tabela turma
"""
from bd.database import DatabaseConnection
from dao.nivel_dao import NivelDAO
from model.turma import Turma

class TurmaDAO:
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.nivelDao = NivelDAO(db)

    def salvar(self, turma: Turma):
        cur = self.db.cursor()

        nivel_id = turma.nivel.id

        if turma.id is None:
            # INSERT
            cur.execute(
                "INSERT INTO turma (horario, nivel_id, professor) VALUES (?, ?, ?);", 
                (turma.horario, nivel_id, turma.professor)
            )
            turma.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute(
                "UPDATE turma SET horario = ?, nivel_id = ?, professor = ? WHERE id = ?;", 
                (turma.horario, nivel_id, turma.professor, turma.id)
            )

        return turma.id

    def buscarPorId(self, id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM turma WHERE id = ?;", (id,))
        row = cur.fetchone()

        if row:
            return self.criarDeRow(row)
        return None

    def buscarPorProfessor(self, professor: str):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM turma WHERE professor LIKE ?;", (f'%{professor}%',))
        rows = cur.fetchall()

        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado

    def buscarPorNivel(self, nivel_id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM turma WHERE nivel_id = ?;", (nivel_id,))
        rows = cur.fetchall()

        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado

    def listarTodas(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM turma ORDER BY nivel_id, horario;")
        rows = cur.fetchall()

        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado

    def criarDeRow(self, row):
        # Buscar o nível usando o NivelDAO
        nivel = self.nivelDao.buscarPorId(row['nivel_id'])
        
        return Turma(
            id=row['id'],
            horario=row['horario'],
            nivel=nivel,
            professor=row['professor']
        )

    def deletar(self, turma: Turma):
        if turma.id is None:
            return False

        cur = self.db.cursor()
        cur.execute("DELETE FROM turma WHERE id = ?;", (turma.id,))
    
        return cur.rowcount > 0