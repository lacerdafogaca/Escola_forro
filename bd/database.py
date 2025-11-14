"""
Classe para gerenciar conexão com o banco de dados SQLite
"""
import sqlite3

class DatabaseConnection:
    def __init__(self, dbPath: str = 'exemplo_bd.db'):
        self.dbPath = dbPath
        self.conn = None

    def conectar(self):
        if self.conn is None:
            # isolation_level=None ativa autocommit (cada operação é commitada automaticamente)
            self.conn = sqlite3.connect(self.dbPath, isolation_level=None)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn

    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def cursor(self):
        """Retorna um cursor para executar queries"""
        if self.conn is None:
            self.conectar()
        return self.conn.cursor()

    def criarTabelas(self):
        cur = self.cursor()
        
        # Tabela categoria
        cur.execute("""
        CREATE TABLE IF NOT EXISTS categoria(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
        );
        """)
        
        # Tabela pessoa
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pessoa(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email VARCHAR(100) UNIQUE,
                data_nascimento VARCHAR(20),
                telefone VARCHAR(20),
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categoria(id)
        );
        """)
        
        # Tabela turma (corrigida)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS turma(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                horario VARCHAR(30) NOT NULL,
                nivel VARCHAR(30) NOT NULL,
                professor TEXT NOT NULL
        );
        """)
        
        # Tabela login
        cur.execute("""
        CREATE TABLE IF NOT EXISTS login(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(100) UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                salt BLOB NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES pessoa(id)
        );
        """)

        # Tabela Inscrição
        cur.execute("""
        CREATE TABLE IF NOT EXISTS inscricao(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno TEXT NOT NULL,
                nivel VARCHAR(30) NOT NULL,       
                data VARCHAR(30) NOT NULL,
                posicao VARCHAR(30),
                aluno_id INTEGER,
                FOREIGN KEY (aluno_id) REFERENCES pessoa(id)
        ) """)

    def limparDados(self):
        """Remove todos os dados das tabelas"""
        cur = self.cursor()
        cur.execute("DELETE FROM login;")
        cur.execute("DELETE FROM turma;")
        cur.execute("DELETE FROM pessoa;")
        cur.execute("DELETE FROM categoria;")
        cur.execute("DELETE FROM inscricao;")
        cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('pessoa', 'categoria', 'turma', 'login','inscricao');")