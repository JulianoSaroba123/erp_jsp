#!/usr/bin/env python3
"""Script para verificar e criar cliente teste"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import app
from extensoes import db
from cliente.cliente_model import Cliente

with app.app_context():
    # Verificar clientes existentes
    clientes = Cliente.query.all()
    print(f"Clientes no banco: {len(clientes)}")
    
    if len(clientes) == 0:
        print("Criando cliente teste...")
        cliente = Cliente(
            nome='Cliente Teste OS',
            cpf_cnpj='12345678901',
            telefone='(11) 99999-9999',
            email='teste@teste.com',
            endereco='Rua Teste, 123',
            ativo=True
        )
        db.session.add(cliente)
        db.session.commit()
        print(f"Cliente criado: ID {cliente.id}")
    else:
        for c in clientes:
            print(f"Cliente: ID {c.id}, Nome: {c.nome}")
