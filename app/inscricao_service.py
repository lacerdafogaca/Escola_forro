"""
Serviço para interação do usuário via linha de comando com a entidade inscrica
"""
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection
from dao.inscricao_dao import InscricaoDAO
from dao.pessoa_dao import PessoaDAO
from model.inscricao import Inscricao


class InscricaoService:

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.inscricaoDao = InscricaoDAO(db)
        self.pessoaDao = PessoaDAO(db)

    def exibirMenu(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*50)
        print("  SISTEMA DE GERENCIAMENTO DE INSCRICAO ")
        print("="*50)
        print("1. Criar inscricao")
        print("2. Listar todas as inscricao")
        print("3. Buscar inscricao por ID")
        print("4. Buscar inscricao por aluno")
        print("5. Atualizar inscricao")
        print("6. Deletar inscricao")
        print("0. Sair")
        print("="*50)


    def criarInscricao(self):
        """Solicita dados do usuário e cria uma nova inscricao"""
        print("\n--- CRIAR INSCRICAO ---")
        
        aluno = input("Digite o nome do aluno: ").strip()
        if not aluno:
            print("❌ Erro: O aluno não pode ser vazio!")
            return

        print("\nNíveis disponíveis: Básico, Intermediário, Avançado")
        nivel = input("Digite o nível da avaliação: ").strip()
        if not nivel:
            print("❌ Erro: O nível não pode ser vazio!")
            return
        
        data = input("Digite a data da avaliação (ex: 08:00-10:00):").strip()
        if not data:
            print("❌ Erro: A data não pode ser vazio!")
            return

        print("\nPosições disponíveis: Condutor, Conduzido")    
        posicao = input("Digite a posição durante a avaliação:").strip()
        if not posicao:
            print("❌ Erro: A posicao não pode ser vazio!")
            return

        try:
            # Criar nova Inscricao
            inscricao = Inscricao(id=None, aluno= aluno, data=data, nivel=nivel, posicao=posicao)
            inscricaoId = self.inscricaoDao.salvar(inscricao)
            print(f"\n✅ Inscricao criada com sucesso!")
            self.exibirDetalhesInscricao(inscricao)

        except Exception as e:
            print(f"❌ Erro ao criar Inscricao: {e}")

    def exibirDetalhesInscricao(self, inscricao: Inscricao):
        """Exibe os detalhes completos da Inscricao"""
        print(f"\n   ID: {inscricao.id}")
        print(f"   Aluno: {inscricao.aluno}")
        print(f"   Nível: {inscricao.nivel}") 
        print(f"   Data: {inscricao.data}")
        print(f"   Posicao: {inscricao.posicao}")

    def listarInscricao(self):
        """Lista todas as inscricoes cadastradas"""
        print("\n--- LISTAR TODAS AS INSCRIÇÕES ---")

        try:
            inscricoes = self.inscricaoDao.listarTodas()

            if not inscricoes:
                print("⚠️  Nenhuma inscrição cadastrada.")
                return

            print(f"\nTotal de inscricoes: {len(inscricoes)}")
            print("\n" + "-"*80)
            print(f"{'ID':<5} | {'Aluno':<30} | {'Nível':<15} |{'Data':<15} |  {'Posicao':<30}")
            print("-"*80)

            for inscricao in inscricoes:
                print(f"{inscricao.id:<5} | {inscricao.aluno} | {inscricao.nivel:<15} |{inscricao.data:<15} |  {inscricao.posicao[:29]:<30}")

            print("-"*80)

        except Exception as e:
            print(f"❌ Erro ao listar inscrições: {e}")

    def buscarPorId(self):
        """Solicita um ID e busca a inscricão correspondente"""
        print("\n--- BUSCAR INSCRIÇÃO POR ID ---")

        try:
            idStr = input("Digite o ID da inscrição: ").strip()
            inscricaoId = int(idStr)

            inscricao = self.inscricaoDao.buscarPorId(inscricaoId)

            if inscricao:
                print("\n✅ Inscrição encontrada:")
                self.exibirDetalhesInscricao(inscricao)
            else:
                print(f"⚠️  Inscrição com ID {inscricaoId} não encontrada.")

        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao buscar Inscrição: {e}")

    def buscarPorAluno(self):
        """Solicita um aluno e busca Inscrição correspondentes"""
        print("\n--- BUSCAR INSCRIÇÃO POR ALUNO ---")

        aluno = input("Digite o nome (ou parte do nome) do aluno: ").strip()

        if not aluno:
            print("❌ Erro: O nome não pode ser vazio!")
            return

        try:
            inscricoes = self.inscricaoDao.buscarPorAluno(aluno)

            if inscricoes:
                print(f"\n✅ {len(inscricoes)} incrições encontradas:")
                print("\n" + "-"*80)
                for inscricao in inscricoes:
                     print(f"{inscricao.id:<5} | {inscricao.aluno} | {inscricao.nivel:<15} |{inscricao.data:<15} |  {inscricao.posicao[:29]:<30}")
                print("-"*80)
            else:
                print(f"⚠️  Nenhuma inscrição encontrada para '{aluno}'.")

        except Exception as e:
            print(f"❌ Erro ao buscar inscrição: {e}")

    def atualizarInscricao(self):
        """Solicita dados do usuário e atualiza uma Inscrição existente"""
        print("\n--- ATUALIZAR INSCRIÇÃO ---")

        try:
            idStr = input("Digite o ID da Inscrição a atualizar: ").strip()
            inscricaoId = int(idStr)

            # Buscar a Inscrição existente
            inscricao = self.inscricaoDao.buscarPorId(inscricaoId)

            if not inscricao:
                print(f"⚠️  Inscricao com ID {inscricaoId} não encontrada.")
                return

            print(f"\nInscrição atual:")
            self.exibirDetalhesInscricao(inscricao)

            print("\nDigite os novos dados (ou Enter para manter o valor atual):")

            # Data
            print(f"\nData atual: {inscricao.data}")
            trocarData = input("Deseja trocar a data? (s/N): ").strip().lower()
            if trocarData == 's':
                novaData = input(f"Data [{inscricao.data}]: ").strip()
                if novoData:
                    inscricao.data = novaData

            # Nível
            print(f"\nNível atual: {inscricao.nivel}")
            trocarNivel = input("Deseja trocar o nível? (s/N): ").strip().lower()
            if trocarNivel == 's':
                novoNivel = input(f"Nível [{inscricao.nivel}]: ").strip()
                if novoNivel:
                    inscricao.nivel = novoNivel

            # Posição
            print(f"\nPosição atual: {inscricao.posicao}")
            trocarPosicao = input("Deseja trocar a posição? (s/N): ").strip().lower()
            if trocarPosicao == 's':
                novaPosicao = input(f"Posição [{inscricao.posicao}]: ").strip()
                if novaPosicao:
                    inscricao.posicao = novaPosicao

            self.inscricaoDao.salvar(inscricao)
            print(f"\n✅ Inscrição atualizada com sucesso!")
            print("\nDados atualizados:")
            self.exibirDetalhesInscricao(inscricao)

        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao atualizar inscrição: {e}")

    def deletarInscricao(self):
        """Solicita um ID e deleta a inscrição correspondente"""
        print("\n--- DELETAR INSCRIÇÃO ---")

        try:
            idStr = input("\nDigite o ID da inscrição a deletar: ").strip()
            inscricaoId = int(idStr)

            # Buscar a inscrição existente
            inscricao = self.inscricaoDao.buscarPorId(inscricaoId)

            if not inscricao:
                print(f"⚠️  Inscrição com ID {inscricaoId} não encontrada.")
                return

            print(f"\nInscrição a ser deletada:")
            self.exibirDetalhesInscricao(inscricao)

            confirmacao = input("\n⚠️  Tem certeza que deseja deletar esta inscrição? (s/N): ").strip().lower()

            if confirmacao != 's':
                print("❌ Operação cancelada.")
                return

            sucesso = self.inscricaoDao.deletar(inscricao)

            if sucesso:
                print(f"\n✅ Inscrição deletada com sucesso!")
            else:
                print(f"\n❌ Erro ao deletar Inscrição.")

        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao deletar Inscrição: {e}")

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
                    self.criarInscricao()
                elif opcao == '2':
                    self.listarInscricao()
                elif opcao == '3':
                    self.buscarPorId()
                elif opcao == '4':
                    self.buscarPorAluno()
                elif opcao == '5':
                    self.atualizarInscricao()
                elif opcao == '6':
                    self.deletarInscricao()
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
        service = InscricaoService(db)
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