"""
Serviço para interação do usuário via linha de comando com a entidade Login
"""
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection
from dao.login_dao import LoginDAO
from dao.pessoa_dao import PessoaDAO
from model.Login import Login


class LoginService:

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.loginDao = LoginDAO(db)
        self.pessoaDao = PessoaDAO(db)
        self.usuario_logado = None

    def exibirMenu(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*50)
        print("  SISTEMA DE GERENCIAMENTO DE LOGIN")
        print("="*50)
        print("1. Criar login")
        print("2. Fazer login")
        print("3. Listar todos os logins")
        print("4. Buscar login por email")
        print("5. Trocar senha")
        print("6. Deletar login")
        print("0. Sair")
        print("="*50)

    def listarPessoasDisponiveis(self):
        """Lista todas as pessoas disponíveis para criar login"""
        pessoas = self.pessoaDao.listarTodas()
        if not pessoas:
            print("⚠️  Nenhuma pessoa cadastrada. Cadastre uma pessoa primeiro!")
            return None

        # Filtrar pessoas que já têm login
        pessoasSemLogin = []
        for pessoa in pessoas:
            loginExistente = self.loginDao.buscarPorUsuarioId(pessoa.id)
            if not loginExistente:
                pessoasSemLogin.append(pessoa)

        if not pessoasSemLogin:
            print("⚠️  Todas as pessoas já possuem login cadastrado!")
            return None

        print("\nPessoas sem login:")
        print("-"*50)
        for pessoa in pessoasSemLogin:
            print(f"  {pessoa.id}. {pessoa.nome} ({pessoa.email})")
        print("-"*50)
        return pessoasSemLogin

    def selecionarPessoa(self):
        """Solicita ao usuário que selecione uma pessoa"""
        pessoas = self.listarPessoasDisponiveis()
        if not pessoas:
            return None

        try:
            pessoaIdStr = input("Digite o ID da pessoa: ").strip()
            pessoaId = int(pessoaIdStr)

            pessoa = self.pessoaDao.buscarPorId(pessoaId)
            if not pessoa:
                print(f"❌ Erro: Pessoa com ID {pessoaId} não encontrada!")
                return None

            # Verificar se já tem login
            loginExistente = self.loginDao.buscarPorUsuarioId(pessoaId)
            if loginExistente:
                print(f"❌ Erro: Esta pessoa já possui um login cadastrado!")
                return None

            return pessoa
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
            return None

    def criarLogin(self):
        """Solicita dados do usuário e cria um novo login"""
        print("\n--- CRIAR LOGIN ---")

        # Selecionar pessoa
        pessoa = self.selecionarPessoa()
        if not pessoa:
            return

        email = input(f"Digite o email de login [{pessoa.email}]: ").strip()
        if not email:
            email = pessoa.email

        # Verificar se o email já está em uso
        if self.loginDao.emailExiste(email):
            print(f"❌ Erro: Já existe um login com o email '{email}'")
            return

        senha = input("Digite a senha: ").strip()
        if not senha:
            print("❌ Erro: A senha não pode ser vazia!")
            return

        confirmarSenha = input("Confirme a senha: ").strip()
        if senha != confirmarSenha:
            print("❌ Erro: As senhas não coincidem!")
            return

        try:
            login = Login(
                id=None,
                email=email,
                senha=senha,
                usuario_id=pessoa.id
            )

            loginId = self.loginDao.salvar(login)
            print(f"\n✅ Login criado com sucesso!")
            print(f"   ID: {loginId}")
            print(f"   Email: {login.email}")
            print(f"   Usuário: {pessoa.nome}")

        except Exception as e:
            print(f"❌ Erro ao criar login: {e}")

    def fazerLogin(self):
        """Realiza o processo de autenticação"""
        print("\n--- FAZER LOGIN ---")

        email = input("Email: ").strip()
        if not email:
            print("❌ Erro: O email não pode ser vazio!")
            return

        senha = input("Senha: ").strip()
        if not senha:
            print("❌ Erro: A senha não pode ser vazia!")
            return

        try:
            login = self.loginDao.buscarPorEmail(email)

            if not login:
                print("❌ Email ou senha incorretos!")
                return

            if login.verificar_senha(senha):
                pessoa = self.pessoaDao.buscarPorId(login.usuario_id)
                self.usuario_logado = pessoa
                print(f"\n✅ Login realizado com sucesso!")
                print(f"   Bem-vindo(a), {pessoa.nome}!")
            else:
                print("❌ Email ou senha incorretos!")

        except Exception as e:
            print(f"❌ Erro ao fazer login: {e}")

    def listarLogins(self):
        """Lista todos os logins cadastrados"""
        print("\n--- LISTAR TODOS OS LOGINS ---")

        try:
            logins = self.loginDao.listarTodos()

            if not logins:
                print("⚠️  Nenhum login cadastrado.")
                return

            print(f"\nTotal de logins: {len(logins)}")
            print("\n" + "-"*80)
            print(f"{'ID':<5} | {'Email':<30} | {'ID Usuário':<15}")
            print("-"*80)

            for login in logins:
                pessoa = self.pessoaDao.buscarPorId(login.usuario_id)
                nome_usuario = pessoa.nome if pessoa else "N/A"
                print(f"{login.id:<5} | {login.email:<30} | {login.usuario_id:<15}")

            print("-"*80)

        except Exception as e:
            print(f"❌ Erro ao listar logins: {e}")

    def buscarPorEmail(self):
        """Solicita um email e busca o login correspondente"""
        print("\n--- BUSCAR LOGIN POR EMAIL ---")

        email = input("Digite o email: ").strip()

        if not email:
            print("❌ Erro: O email não pode ser vazio!")
            return

        try:
            login = self.loginDao.buscarPorEmail(email)

            if login:
                pessoa = self.pessoaDao.buscarPorId(login.usuario_id)
                print("\n✅ Login encontrado:")
                print(f"   ID: {login.id}")
                print(f"   Email: {login.email}")
                print(f"   Usuário: {pessoa.nome if pessoa else 'N/A'}")
                print(f"   ID Usuário: {login.usuario_id}")
            else:
                print(f"⚠️  Login com email '{email}' não encontrado.")

        except Exception as e:
            print(f"❌ Erro ao buscar login: {e}")

    def trocarSenha(self):
        """Permite ao usuário trocar a senha"""
        print("\n--- TROCAR SENHA ---")

        email = input("Email: ").strip()
        if not email:
            print("❌ Erro: O email não pode ser vazio!")
            return

        senhaAtual = input("Senha atual: ").strip()
        if not senhaAtual:
            print("❌ Erro: A senha não pode ser vazia!")
            return

        try:
            login = self.loginDao.buscarPorEmail(email)

            if not login:
                print("❌ Email ou senha incorretos!")
                return

            if not login.verificar_senha(senhaAtual):
                print("❌ Email ou senha incorretos!")
                return

            novaSenha = input("Nova senha: ").strip()
            if not novaSenha:
                print("❌ Erro: A nova senha não pode ser vazia!")
                return

            confirmarNovaSenha = input("Confirme a nova senha: ").strip()
            if novaSenha != confirmarNovaSenha:
                print("❌ Erro: As senhas não coincidem!")
                return

            login.trocar_senha(novaSenha)
            self.loginDao.salvar(login)
            print("\n✅ Senha alterada com sucesso!")

        except Exception as e:
            print(f"❌ Erro ao trocar senha: {e}")

    def deletarLogin(self):
        """Solicita um email e deleta o login correspondente"""
        print("\n--- DELETAR LOGIN ---")

        email = input("Digite o email do login a deletar: ").strip()

        if not email:
            print("❌ Erro: O email não pode ser vazio!")
            return

        try:
            login = self.loginDao.buscarPorEmail(email)

            if not login:
                print(f"⚠️  Login com email '{email}' não encontrado.")
                return

            pessoa = self.pessoaDao.buscarPorId(login.usuario_id)
            print(f"\nLogin a ser deletado:")
            print(f"   ID: {login.id}")
            print(f"   Email: {login.email}")
            print(f"   Usuário: {pessoa.nome if pessoa else 'N/A'}")

            confirmacao = input("\n⚠️  Tem certeza que deseja deletar este login? (s/N): ").strip().lower()

            if confirmacao != 's':
                print("❌ Operação cancelada.")
                return

            sucesso = self.loginDao.deletar(login)

            if sucesso:
                print(f"\n✅ Login deletado com sucesso!")
            else:
                print(f"\n❌ Erro ao deletar login.")

        except Exception as e:
            print(f"❌ Erro ao deletar login: {e}")

    def executar(self):
        """Método principal que executa o loop do menu"""
        try:
            while True:
                self.exibirMenu()
                opcao = input("\nEscolha uma opção: ").strip()

                if opcao == '0':
                    print("\n👋 Encerrando o sistema...")
                    break
                elif opcao == '1':
                    self.criarLogin()
                elif opcao == '2':
                    self.fazerLogin()
                elif opcao == '3':
                    self.listarLogins()
                elif opcao == '4':
                    self.buscarPorEmail()
                elif opcao == '5':
                    self.trocarSenha()
                elif opcao == '6':
                    self.deletarLogin()
                else:
                    print("❌ Opção inválida! Tente novamente.")

                input("\nPressione Enter para continuar...")

        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Função principal para executar o serviço"""
    db = DatabaseConnection('exemplo_bd.db')

    try:
        # Conectar ao banco
        db.conectar()

        # Garantir que as tabelas existam
        db.criarTabelas()

        # Criar e executar o serviço
        service = LoginService(db)
        service.executar()

    except Exception as e:
        print(f"❌ Erro ao inicializar o sistema: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.fechar()
        print("✓ Conexão com banco de dados encerrada.")


if __name__ == "__main__":
    main()