"""
Serviço para interação do usuário via linha de comando com a entidade Turma
"""
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection
from dao.turma_dao import TurmaDAO
from dao.pessoa_dao import PessoaDAO
from model.turma import Turma


class TurmaService:

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.turmaDao = TurmaDAO(db)
        self.pessoaDao = PessoaDAO(db)

    def exibirMenu(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*50)
        print("  SISTEMA DE GERENCIAMENTO DE TURMAS ")
        print("="*50)
        print("1. Criar turma")
        print("2. Listar todas as turmas")
        print("3. Buscar turma por ID")
        print("4. Buscar turmas por professor")
        print("5. Buscar turmas por nível")
        print("6. Atualizar turma")
        print("7. Deletar turma")
        print("0. Sair")
        print("="*50)

    def listarProfessoresDisponiveis(self):
        """Lista todas as pessoas disponíveis para serem professores"""
        pessoas = self.pessoaDao.listarTodas()
        if not pessoas:
            print("⚠️  Nenhuma pessoa cadastrada. Cadastre uma pessoa primeiro!")
            return None

        print("\nPessoas disponíveis:")
        print("-"*50)
        for pessoa in pessoas:
            print(f"  {pessoa.id}. {pessoa.nome} ({pessoa.email})")
        print("-"*50)
        return pessoas

    def selecionarProfessor(self):
        """Solicita ao usuário que selecione um professor"""
        pessoas = self.listarProfessoresDisponiveis()
        if not pessoas:
            return None

        try:
            pessoaIdStr = input("Digite o ID do professor: ").strip()
            pessoaId = int(pessoaIdStr)

            pessoa = self.pessoaDao.buscarPorId(pessoaId)
            if not pessoa:
                print(f"❌ Erro: Pessoa com ID {pessoaId} não encontrada!")
                return None

            return pessoa.nome
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
            return None

    def criarTurma(self):
        """Solicita dados do usuário e cria uma nova turma"""
        print("\n--- CRIAR TURMA ---")
        
        horario = input("Digite o horário da turma (ex: 08:00-10:00): ").strip()
        if not horario:
            print("❌ Erro: O horário não pode ser vazio!")
            return

        print("\nNíveis disponíveis: Básico, Intermediário, Avançado")
        nivel = input("Digite o nível da turma: ").strip()
        if not nivel:
            print("❌ Erro: O nível não pode ser vazio!")
            return

        # Selecionar professor
        professor = self.selecionarProfessor()
        if not professor:
            return

        try:
            # Criar nova turma
            turma = Turma(id=None, horario=horario, nivel=nivel, professor=professor)
            turmaId = self.turmaDao.salvar(turma)
            print(f"\n✅ Turma criada com sucesso!")
            self.exibirDetalhesTurma(turma)

        except Exception as e:
            print(f"❌ Erro ao criar turma: {e}")

    def exibirDetalhesTurma(self, turma: Turma):
        """Exibe os detalhes completos de uma turma"""
        print(f"\n   ID: {turma.id}")
        print(f"   Horário: {turma.horario}")
        print(f"   Nível: {turma.nivel}")
        print(f"   Professor: {turma.professor}")

    def listarTurmas(self):
        """Lista todas as turmas cadastradas"""
        print("\n--- LISTAR TODAS AS TURMAS ---")

        try:
            turmas = self.turmaDao.listarTodas()

            if not turmas:
                print("⚠️  Nenhuma turma cadastrada.")
                return

            print(f"\nTotal de turmas: {len(turmas)}")
            print("\n" + "-"*80)
            print(f"{'ID':<5} | {'Horário':<15} | {'Nível':<15} | {'Professor':<30}")
            print("-"*80)

            for turma in turmas:
                print(f"{turma.id:<5} | {turma.horario:<15} | {turma.nivel:<15} | {turma.professor[:29]:<30}")

            print("-"*80)

        except Exception as e:
            print(f"❌ Erro ao listar turmas: {e}")

    def buscarPorId(self):
        """Solicita um ID e busca a turma correspondente"""
        print("\n--- BUSCAR TURMA POR ID ---")

        try:
            idStr = input("Digite o ID da turma: ").strip()
            turmaId = int(idStr)

            turma = self.turmaDao.buscarPorId(turmaId)

            if turma:
                print("\n✅ Turma encontrada:")
                self.exibirDetalhesTurma(turma)
            else:
                print(f"⚠️  Turma com ID {turmaId} não encontrada.")

        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao buscar turma: {e}")

    def buscarPorProfessor(self):
        """Solicita um professor e busca turmas correspondentes"""
        print("\n--- BUSCAR TURMAS POR PROFESSOR ---")

        professor = input("Digite o nome (ou parte do nome) do professor: ").strip()

        if not professor:
            print("❌ Erro: O nome não pode ser vazio!")
            return

        try:
            turmas = self.turmaDao.buscarPorProfessor(professor)

            if turmas:
                print(f"\n✅ {len(turmas)} turma(s) encontrada(s):")
                print("\n" + "-"*80)
                for turma in turmas:
                    print(f"ID: {turma.id} | {turma.horario} | {turma.nivel} | Professor: {turma.professor}")
                print("-"*80)
            else:
                print(f"⚠️  Nenhuma turma encontrada com professor contendo '{professor}'.")

        except Exception as e:
            print(f"❌ Erro ao buscar turmas: {e}")

    def buscarPorNivel(self):
        """Lista turmas de um nível específico"""
        print("\n--- BUSCAR TURMAS POR NÍVEL ---")

        print("Níveis disponíveis: Básico, Intermediário, Avançado")
        nivel = input("Digite o nível: ").strip()

        if not nivel:
            print("❌ Erro: O nível não pode ser vazio!")
            return

        try:
            turmas = self.turmaDao.buscarPorNivel(nivel)

            if turmas:
                print(f"\n✅ {len(turmas)} turma(s) encontrada(s) no nível '{nivel}':")
                print("\n" + "-"*80)
                for turma in turmas:
                    print(f"ID: {turma.id} | {turma.horario} | Professor: {turma.professor}")
                print("-"*80)
            else:
                print(f"⚠️  Nenhuma turma encontrada no nível '{nivel}'.")

        except Exception as e:
            print(f"❌ Erro ao buscar turmas: {e}")

    def atualizarTurma(self):
        """Solicita dados do usuário e atualiza uma turma existente"""
        print("\n--- ATUALIZAR TURMA ---")

        try:
            idStr = input("Digite o ID da turma a atualizar: ").strip()
            turmaId = int(idStr)

            # Buscar a turma existente
            turma = self.turmaDao.buscarPorId(turmaId)

            if not turma:
                print(f"⚠️  Turma com ID {turmaId} não encontrada.")
                return

            print(f"\nTurma atual:")
            self.exibirDetalhesTurma(turma)

            print("\nDigite os novos dados (ou Enter para manter o valor atual):")

            # Horário
            novoHorario = input(f"Horário [{turma.horario}]: ").strip()
            if novoHorario:
                turma.horario = novoHorario

            # Nível
            novoNivel = input(f"Nível [{turma.nivel}]: ").strip()
            if novoNivel:
                turma.nivel = novoNivel

            # Professor
            print(f"\nProfessor atual: {turma.professor}")
            trocarProfessor = input("Deseja trocar o professor? (s/N): ").strip().lower()
            if trocarProfessor == 's':
                novoProfessor = self.selecionarProfessor()
                if novoProfessor:
                    turma.professor = novoProfessor

            self.turmaDao.salvar(turma)
            print(f"\n✅ Turma atualizada com sucesso!")
            print("\nDados atualizados:")
            self.exibirDetalhesTurma(turma)

        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao atualizar turma: {e}")

    def deletarTurma(self):
        """Solicita um ID e deleta a turma correspondente"""
        print("\n--- DELETAR TURMA ---")

        try:
            idStr = input("Digite o ID da turma a deletar: ").strip()
            turmaId = int(idStr)

            # Buscar a turma existente
            turma = self.turmaDao.buscarPorId(turmaId)

            if not turma:
                print(f"⚠️  Turma com ID {turmaId} não encontrada.")
                return

            print(f"\nTurma a ser deletada:")
            self.exibirDetalhesTurma(turma)

            confirmacao = input("\n⚠️  Tem certeza que deseja deletar esta turma? (s/N): ").strip().lower()

            if confirmacao != 's':
                print("❌ Operação cancelada.")
                return

            sucesso = self.turmaDao.deletar(turma)

            if sucesso:
                print(f"\n✅ Turma deletada com sucesso!")
            else:
                print(f"\n❌ Erro ao deletar turma.")

        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao deletar turma: {e}")

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
                    self.criarTurma()
                elif opcao == '2':
                    self.listarTurmas()
                elif opcao == '3':
                    self.buscarPorId()
                elif opcao == '4':
                    self.buscarPorProfessor()
                elif opcao == '5':
                    self.buscarPorNivel()
                elif opcao == '6':
                    self.atualizarTurma()
                elif opcao == '7':
                    self.deletarTurma()
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
        service = TurmaService(db)
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