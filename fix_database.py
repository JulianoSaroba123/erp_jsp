#!/usr/bin/env python3
"""
Script para remover coluna data_atualizacao da tabela ordens_servico
Executa diretamente no banco para corrigir o erro de SELECT
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app.app import app
from extensoes import db

def fix_database():
    """Remove colunas data_atualizacao que podem estar causando problemas"""
    with app.app_context():
        try:
            # Para PostgreSQL (Render)
            if 'postgresql' in str(db.engine.url):
                print("Executando correção no PostgreSQL...")
                
                # Lista de tabelas que podem ter a coluna problemática
                tables = ['ordens_servico', 'clientes', 'fornecedores', 'servicos']
                
                for table in tables:
                    try:
                        # Verifica se a coluna existe
                        result = db.session.execute(db.text(f"""
                            SELECT column_name 
                            FROM information_schema.columns 
                            WHERE table_name='{table}' AND column_name='data_atualizacao'
                        """))
                        
                        if result.fetchone():
                            print(f"Removendo coluna data_atualizacao da tabela {table}...")
                            db.session.execute(db.text(f"ALTER TABLE {table} DROP COLUMN IF EXISTS data_atualizacao"))
                            db.session.commit()
                            print(f"✅ Coluna removida da tabela {table}")
                        else:
                            print(f"⚠️ Coluna data_atualizacao não existe na tabela {table}")
                            
                    except Exception as e:
                        print(f"❌ Erro ao processar tabela {table}: {e}")
                        db.session.rollback()
                        
            # Para SQLite (local)
            else:
                print("SQLite detectado - não precisa de correção")
                
            print("🚀 Correção de banco concluída!")
            
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            db.session.rollback()

if __name__ == '__main__':
    fix_database()
