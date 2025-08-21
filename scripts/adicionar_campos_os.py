#!/usr/bin/env python3
"""
Script para adicionar campos faltantes na tabela ordens_servico
"""

import sys
import os

# Adicionar o diretório app ao path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app'))

from app import app
from extensoes import db

def adicionar_campos_os():
    """Adiciona campos faltantes na tabela ordens_servico"""
    
    with app.app_context():
        try:
            # Lista de campos para adicionar
            campos_adicionar = [
                "ALTER TABLE ordens_servico ADD COLUMN problema_descrito TEXT",
                "ALTER TABLE ordens_servico ADD COLUMN outras_informacoes TEXT",
            ]
            
            print("🔧 Adicionando campos faltantes na tabela ordens_servico...")
            
            for campo_sql in campos_adicionar:
                try:
                    db.engine.execute(campo_sql)
                    print(f"✅ Executado: {campo_sql}")
                except Exception as e:
                    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                        print(f"⚠️  Campo já existe: {campo_sql}")
                    else:
                        print(f"❌ Erro ao executar: {campo_sql} - {str(e)}")
            
            # Commit das alterações
            db.session.commit()
            print("\n✅ Campos adicionados com sucesso!")
            
            # Verificar campos existentes
            print("\n📋 Verificando estrutura da tabela...")
            result = db.engine.execute("PRAGMA table_info(ordens_servico)")
            campos = result.fetchall()
            
            print("Campos existentes na tabela ordens_servico:")
            for campo in campos:
                print(f"  - {campo[1]} ({campo[2]})")
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    adicionar_campos_os()
