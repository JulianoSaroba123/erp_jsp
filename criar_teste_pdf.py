#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Adicionar o caminho do projeto ao sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.extensoes import db
from app.cliente.cliente_model import Cliente
from app.ordem_servico.os_model import OrdemServico
import json
from datetime import datetime, date

def criar_dados_teste():
    """Criar dados de teste para demonstrar o PDF"""
    try:
        # Verificar se já há um cliente
        cliente = Cliente.query.first()
        if not cliente:
            # Criar cliente teste
            cliente = Cliente(
                nome='Cliente Teste PDF',
                documento='123.456.789-00',
                telefone='(15) 99999-9999',
                endereco='Rua Teste, 123',
                ativo=True
            )
            db.session.add(cliente)
            db.session.commit()
            print(f'Cliente criado: ID {cliente.id}')
        else:
            print(f'Cliente existente: ID {cliente.id}, Nome: {cliente.nome}')

        # Verificar se já há uma OS
        os = OrdemServico.query.first()
        if not os:
            # Criar OS teste
            servicos_data = [
                {'nome': 'Instalação elétrica', 'quantidade': 2, 'valor_unitario': 150.00, 'valor_total': 300.00}
            ]
            produtos_data = [
                {'nome': 'Cabo 2.5mm', 'quantidade': 10, 'valor_unitario': 8.50, 'valor_total': 85.00}
            ]
            
            os = OrdemServico(
                codigo='OS0001',
                cliente_id=cliente.id,
                status='Concluída',
                data_emissao=date.today(),
                equipamento_nome='Quadro Elétrico',
                problema_descrito='Instalação de novo quadro elétrico',
                descricao_servico_realizado='Quadro instalado com sucesso',
                tecnico_responsavel='João Silva',
                valor_servicos=300.00,
                valor_produtos=85.00,
                valor_total=385.00,
                servicos_dados=json.dumps(servicos_data),
                produtos_dados=json.dumps(produtos_data),
                ativo=True
            )
            db.session.add(os)
            db.session.commit()
            print(f'OS criada: ID {os.id}, Código: {os.codigo}')
        else:
            print(f'OS existente: ID {os.id}, Código: {os.codigo}')

        return os

    except Exception as e:
        print(f'Erro: {e}')
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    # Simular o contexto da aplicação Flask
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    # Importar configurações
    from app.config import SQLALCHEMY_DATABASE_URI
    
    from flask import Flask
    from app.extensoes import db
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        os = criar_dados_teste()
        if os:
            print(f'Dados criados com sucesso! Teste o PDF em: http://127.0.0.1:5000/os/{os.id}/pdf')
