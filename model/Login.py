import hashlib
import os

class Login:
    def __init__(self, id, email, senha, usuario_id):
        self.id = id
        self.email = email
        self.usuario_id = usuario_id
        self.salt = os.urandom(16)  # Gera um salt aleatório de 16 bytes 
        self.senha = self.gerar_hash_senha(senha) 
    
    # Método para gerar o hash da senha
    def gerar_hash_senha(self, senha):
        senha_salt = self.salt + senha.encode('utf-8')
        hash_senha = hashlib.sha256(senha_salt).hexdigest()
        return hash_senha
    
    # Método para verificar a senha fornecida com o hash armazenado
    def verificar_senha(self, senha_digitada):
        senha_salt = self.salt + senha_digitada.encode('utf-8')
        hash_digitado = hashlib.sha256(senha_salt).hexdigest()
        return hash_digitado == self.senha
    
    def autenticar_login(self, email_digitado, senha_digitada):
        if self.email == email_digitado and self.verificar_senha(senha_digitada):
            print("Login realizado com sucesso!")
            return True
        else:
            print("Erro ao fazer login. Tente novamente.")
            return False
    
    def trocar_senha(self, nova_senha):
        self.senha = self.gerar_hash_senha(nova_senha)
        print("Senha alterada com sucesso!")

    def __str__(self):
        return f"Login(id={self.id}, email={self.email}, usuario_id={self.usuario_id})"
