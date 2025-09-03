import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.extensoes import db
from app.cliente.cliente_model import Cliente
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Conectar diretamente ao banco
engine = create_engine('postgresql+psycopg2://jsp_user:jsp123456@localhost:5432/jsp_erp')
Session = sessionmaker(bind=engine)
session = Session()

try:
    print("=== ATIVANDO CLIENTE EXISTENTE ===")
    
    # Buscar cliente
    cliente = session.query(Cliente).first()
    if cliente:
        print(f"Cliente encontrado: {cliente.nome}")
        print(f"Status atual - Ativo: {cliente.ativo}")
        
        # Ativar cliente
        cliente.ativo = True
        session.commit()
        
        print(f"✓ Cliente ativado com sucesso!")
        print(f"Novo status - Ativo: {cliente.ativo}")
        
        # Verificar se a busca funciona agora
        print("\n=== TESTANDO BUSCA ===")
        termo = 'sergi'
        resultado = session.query(Cliente).filter(
            Cliente.nome.ilike(f'%{termo}%'),
            Cliente.ativo == True
        ).all()
        
        print(f"Clientes encontrados com '{termo}': {len(resultado)}")
        for c in resultado:
            print(f"  - {c.nome} ({c.cpf_cnpj})")
            
    else:
        print("Nenhum cliente encontrado no banco")
        
except Exception as e:
    session.rollback()
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    session.close()
