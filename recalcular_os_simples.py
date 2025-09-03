#!/usr/bin/env python3
"""Script simples para recalcular uma OS específica"""

# Importar os módulos necessários
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar o Flask app
from app.app import create_app
from app.extensoes import db
from app.ordem_servico.os_model import OrdemServico

# Criar app e contexto
app = create_app()

with app.app_context():
    # Buscar a OS específica (código OS0002)
    ordem = OrdemServico.query.filter_by(codigo='OS0002').first()
    
    if ordem:
        print(f"Encontrada OS {ordem.codigo}")
        print(f"Valor atual: R$ {ordem.valor_total:.2f}")
        
        # Recalcular
        ordem.recalcular_valores()
        
        print(f"Novo valor: R$ {ordem.valor_total:.2f}")
        
        # Salvar
        db.session.commit()
        print("OS atualizada com sucesso!")
    else:
        print("OS OS0002 não encontrada")
