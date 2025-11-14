"""
DAO (Data Access Object) para operações do banco de dados da tabela nivel
"""
from bd.database import DatabaseConnection
from model.nivel import Nivel

class NivelDAO:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def salvar(self, nivel: Nivel):
        cur = self.db.cursor()

        if nivel.id is None:
            # INSERT
            cur.execute("INSERT INTO nivel (nome) VALUES (?);", (nivel.nome,))
            nivel.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("UPDATE nivel SET nome = ? WHERE id = ?;", (nivel.nome, nivel.id))

        return nivel.id

    def buscarPorId(self, id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM nivel WHERE id = ?;", (id,))
        row = cur.fetchone()

        if row:
            return self.criarDeRow(row)
        return None

    def buscarPorNome(self, nome: str):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM nivel WHERE nome = ?;", (nome,))
        row = cur.fetchone()

        if row:
            return self.criarDeRow(row)
        return None

    def listarTodas(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM nivel ORDER BY nome;")
        rows = cur.fetchall()

        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado

    def criarDeRow(self, row):
        return Nivel(
            id=row['id'],
            nome=row['nome']
        )

    def deletar(self, nivel: Nivel):
        if nivel.id is None:
            return False

        cur = self.db.cursor()
        cur.execute("DELETE FROM nivel WHERE id = ?;", (nivel.id,))

        return cur.rowcount > 0

