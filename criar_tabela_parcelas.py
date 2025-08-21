import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import app
from extensoes import db
from condicoes_pagamento.condicoes_pag_model import OSParcela

with app.app_context():
    print('Criando tabela os_parcelas...')
    try:
        db.create_all()
        print('Tabela os_parcelas criada com sucesso!')
    except Exception as e:
        print(f'Erro: {e}')
