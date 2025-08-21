#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para migrar banco de dados do ERP JSP
Atualiza campos antigos para nova estrutura
"""

import sqlite3
import os

def migrar_banco():
    """Migra banco de dados para nova estrutura"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'database.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Iniciando migração do banco de dados...")
        
        # Verificar se existe a tabela clientes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clientes';")
        if cursor.fetchone():
            print("📋 Migrando tabela clientes...")
            
            # Verificar se coluna 'uf' já existe
            cursor.execute("PRAGMA table_info(clientes);")
            colunas = [col[1] for col in cursor.fetchall()]
            
            if 'uf' not in colunas:
                # Adicionar novas colunas
                cursor.execute("ALTER TABLE clientes ADD COLUMN uf VARCHAR(2);")
                cursor.execute("ALTER TABLE clientes ADD COLUMN pais VARCHAR(50) DEFAULT 'Brasil';")
                cursor.execute("ALTER TABLE clientes ADD COLUMN inscricao_estadual VARCHAR(20);")
                cursor.execute("ALTER TABLE clientes ADD COLUMN inscricao_municipal VARCHAR(20);")
                cursor.execute("ALTER TABLE clientes ADD COLUMN observacoes TEXT;")
                cursor.execute("ALTER TABLE clientes ADD COLUMN ativo BOOLEAN DEFAULT 1;")
                cursor.execute("ALTER TABLE clientes ADD COLUMN data_cadastro DATETIME;")
                cursor.execute("ALTER TABLE clientes ADD COLUMN data_atualizacao DATETIME;")
                
                # Migrar dados de estado para uf
                if 'estado' in colunas:
                    cursor.execute("UPDATE clientes SET uf = estado WHERE estado IS NOT NULL;")
                
                print("✅ Clientes migrados com sucesso!")
            else:
                print("ℹ️ Tabela clientes já está atualizada")
        
        # Verificar se existe a tabela fornecedores
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fornecedores';")
        if cursor.fetchone():
            print("📋 Migrando tabela fornecedores...")
            
            cursor.execute("PRAGMA table_info(fornecedores);")
            colunas = [col[1] for col in cursor.fetchall()]
            
            if 'uf' not in colunas:
                # Adicionar novas colunas
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN uf VARCHAR(2);")
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN pais VARCHAR(50) DEFAULT 'Brasil';")
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN inscricao_estadual VARCHAR(20);")
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN inscricao_municipal VARCHAR(20);")
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN contato_comercial VARCHAR(100);")
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN telefone_comercial VARCHAR(20);")
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN email_comercial VARCHAR(120);")
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN observacoes TEXT;")
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN ativo BOOLEAN DEFAULT 1;")
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN data_cadastro DATETIME;")
                cursor.execute("ALTER TABLE fornecedores ADD COLUMN data_atualizacao DATETIME;")
                
                # Migrar dados de estado para uf
                if 'estado' in colunas:
                    cursor.execute("UPDATE fornecedores SET uf = estado WHERE estado IS NOT NULL;")
                
                # Migrar cnpj para cpf_cnpj se necessário
                if 'cnpj' in colunas and 'cpf_cnpj' not in colunas:
                    cursor.execute("ALTER TABLE fornecedores ADD COLUMN cpf_cnpj VARCHAR(18);")
                    cursor.execute("UPDATE fornecedores SET cpf_cnpj = cnpj WHERE cnpj IS NOT NULL;")
                
                print("✅ Fornecedores migrados com sucesso!")
            else:
                print("ℹ️ Tabela fornecedores já está atualizada")
        
        conn.commit()
        conn.close()
        
        print("\n🎯 Migração concluída com sucesso!")
        print("📝 Novas colunas adicionadas:")
        print("   - uf (substituindo estado)")
        print("   - pais, inscricao_estadual, inscricao_municipal")
        print("   - observacoes, ativo, data_cadastro, data_atualizacao")
        print("   - Campos comerciais para fornecedores")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        return False

if __name__ == "__main__":
    success = migrar_banco()
    if success:
        print("\n✨ Banco de dados migrado com sucesso!")
    else:
        print("\n💥 Falha na migração!")
