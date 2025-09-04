#!/usr/bin/env python3
"""
Script para verificar o estado dos clientes no banco de dados.
Este script apenas consulta os dados sem modificá-los.
"""

from app.app import app
from app.cliente.cliente_model import Cliente
from app.extensoes import db
from sqlalchemy import text, inspect
from sqlalchemy.exc import ProgrammingError
import sys

def verificar_estado_clientes():
    """Verificar o estado atual dos clientes no banco de dados"""
    with app.app_context():
        # Obter estatísticas gerais
        total = Cliente.query.count()
        ativos = Cliente.query.filter_by(ativo=True).count()
        inativos = Cliente.query.filter_by(ativo=False).count()
        sem_pais = Cliente.query.filter(Cliente.pais.is_(None) | (Cliente.pais == '')).count()

        print("=== ESTADO ATUAL DOS CLIENTES ===")
        print(f"Total de clientes: {total}")
        print(f"Ativos: {ativos}")
        print(f"Inativos: {inativos}")
        print(f"Sem país definido: {sem_pais}")
        
        # Listar clientes inativos
        if inativos > 0:
            print("\n=== CLIENTES INATIVOS ===")
            for cliente in Cliente.query.filter_by(ativo=False).all():
                print(f"ID: {cliente.id} | Nome: {cliente.nome} | CPF/CNPJ: {cliente.cpf_cnpj}")
        
        # Determinar se é PostgreSQL ou SQLite
        engine_name = db.engine.name
        print(f"\nTipo de banco de dados: {engine_name}")
        
        # Verificar estrutura da tabela
        print("\n=== ESTRUTURA DA TABELA ===")
        
        if engine_name == 'postgresql':
            try:
                constraint_info = db.session.execute(text("""
                    SELECT conname, pg_get_constraintdef(oid)
                    FROM pg_constraint
                    WHERE conrelid = 'clientes'::regclass
                    ORDER BY contype, conname;
                """)).fetchall()
        
                for name, definition in constraint_info:
                    print(f"Constraint: {name} | Definição: {definition}")
                
                # Verificar definição da coluna 'ativo'
                column_info = db.session.execute(text("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_name = 'clientes' AND column_name = 'ativo';
                """)).fetchone()
                
                if column_info:
                    col_name, data_type, is_nullable, default = column_info
                    print(f"Coluna 'ativo': Tipo={data_type}, Nullable={is_nullable}, Default={default}")
            except ProgrammingError as e:
                print(f"Erro ao consultar metadados PostgreSQL: {e}")
        else:
            # SQLite
            inspector = inspect(db.engine)
            columns = inspector.get_columns('clientes')
            for column in columns:
                if column['name'] == 'ativo':
                    print(f"Coluna 'ativo': Tipo={column['type']}, Nullable={not column.get('nullable', False)}, Default={column.get('default')}")

if __name__ == "__main__":
    print("Iniciando verificação dos clientes...")
    try:
        verificar_estado_clientes()
    except Exception as e:
        print(f"ERRO: {e}")
        sys.exit(1)
