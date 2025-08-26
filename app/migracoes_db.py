# Migração automática para adicionar campos de endereço
from flask import current_app
from app.extensoes import db
import os

def executar_migracoes():
    """Executa migrações necessárias no banco de dados"""
    try:
        with current_app.app_context():
            # Verifica se as colunas de endereço existem
            from sqlalchemy import text, inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('clientes')]
            
            # Lista de colunas que devem existir
            colunas_endereco = ['cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf']
            
            # Adiciona colunas que não existem
            for coluna in colunas_endereco:
                if coluna not in columns:
                    if coluna == 'uf':
                        sql = f"ALTER TABLE clientes ADD COLUMN {coluna} VARCHAR(2)"
                    elif coluna == 'cep':
                        sql = f"ALTER TABLE clientes ADD COLUMN {coluna} VARCHAR(10)"
                    elif coluna == 'logradouro':
                        sql = f"ALTER TABLE clientes ADD COLUMN {coluna} VARCHAR(150)"
                    elif coluna == 'numero':
                        sql = f"ALTER TABLE clientes ADD COLUMN {coluna} VARCHAR(20)"
                    else:  # complemento, bairro, cidade
                        sql = f"ALTER TABLE clientes ADD COLUMN {coluna} VARCHAR(100)"
                    
                    try:
                        db.session.execute(text(sql))
                        db.session.commit()
                        print(f"Coluna {coluna} adicionada com sucesso")
                    except Exception as e:
                        print(f"Erro ao adicionar coluna {coluna}: {e}")
                        db.session.rollback()
                        
    except Exception as e:
        print(f"Erro na migração: {e}")
        return False
    return True
