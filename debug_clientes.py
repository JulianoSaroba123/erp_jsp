import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.extensoes import db
from app.cliente.cliente_model import Cliente
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Conectar diretamente ao banco
engine = create_engine('postgresql+psycopg2://jsp_user:jsp123456@localhost:5432/jsp_erp')
Session = sessionmaker(bind=engine)
session = Session()

try:
    print("=== VERIFICANDO CLIENTES NO BANCO ===")
    
    # Buscar todos os clientes
    clientes = session.query(Cliente).all()
    print(f"Total de clientes: {len(clientes)}")
    
    for i, cliente in enumerate(clientes, 1):
        print(f"\nCliente {i}:")
        print(f"  ID: {cliente.id}")
        print(f"  Código: {cliente.codigo}")
        print(f"  Nome: '{cliente.nome}'")
        print(f"  CPF/CNPJ: '{cliente.cpf_cnpj}'")
        print(f"  Ativo: {cliente.ativo} (tipo: {type(cliente.ativo)})")
        print(f"  Telefone: '{cliente.telefone}'")
        print(f"  Email: '{cliente.email}'")
        print(f"  Endereço: '{cliente.endereco}'")
    
    print("\n=== TESTANDO FILTROS ===")
    
    # Teste 1: Apenas clientes ativos
    ativos = session.query(Cliente).filter(Cliente.ativo == True).all()
    print(f"Clientes ativos: {len(ativos)}")
    
    # Teste 2: Busca por nome (case insensitive)
    termo = 'sergi'
    por_nome = session.query(Cliente).filter(Cliente.nome.ilike(f'%{termo}%')).all()
    print(f"Clientes com nome contendo '{termo}': {len(por_nome)}")
    
    # Teste 3: Busca por CPF
    por_cpf = session.query(Cliente).filter(Cliente.cpf_cnpj.ilike(f'%077%')).all()
    print(f"Clientes com CPF contendo '077': {len(por_cpf)}")
    
    # Teste 4: Busca combinada (nome OU cpf) E ativo
    combinada = session.query(Cliente).filter(
        (Cliente.nome.ilike(f'%{termo}%') | Cliente.cpf_cnpj.ilike(f'%{termo}%')) &
        (Cliente.ativo == True)
    ).all()
    print(f"Busca combinada ('{termo}' e ativo): {len(combinada)}")
    
    # Teste 5: SQL Raw para verificar dados
    print("\n=== DADOS BRUTOS (SQL) ===")
    result = session.execute(text("SELECT id, codigo, nome, cpf_cnpj, ativo FROM cliente LIMIT 5"))
    for row in result:
        print(f"ID: {row[0]}, Código: {row[1]}, Nome: '{row[2]}', CPF: '{row[3]}', Ativo: {row[4]} ({type(row[4])})")
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    session.close()
