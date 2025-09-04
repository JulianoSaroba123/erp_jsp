#!/usr/bin/env python3
"""
Script para verificar o estado das migrações e corrigir problemas
"""

import os
import sys
from flask import Flask
from alembic import command
from alembic.config import Config
from sqlalchemy import text, inspect

# Configurar o path para importar o app
sys.path.append(os.path.abspath('.'))

from app.app import app
from app.extensoes import db
from app.cliente.cliente_model import Cliente

def verificar_estado_banco():
    """Verifica o estado atual do banco de dados"""
    print("=== VERIFICAÇÃO DO ESTADO DO BANCO ===")
    
    with app.app_context():
        try:
            # Verificar se a tabela clientes existe
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Tabelas no banco: {tables}")
            
            if 'clientes' in tables:
                # Verificar estrutura da tabela clientes
                columns = inspector.get_columns('clientes')
                print(f"\nColunas da tabela 'clientes':")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")
                
                # Verificar dados
                total = Cliente.query.count()
                ativos = Cliente.query.filter(Cliente.ativo == True).count()
                inativos = Cliente.query.filter(Cliente.ativo == False).count()
                
                print(f"\nDados dos clientes:")
                print(f"  - Total: {total}")
                print(f"  - Ativos: {ativos}")
                print(f"  - Inativos: {inativos}")
                
                # Verificar se há clientes com problemas
                clientes_sem_ativo = db.session.execute(
                    text("SELECT COUNT(*) FROM clientes WHERE ativo IS NULL")
                ).scalar()
                print(f"  - Com campo 'ativo' NULL: {clientes_sem_ativo}")
                
            else:
                print("Tabela 'clientes' não encontrada!")
                
        except Exception as e:
            print(f"Erro ao verificar banco: {e}")

def verificar_migracao():
    """Verifica o estado das migrações"""
    print("\n=== VERIFICAÇÃO DAS MIGRAÇÕES ===")
    
    try:
        # Configurar Alembic
        alembic_cfg = Config('alembic.ini')
        
        with app.app_context():
            # Verificar versão atual
            from alembic.runtime.migration import MigrationContext
            from alembic.script import ScriptDirectory
            
            context = MigrationContext.configure(db.engine.connect())
            current = context.get_current_revision()
            print(f"Revisão atual no banco: {current}")
            
            # Verificar versões disponíveis
            script = ScriptDirectory.from_config(alembic_cfg)
            head = script.get_current_head()
            print(f"Última revisão disponível: {head}")
            
            if current != head:
                print("⚠️  Há migrações pendentes!")
                return False
            else:
                print("✅ Migrações estão atualizadas")
                return True
                
    except Exception as e:
        print(f"Erro ao verificar migrações: {e}")
        return False

def corrigir_clientes():
    """Corrige problemas nos dados de clientes"""
    print("\n=== CORREÇÃO DOS DADOS DE CLIENTES ===")
    
    with app.app_context():
        try:
            # Corrigir clientes com ativo = NULL
            clientes_null = db.session.execute(
                text("UPDATE clientes SET ativo = TRUE WHERE ativo IS NULL")
            )
            db.session.commit()
            print(f"✅ Corrigidos {clientes_null.rowcount} clientes com ativo=NULL")
            
            # Corrigir clientes sem país
            clientes_sem_pais = db.session.execute(
                text("UPDATE clientes SET pais = 'Brasil' WHERE pais IS NULL OR pais = ''")
            )
            db.session.commit()
            print(f"✅ Corrigidos {clientes_sem_pais.rowcount} clientes sem país")
            
            print("✅ Correção dos dados concluída")
            
        except Exception as e:
            print(f"❌ Erro ao corrigir dados: {e}")
            db.session.rollback()

def main():
    print("🔍 DIAGNÓSTICO DO SISTEMA ERP JSP")
    print("=" * 50)
    
    # Verificar estado do banco
    verificar_estado_banco()
    
    # Verificar migrações
    migracoes_ok = verificar_migracao()
    
    if not migracoes_ok:
        print("\n🔧 Aplicando migrações pendentes...")
        try:
            with app.app_context():
                alembic_cfg = Config('alembic.ini')
                command.upgrade(alembic_cfg, 'head')
            print("✅ Migrações aplicadas com sucesso")
        except Exception as e:
            print(f"❌ Erro ao aplicar migrações: {e}")
    
    # Corrigir dados
    corrigir_clientes()
    
    # Verificação final
    print("\n=== VERIFICAÇÃO FINAL ===")
    verificar_estado_banco()

if __name__ == '__main__':
    main()
