#!/usr/bin/env python3
"""
Ponto de entrada principal do ERP JSP - Elétrica Industrial
Execute este arquivo para iniciar a aplicação Flask
"""

import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para permitir imports do pacote app
sys.path.insert(0, os.path.dirname(__file__))

from app.app import app
from flask_migrate import upgrade
from extensoes import db

def clean_alembic_temp_tables():
    """Remove tabelas temporárias do Alembic que podem causar problemas."""
    try:
        with app.app_context():
            # Lista de possíveis tabelas temporárias do Alembic
            temp_tables = [
                '_alembic_tmp_clientes',
                '_alembic_tmp_fornecedores', 
                '_alembic_tmp_produtos',
                '_alembic_tmp_servicos',
                '_alembic_tmp_ordem_servicos'
            ]
            
            for table in temp_tables:
                try:
                    with db.engine.connect() as conn:
                        conn.execute(db.text(f"DROP TABLE IF EXISTS {table}"))
                        conn.commit()
                    print(f"Dropped temp table: {table}")
                except Exception as e:
                    print(f"Could not drop {table}: {e}")
    except Exception as e:
        print(f"Error cleaning temp tables: {e}")

def deploy():
    """Run deployment tasks."""
    with app.app_context():
        # Primeiro, limpar tabelas temporárias problemáticas
        clean_alembic_temp_tables()
        # Depois executar migrações
        upgrade()

if __name__ == '__main__':
    # Em produção (Render), limpar tabelas temporárias problemáticas
    if os.environ.get('DATABASE_URL'):
        try:
            clean_alembic_temp_tables()
            print("Alembic temp tables cleaned successfully")
        except Exception as e:
            print(f"Migration error (ignoring): {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
