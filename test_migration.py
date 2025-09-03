#!/usr/bin/env python3
import sys
sys.path.append('.')

from run import app
from app.extensoes import db
from sqlalchemy import inspect

with app.app_context():
    # Verificar estrutura da tabela servicos
    inspector = inspect(db.engine)
    columns = inspector.get_columns('servicos')
    
    print('=== Colunas da tabela servicos ===')
    for col in columns:
        name = col.get('name', 'N/A')
        col_type = str(col.get('type', 'N/A'))
        nullable = col.get('nullable', True)
        print(f'  {name}: {col_type} - nullable: {nullable}')
    
    # Verificar constraints CHECK
    try:
        constraints = inspector.get_check_constraints('servicos')
        print('\n=== Constraints CHECK ===')
        for constraint in constraints:
            name = constraint.get('name', 'N/A')
            sqltext = constraint.get('sqltext', 'N/A')
            print(f'  {name}: {sqltext}')
    except Exception as e:
        print(f'\nErro ao buscar constraints: {e}')
    
    # Testar uma consulta simples
    print('\n=== Teste de dados ===')
    result = db.session.execute(db.text("SELECT COUNT(*) FROM servicos"))
    count = result.scalar()
    print(f'Total de serviços na tabela: {count}')
    
    # Verificar se as colunas existem
    required_cols = ['markup_percentual', 'preco_venda', 'valor']
    existing_cols = [col['name'] for col in columns]
    
    print('\n=== Verificação de colunas requeridas ===')
    for col in required_cols:
        status = '✓' if col in existing_cols else '✗'
        print(f'  {status} {col}')

print('✅ Teste de migration concluído!')
