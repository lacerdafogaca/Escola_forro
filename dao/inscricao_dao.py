"""
DAO (Data Access Object) para operações de banco de dados da tabela inscricao
"""
from bd.database import DatabaseConnection
from model.inscricao import Inscricao

class InscricaoDAO:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def salvar(self, inscricao: Inscricao):
        cur = self.db.cursor()

        if inscricao.id is None:
            # INSERT
            cur.execute("INSERT INTO inscricao (aluno) VALUES (?);", (inscricao.aluno,))
            inscricao.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("UPDATE inscricao SET aluno = ? WHERE id = ?;", (inscricao.aluno, inscricao.id))

        return inscricao.id

    def buscarPorId(self, id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM inscricao WHERE id = ?;", (id,))
        row = cur.fetchone()

        if row:
            return self.criarDeRow(row)
        return None

    def buscarPorAluno(self, aluno: str):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM inscricao WHERE aluno = ?;", (aluno,))
        row = cur.fetchone()

        if row:
            return self.criarDeRow(row)
        return None

    def listarTodas(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM inscricao ORDER BY data;")
        rows = cur.fetchall()

        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado

    def criarDeRow(self, row):
        return Inscricao(
            id=row['id'],
            aluno=row['aluno'],
            data=row['data'],
            nivel=row['nivel'],
            posicao=row['posicao'],
            aluno_id=row['aluno_id']
        )

    def deletar(self, inscricao: Inscricao):
        if inscricao.id is None:
            return False

        cur = self.db.cursor()
        cur.execute("DELETE FROM inscricao WHERE id = ?;", (inscricao.id,))

        return cur.rowcount > 0

