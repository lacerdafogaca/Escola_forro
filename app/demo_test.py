"""
Script de demonstração e teste do sistema
Popula o banco com dados de exemplo
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection
from dao.categoria_dao import CategoriaDAO
from dao.pessoa_dao import PessoaDAO
from dao.turma_dao import TurmaDAO
from dao.login_dao import LoginDAO
from dao.nivel_dao import NivelDAO
from model.categoria import Categoria
from model.pessoa import Pessoa
from model.turma import Turma
from model.nivel import Nivel
from model.Login import Login


def limpar_banco(db):
    """Limpa todos os dados do banco"""
    print("🗑️  Limpando banco de dados...")
    db.limparDados()
    print("✅ Banco limpo!\n")


def criar_dados_exemplo(db):
    """Cria dados de exemplo no banco"""
    print("="*60)
    print("  POPULANDO BANCO DE DADOS COM DADOS DE EXEMPLO")
    print("="*60)
    
    # DAOs
    categoriaDao = CategoriaDAO(db)
    pessoaDao = PessoaDAO(db)
    turmaDao = TurmaDAO(db)
    loginDao = LoginDAO(db)
    nivelDao = NivelDAO(db)
    
    # 1. CRIAR CATEGORIAS
    print("\n1️⃣  Criando categorias...")
    categorias = {}
    
    cat_aluno = Categoria(id=None, nome="Aluno")
    categorias['aluno'] = cat_aluno
    cat_aluno.id = categoriaDao.salvar(cat_aluno)
    print(f"   ✅ Categoria criada: {cat_aluno.nome} (ID: {cat_aluno.id})")
    
    cat_professor = Categoria(id=None, nome="Professor")
    categorias['professor'] = cat_professor
    cat_professor.id = categoriaDao.salvar(cat_professor)
    print(f"   ✅ Categoria criada: {cat_professor.nome} (ID: {cat_professor.id})")
    
    cat_admin = Categoria(id=None, nome="Administrador")
    categorias['admin'] = cat_admin
    cat_admin.id = categoriaDao.salvar(cat_admin)
    print(f"   ✅ Categoria criada: {cat_admin.nome} (ID: {cat_admin.id})")
    
    # 2. CRIAR NÍVEIS
    print("\n2️⃣  Criando níveis...")
    niveis = {}
    
    nivel_basico = Nivel(id=None, nome="Básico")
    nivel_basico.id = nivelDao.salvar(nivel_basico)
    niveis['basico'] = nivel_basico
    print(f"   ✅ Nível criado: {nivel_basico.nome} (ID: {nivel_basico.id})")
    
    nivel_intermediario = Nivel(id=None, nome="Intermediário")
    nivel_intermediario.id = nivelDao.salvar(nivel_intermediario)
    niveis['intermediario'] = nivel_intermediario
    print(f"   ✅ Nível criado: {nivel_intermediario.nome} (ID: {nivel_intermediario.id})")
    
    nivel_avancado = Nivel(id=None, nome="Avançado")
    nivel_avancado.id = nivelDao.salvar(nivel_avancado)
    niveis['avancado'] = nivel_avancado
    print(f"   ✅ Nível criado: {nivel_avancado.nome} (ID: {nivel_avancado.id})")
    
    # 3. CRIAR PESSOAS
    print("\n3️⃣  Criando pessoas...")
    pessoas = []
    
    # Professores
    prof1 = Pessoa(
        id=None,
        nome="João Silva",
        email="joao.silva@escola.com",
        categoria=categorias['professor'],
        data_nascimento="1985-03-15",
        telefone="(11) 98765-4321"
    )
    prof1.id = pessoaDao.salvar(prof1)
    pessoas.append(prof1)
    print(f"   ✅ Pessoa criada: {prof1.nome} - {prof1.categoria.nome}")
    
    prof2 = Pessoa(
        id=None,
        nome="Maria Santos",
        email="maria.santos@escola.com",
        categoria=categorias['professor'],
        data_nascimento="1990-07-22",
        telefone="(11) 98765-1234"
    )
    prof2.id = pessoaDao.salvar(prof2)
    pessoas.append(prof2)
    print(f"   ✅ Pessoa criada: {prof2.nome} - {prof2.categoria.nome}")
    
    # Alunos
    aluno1 = Pessoa(
        id=None,
        nome="Pedro Costa",
        email="pedro.costa@aluno.com",
        categoria=categorias['aluno'],
        data_nascimento="2005-01-10",
        telefone="(11) 91234-5678"
    )
    aluno1.id = pessoaDao.salvar(aluno1)
    pessoas.append(aluno1)
    print(f"   ✅ Pessoa criada: {aluno1.nome} - {aluno1.categoria.nome}")
    
    aluno2 = Pessoa(
        id=None,
        nome="Ana Oliveira",
        email="ana.oliveira@aluno.com",
        categoria=categorias['aluno'],
        data_nascimento="2006-05-20",
        telefone="(11) 91234-8765"
    )
    aluno2.id = pessoaDao.salvar(aluno2)
    pessoas.append(aluno2)
    print(f"   ✅ Pessoa criada: {aluno2.nome} - {aluno2.categoria.nome}")
    
    # Administrador
    admin = Pessoa(
        id=None,
        nome="Carlos Admin",
        email="admin@escola.com",
        categoria=categorias['admin'],
        data_nascimento="1980-12-01",
        telefone="(11) 99999-9999"
    )
    admin.id = pessoaDao.salvar(admin)
    pessoas.append(admin)
    print(f"   ✅ Pessoa criada: {admin.nome} - {admin.categoria.nome}")
    
    # 4. CRIAR TURMAS
    print("\n4️⃣  Criando turmas...")
    turmas = []
    
    turma1 = Turma(
        id=None,
        horario="08:00-10:00",
        nivel=niveis['basico'],
        professor=prof1.nome
    )
    turma1.id = turmaDao.salvar(turma1)
    turmas.append(turma1)
    print(f"   ✅ Turma criada: {turma1.nivel.nome} - {turma1.horario} - Prof. {turma1.professor}")
    
    turma2 = Turma(
        id=None,
        horario="10:30-12:30",
        nivel=niveis['intermediario'],
        professor=prof1.nome
    )
    turma2.id = turmaDao.salvar(turma2)
    turmas.append(turma2)
    print(f"   ✅ Turma criada: {turma2.nivel.nome} - {turma2.horario} - Prof. {turma2.professor}")
    
    turma3 = Turma(
        id=None,
        horario="14:00-16:00",
        nivel=niveis['avancado'],
        professor=prof2.nome
    )
    turma3.id = turmaDao.salvar(turma3)
    turmas.append(turma3)
    print(f"   ✅ Turma criada: {turma3.nivel.nome} - {turma3.horario} - Prof. {turma3.professor}")
    
    # 5. CRIAR LOGINS
    print("\n5️⃣  Criando logins...")
    logins = []
    
    # Login para admin
    login_admin = Login(
        id=None,
        email="admin@escola.com",
        senha="admin123",
        usuario_id=admin.id
    )
    login_admin.id = loginDao.salvar(login_admin)
    logins.append(login_admin)
    print(f"   ✅ Login criado: {login_admin.email} (senha: admin123)")
    
    # Login para professor 1
    login_prof1 = Login(
        id=None,
        email="joao.silva@escola.com",
        senha="prof123",
        usuario_id=prof1.id
    )
    login_prof1.id = loginDao.salvar(login_prof1)
    logins.append(login_prof1)
    print(f"   ✅ Login criado: {login_prof1.email} (senha: prof123)")
    
    # Login para aluno 1
    login_aluno1 = Login(
        id=None,
        email="pedro.costa@aluno.com",
        senha="aluno123",
        usuario_id=aluno1.id
    )
    login_aluno1.id = loginDao.salvar(login_aluno1)
    logins.append(login_aluno1)
    print(f"   ✅ Login criado: {login_aluno1.email} (senha: aluno123)")
    
    print("\n" + "="*60)
    print("  ✅ DADOS DE EXEMPLO CRIADOS COM SUCESSO!")
    print("="*60)
    
    return {
        'categorias': categorias,
        'niveis': niveis,
        'pessoas': pessoas,
        'turmas': turmas,
        'logins': logins
    }


def exibir_resumo(dados):
    """Exibe um resumo dos dados criados"""
    print("\n" + "="*60)
    print("  📊 RESUMO DOS DADOS CRIADOS")
    print("="*60)
    
    print(f"\n📁 Categorias: {len(dados['categorias'])}")
    for nome, cat in dados['categorias'].items():
        print(f"   • {cat.nome} (ID: {cat.id})")
    
    print(f"\n📊 Níveis: {len(dados['niveis'])}")
    for nome, nivel in dados['niveis'].items():
        print(f"   • {nivel.nome} (ID: {nivel.id})")
    
    print(f"\n👥 Pessoas: {len(dados['pessoas'])}")
    for pessoa in dados['pessoas']:
        print(f"   • {pessoa.nome} - {pessoa.categoria.nome} ({pessoa.email})")
    
    print(f"\n🎓 Turmas: {len(dados['turmas'])}")
    for turma in dados['turmas']:
        print(f"   • {turma.nivel.nome} - {turma.horario} - Prof. {turma.professor}")
    
    print(f"\n🔐 Logins: {len(dados['logins'])}")
    for login in dados['logins']:
        print(f"   • {login.email}")
    
    print("\n" + "="*60)


def testar_autenticacao(db):
    """Testa o sistema de autenticação"""
    print("\n" + "="*60)
    print("  🔒 TESTANDO SISTEMA DE AUTENTICAÇÃO")
    print("="*60)
    
    loginDao = LoginDAO(db)
    
    # Teste 1: Login correto
    print("\n1️⃣  Teste: Login com credenciais corretas")
    login = loginDao.buscarPorEmail("admin@escola.com")
    if login and login.verificar_senha("admin123"):
        print("   ✅ Autenticação bem-sucedida!")
    else:
        print("   ❌ Autenticação falhou!")
    
    # Teste 2: Login com senha errada
    print("\n2️⃣  Teste: Login com senha incorreta")
    if login and login.verificar_senha("senha_errada"):
        print("   ❌ ERRO: Autenticou com senha errada!")
    else:
        print("   ✅ Senha incorreta rejeitada corretamente!")
    
    # Teste 3: Email inexistente
    print("\n3️⃣  Teste: Login com email inexistente")
    login_inexistente = loginDao.buscarPorEmail("naoexiste@escola.com")
    if login_inexistente:
        print("   ❌ ERRO: Encontrou login inexistente!")
    else:
        print("   ✅ Email inexistente rejeitado corretamente!")
    
    print("\n" + "="*60)


def main():
    """Função principal"""
    db = DatabaseConnection('exemplo_bd.db')
    
    try:
        # Conectar ao banco
        db.conectar()
        
        # Criar tabelas
        db.criarTabelas()
        
        # Limpar dados antigos
        limpar_banco(db)
        
        # Criar dados de exemplo
        dados = criar_dados_exemplo(db)
        
        # Exibir resumo
        exibir_resumo(dados)
        
        # Testar autenticação
        testar_autenticacao(db)
        
        print("\n✅ Demonstração concluída!")
        print("Você pode agora executar o sistema principal: python main.py")
        
    except Exception as e:
        print(f"\n❌ Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.fechar()
        print("\n✔ Conexão com banco de dados encerrada.")


if __name__ == "__main__":
    main()