#!/usr/bin/env python3
"""
Script para corrigir migração no Render ou ambiente local.
Usa o SQLAlchemy para aplicar diretamente as alterações.
"""

from app.app import app
from app.extensoes import db
from app.cliente.cliente_model import Cliente
from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError, OperationalError
import sys

def corrigir_migracao():
    """Corrigir dados inconsistentes que podem ter sido criados por migrações falhas"""
    with app.app_context():
        try:
            engine_name = db.engine.name
            print(f"=== CORREÇÃO DE MIGRAÇÕES [{engine_name.upper()}] ===")
            
            # Primeiro atualizar todos os clientes para ativo=True
            total_atualizados = 0
            for cliente in Cliente.query.filter(Cliente.ativo.is_(False) | Cliente.ativo.is_(None)).all():
                cliente.ativo = True
                total_atualizados += 1
            
            print(f"Clientes atualizados para ativo=True: {total_atualizados}")
            
            # Atualizar país para Brasil onde estiver vazio
            total_pais = 0
            for cliente in Cliente.query.filter(Cliente.pais.is_(None) | (Cliente.pais == '')).all():
                cliente.pais = 'Brasil'
                total_pais += 1
            
            print(f"Clientes atualizados com país='Brasil': {total_pais}")
            
            # PostgreSQL: garantir que a coluna "ativo" é NOT NULL e com default TRUE
            if engine_name == 'postgresql':
                try:
                    print("\nAplicando alterações de esquema no PostgreSQL...")
                    db.session.execute(text("""
                        ALTER TABLE clientes 
                        ALTER COLUMN ativo SET DEFAULT TRUE,
                        ALTER COLUMN ativo SET NOT NULL;
                    """))
                    print("✅ Esquema atualizado com sucesso!")
                except (ProgrammingError, OperationalError) as e:
                    print(f"⚠️ Não foi possível alterar o esquema: {e}")
            
            # Commit as alterações
            db.session.commit()
            print("✅ Alterações aplicadas com sucesso!")
            
            # Verificar estado atual
            total = Cliente.query.count()
            ativos = Cliente.query.filter_by(ativo=True).count()
            inativos = Cliente.query.filter_by(ativo=False).count()
            print(f"\nTotal de clientes: {total}")
            print(f"Ativos: {ativos}")
            print(f"Inativos: {inativos}")
            
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"❌ Erro ao aplicar correções: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    print("Iniciando correção de migração...")
    try:
        corrigir_migracao()
    except Exception as e:
        print(f"ERRO CRÍTICO: {e}")
        sys.exit(1)
