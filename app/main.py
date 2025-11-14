"""
Sistema principal de gerenciamento com menu unificado
Permite ao usuário escolher entre gerenciar Categorias, Pessoas, Turmas e Logins
"""
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection

# Importar serviços
from categoria_service import CategoriaService
from pessoa_service import PessoaService
from turma_service import TurmaService
from login_service import LoginService
from nivel_service import NivelService

class SistemaPrincipal:
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.categoriaService = CategoriaService(db)
        self.pessoaService = PessoaService(db)
        self.turmaService = TurmaService(db)
        self.loginService = LoginService(db)
        self.nivelService = NivelService(db)
    
    def exibirMenuPrincipal(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*50)
        print("     SISTEMA DE GERENCIAMENTO COMPLETO")
        print("="*50)
        print("1. Gerenciar Categorias")
        print("2. Gerenciar Pessoas")
        print("3. Gerenciar Turmas")
        print("4. Gerenciar Logins")
        print("5. Gerenciar Niveis")
        print("6. Limpar todos os dados do banco")
        print("0. Sair")
        print("="*50)
    
    def limparDados(self):
        """Limpa todos os dados do banco de dados"""
        print("\n" + "="*50)
        print("  ⚠️  ATENÇÃO: LIMPAR TODOS OS DADOS")
        print("="*50)
        print("Esta operação vai deletar TODOS os dados de:")
        print("  - Logins")
        print("  - Turmas")
        print("  - Pessoas")
        print("  - Categorias")
        print("  - Niveis")
        print()
        confirmacao = input("Tem certeza que deseja continuar? Digite 'CONFIRMAR' para prosseguir: ").strip()
        
        if confirmacao == 'CONFIRMAR':
            try:
                self.db.limparDados()
                print("\n✅ Todos os dados foram removidos com sucesso!")
            except Exception as e:
                print(f"\n❌ Erro ao limpar dados: {e}")
        else:
            print("\n❌ Operação cancelada.")
    
    def executar(self):
        """Método principal que executa o loop do menu"""
        try:
            print("\n" + "="*50)
            print("     BEM-VINDO AO SISTEMA DE GERENCIAMENTO")
            print("="*50)
            print("Versão 1.0 - Sistema completo de gestão")
            print()
            
            while True:
                self.exibirMenuPrincipal()
                opcao = input("\nEscolha uma opção: ").strip()
                
                if opcao == '0':
                    print("\n👋 Encerrando o sistema...")
                    print("Obrigado por utilizar nosso sistema!")
                    break
                elif opcao == '1':
                    print("\n" + "="*50)
                    print("  ENTRANDO NO GERENCIAMENTO DE CATEGORIAS")
                    print("="*50)
                    self.categoriaService.executar()
                elif opcao == '2':
                    print("\n" + "="*50)
                    print("  ENTRANDO NO GERENCIAMENTO DE PESSOAS")
                    print("="*50)
                    self.pessoaService.executar()
                elif opcao == '3':
                    print("\n" + "="*50)
                    print("  ENTRANDO NO GERENCIAMENTO DE TURMAS")
                    print("="*50)
                    self.turmaService.executar()
                elif opcao == '4':
                    print("\n" + "="*50)
                    print("  ENTRANDO NO GERENCIAMENTO DE LOGINS")
                    print("="*50)
                    self.loginService.executar()
                elif opcao == '5':
                    print("\n" + "=" * 50)
                    print("  ENTRANDO NO GERENCIAMENTO DE NIVEIS")
                    print("=" * 50)
                    self.nivelService.executar()
                elif opcao == '6':
                    self.limparDados()
                else:
                    print("❌ Opção inválida! Tente novamente.")
                
                if opcao in ['0', '1', '2', '3', '4', '5', '6']:
                    input("\nPressione Enter para voltar ao menu principal...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Função principal para executar o sistema"""
    db = DatabaseConnection('exemplo_bd.db')
    
    try:
        # Conectar ao banco
        db.conectar()
        
        # Garantir que as tabelas existam
        db.criarTabelas()
        
        # Criar e executar o sistema principal
        sistema = SistemaPrincipal(db)
        sistema.executar()
    
    except Exception as e:
        print(f"❌ Erro ao inicializar o sistema: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.fechar()
        print("✓ Conexão com banco de dados encerrada.")


if __name__ == "__main__":
    main()