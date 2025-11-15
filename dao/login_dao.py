"""
DAO (Data Access Object) para operações de banco de dados da tabela login
"""
from bd.database import DatabaseConnection
from model.Login import Login

class LoginDAO:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def salvar(self, login: Login):
        """Salva ou atualiza um login no banco"""
        cur = self.db.cursor()

        if login.id is None:
            # INSERT
            cur.execute("""
                INSERT INTO login (email, senha, salt, usuario_id)
                VALUES (?, ?, ?, ?);
            """, (login.email, login.senha, login.salt, login.usuario_id))

            login.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("""
                UPDATE login SET email = ?, senha = ?, salt = ?, usuario_id = ?
                WHERE id = ?;
            """, (login.email, login.senha, login.salt, login.usuario_id, login.id))

        return login.id

    def buscarPorId(self, id: int):
        """Busca um login por ID"""
        cur = self.db.cursor()
        cur.execute("SELECT * FROM login WHERE id = ?;", (id,))
        row = cur.fetchone()

        if row:
            return self.criarDeRow(row)
        return None

    def buscarPorEmail(self, email: str):
        """Busca um login por email"""
        cur = self.db.cursor()
        cur.execute("SELECT * FROM login WHERE email = ?;", (email,))
        row = cur.fetchone()

        if row:
            return self.criarDeRow(row)
        return None

    def buscarPorUsuarioId(self, usuario_id: int):
        """Busca um login pelo ID do usuário"""
        cur = self.db.cursor()
        cur.execute("SELECT * FROM login WHERE usuario_id = ?;", (usuario_id,))
        row = cur.fetchone()

        if row:
            return self.criarDeRow(row)
        return None

    def listarTodos(self):
        """Lista todos os logins cadastrados"""
        cur = self.db.cursor()
        cur.execute("SELECT * FROM login ORDER BY email;")
        rows = cur.fetchall()

        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado

    def criarDeRow(self, row):
        """Cria um objeto Login a partir de uma row do banco"""
        # Criar o login sem passar senha no construtor
        # pois a senha já está hasheada no banco
        login = object.__new__(Login)
        
        # Definir atributos privados diretamente
        login._Login__id = row['id']
        login._Login__email = row['email']
        login._Login__senha = row['senha']
        login._Login__salt = row['salt']
        login._Login__usuario_id = row['usuario_id']
        
        return login

    def deletar(self, login: Login):
        """Deleta um login do banco"""
        if login.id is None:
            return False

        cur = self.db.cursor()
        cur.execute("DELETE FROM login WHERE id = ?;", (login.id,))

        return cur.rowcount > 0

    def emailExiste(self, email: str):
        """Verifica se um email já está cadastrado"""
        cur = self.db.cursor()
        cur.execute("SELECT COUNT(*) as total FROM login WHERE email = ?;", (email,))
        row = cur.fetchone()
        return row['total'] > 0