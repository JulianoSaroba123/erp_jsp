#!/usr/bin/env python3
"""
Script para adicionar campos da integração financeira manualmente
"""

import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app.app import app
from app.extensoes import db
from sqlalchemy import text

def adicionar_campos_os():
    """Adiciona os campos necessários para integração financeira na tabela ordens_servico"""
    with app.app_context():
        try:
            print("=== ADICIONANDO CAMPOS PARA INTEGRAÇÃO FINANCEIRA ===")
            
            # Verificar se os campos já existem
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='ordens_servico' 
                AND column_name IN ('condicao_pagamento', 'qtd_parcelas', 'valor_entrada', 'status_pagamento', 'schedule_json')
            """))
            existing_columns = [row[0] for row in result]
            print(f"Campos existentes: {existing_columns}")
            
            # Campos para adicionar
            campos_para_adicionar = {
                'condicao_pagamento': 'VARCHAR(50)',
                'qtd_parcelas': 'INTEGER',
                'valor_entrada': 'NUMERIC(10,2)',
                'status_pagamento': 'VARCHAR(20)',
                'schedule_json': 'TEXT'
            }
            
            # Adicionar cada campo se não existir
            for campo, tipo in campos_para_adicionar.items():
                if campo not in existing_columns:
                    try:
                        db.session.execute(text(f'ALTER TABLE ordens_servico ADD COLUMN {campo} {tipo}'))
                        print(f"✅ Campo '{campo}' adicionado com sucesso")
                    except Exception as e:
                        print(f"❌ Erro ao adicionar campo '{campo}': {e}")
                else:
                    print(f"⚠️  Campo '{campo}' já existe")
            
            # Commit das alterações
            db.session.commit()
            print("\n🎯 Migração manual concluída com sucesso!")
            
            # Verificar se todos os campos foram adicionados
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='ordens_servico' 
                AND column_name IN ('condicao_pagamento', 'qtd_parcelas', 'valor_entrada', 'status_pagamento', 'schedule_json')
            """))
            final_columns = [row[0] for row in result]
            print(f"Campos após migração: {final_columns}")
            
            if len(final_columns) == 5:
                print("✅ Todos os campos necessários estão presentes!")
            else:
                print(f"⚠️  Faltam campos: {set(campos_para_adicionar.keys()) - set(final_columns)}")
                
        except Exception as e:
            print(f"❌ Erro durante migração: {str(e)}")
            db.session.rollback()
            return False
        
        return True

if __name__ == "__main__":
    sucesso = adicionar_campos_os()
    if not sucesso:
        sys.exit(1)
