#!/usr/bin/env python3
# scripts/atualizar_banco_arquivos.py

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask
from extensoes import db

def create_app():
    """Cria e configura o app Flask"""
    app = Flask(__name__)
    
    # Configurações do banco (usando valores padrão)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-key'
    
    # Inicializa o banco
    db.init_app(app)
    
    return app

def atualizar_banco():
    """Atualiza o banco de dados com a tabela de arquivos"""
    print("=== ATUALIZANDO BANCO DE DADOS - ARQUIVOS OS ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Importar modelo aqui para evitar problemas de importação circular
            from app.ordem_servico.arquivo_model import OSArquivo
            
            # Criar tabela de arquivos
            print("Criando tabela os_arquivos...")
            db.create_all()
            
            print("✅ Tabela os_arquivos criada com sucesso!")
            
            # Verificar se a tabela foi criada
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tabelas = inspector.get_table_names()
            
            if 'os_arquivos' in tabelas:
                print("✅ Tabela os_arquivos confirmada no banco")
                
                # Mostrar colunas da tabela
                colunas = inspector.get_columns('os_arquivos')
                print("Colunas da tabela os_arquivos:")
                for coluna in colunas:
                    print(f"  - {coluna['name']}: {coluna['type']}")
            else:
                print("❌ Tabela os_arquivos não encontrada")
            
            print("\n=== ATUALIZAÇÃO CONCLUÍDA ===")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar banco: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    atualizar_banco()
