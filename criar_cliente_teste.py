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
    # Verificar se já existe cliente
    total = session.query(Cliente).count()
    print(f'Total de clientes existentes: {total}')
    
    if total == 0:
        print('Criando cliente de teste...')
        cliente = Cliente()
        cliente.codigo = 'CLI0001'
        cliente.nome = 'Sergio Silva'
        cliente.cpf_cnpj = '12345678901'
        cliente.telefone = '(11) 99999-9999'
        cliente.email = 'sergio@teste.com'
        cliente.endereco = 'Rua Teste, 123'
        cliente.ativo = True
        
        session.add(cliente)
        session.commit()
        print('Cliente criado com sucesso!')
    else:
        print('Clientes já existem:')
        clientes = session.query(Cliente).all()
        for c in clientes:
            print(f'- {c.nome} ({c.cpf_cnpj})')
    
    # Verificar novamente
    total_final = session.query(Cliente).count()
    print(f'Total final de clientes: {total_final}')
    
except Exception as e:
    session.rollback()
    print(f'Erro: {e}')
    import traceback
    traceback.print_exc()
finally:
    session.close()
