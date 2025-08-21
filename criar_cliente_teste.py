#!/usr/bin/env python3
"""Script para criar cliente e testar OS"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensoes import db
from cliente.cliente_model import Cliente

app = create_app()

with app.app_context():
    # Criar cliente teste se não existir
    cliente_teste = Cliente.query.filter_by(cpf_cnpj='12345678901').first()
    
    if not cliente_teste:
        cliente_teste = Cliente(
            nome='Cliente Teste OS',
            cpf_cnpj='12345678901',
            telefone='(11) 99999-9999',
            email='teste@teste.com',
            endereco='Rua Teste, 123',
            ativo=True
        )
        db.session.add(cliente_teste)
        db.session.commit()
        print(f'Cliente criado: ID={cliente_teste.id}, Nome={cliente_teste.nome}')
    else:
        print(f'Cliente já existe: ID={cliente_teste.id}, Nome={cliente_teste.nome}')
    
    # Verificar se as tabelas existem
    print(f'\nTabelas existentes:')
    print(f'- cliente: {db.engine.has_table("cliente")}')
    print(f'- ordem_servico: {db.engine.has_table("ordem_servico")}')
    
    # Verificar todos os clientes
    todos_clientes = Cliente.query.filter_by(ativo=True).all()
    print(f'\nClientes ativos: {len(todos_clientes)}')
    for c in todos_clientes:
        print(f'  ID: {c.id}, Nome: {c.nome}')
