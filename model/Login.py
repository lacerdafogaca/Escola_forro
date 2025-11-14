import hashlib
import os

class Login:
    def __init__(self, id, email, senha, usuario_id):
        self.__id = id
        self.__email = email
        self.__usuario_id = usuario_id
        self.__salt = os.urandom(16)  # Gera um salt aleatório de 16 bytes 
        self.__senha = self.gerar_hash_senha(senha) 
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, value):
        self.__senha = value
    
    @property
    def usuario_id(self):
        return self.__usuario_id
    
    @usuario_id.setter
    def usuario_id(self, value):
        self.__usuario_id = value

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
