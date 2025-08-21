#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para atualizar estrutura do banco de dados
Adiciona novos campos aos models Cliente, Fornecedor e Produto
"""

import sys
import os

# Adicionar o diretório pai ao path para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Mudar para o diretório do projeto
os.chdir(parent_dir)

# Importar módulos
from extensoes import db
from app import app

def atualizar_banco():
    """Atualiza estrutura do banco de dados"""
    with app.app_context():
        try:
            print("🔄 Iniciando atualização do banco de dados...")
            
            # Criar todas as tabelas com as novas estruturas
            db.create_all()
            
            print("✅ Estrutura do banco atualizada com sucesso!")
            print("\n📋 Novos campos adicionados:")
            
            print("\n🔹 Cliente:")
            print("  - uf (substituiu estado)")
            print("  - pais")
            print("  - inscricao_estadual")
            print("  - inscricao_municipal")
            print("  - observacoes")
            print("  - ativo")
            print("  - data_cadastro")
            print("  - data_atualizacao")
            
            print("\n🔹 Fornecedor:")
            print("  - cpf_cnpj (substituiu cnpj)")
            print("  - uf (substituiu estado)")
            print("  - pais")
            print("  - inscricao_estadual")
            print("  - inscricao_municipal")
            print("  - contato_comercial")
            print("  - telefone_comercial")
            print("  - email_comercial")
            print("  - observacoes")
            print("  - ativo")
            print("  - data_cadastro")
            print("  - data_atualizacao")
            
            print("\n🔹 Produto:")
            print("  - Estrutura já estava completa")
            
            print("\n🎯 Banco de dados pronto para uso com os novos formulários!")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar banco: {e}")
            return False
        
        return True

if __name__ == "__main__":
    success = atualizar_banco()
    if success:
        print("\n✨ Atualização concluída com sucesso!")
    else:
        print("\n💥 Falha na atualização!")
        sys.exit(1)
