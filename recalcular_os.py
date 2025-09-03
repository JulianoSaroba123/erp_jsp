#!/usr/bin/env python3
"""
Script para recalcular todas as ordens de serviço existentes
após correção na lógica de cálculo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.app import create_app
from app.extensoes import db
from app.ordem_servico.os_model import OrdemServico

def recalcular_todas_os():
    """Recalcula todas as ordens de serviço"""
    app = create_app()
    
    with app.app_context():
        try:
            # Buscar todas as ordens de serviço
            ordens = OrdemServico.query.all()
            total_ordens = len(ordens)
            
            print(f"Iniciando recálculo de {total_ordens} ordens de serviço...")
            
            for i, ordem in enumerate(ordens, 1):
                print(f"[{i}/{total_ordens}] Recalculando OS {ordem.codigo}...")
                
                # Valores antes do recálculo
                valor_antes = ordem.valor_total
                
                # Recalcular valores
                ordem.recalcular_valores()
                
                # Valores após o recálculo
                valor_depois = ordem.valor_total
                
                print(f"  - Valor antes: R$ {valor_antes:.2f}")
                print(f"  - Valor depois: R$ {valor_depois:.2f}")
                
                if valor_antes != valor_depois:
                    print(f"  - ✅ Valor atualizado!")
                else:
                    print(f"  - ⚪ Sem alteração")
            
            # Salvar todas as alterações
            db.session.commit()
            print(f"\n✅ Recálculo concluído! {total_ordens} ordens de serviço processadas.")
            
        except Exception as e:
            print(f"❌ Erro durante o recálculo: {e}")
            db.session.rollback()

if __name__ == "__main__":
    recalcular_todas_os()
