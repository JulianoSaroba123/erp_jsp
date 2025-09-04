#!/usr/bin/env python3
"""
Script para aplicar correções no ambiente Render.
Este script cria um arquivo cliente_status.py na pasta app/ com a lógica
necessária para garantir que a coluna 'ativo' sempre seja True por padrão.

Use quando precisar fazer deploy no Render.
"""

import os
from app.app import app
from app.extensoes import db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import sys

def criar_arquivo_cliente_status():
    """
    Cria o arquivo cliente_status.py na pasta app/ com a lógica
    para garantir que todos os clientes sejam ativos.
    """
    conteudo = """# cliente_status.py
# Este arquivo foi criado automaticamente para garantir consistência
# dos dados de cliente entre ambientes

from flask import current_app
from app.extensoes import db
from app.cliente.cliente_model import Cliente
from sqlalchemy import text

def garantir_cliente_ativo():
    \"\"\"
    Função chamada durante inicialização para garantir que:
    1. A coluna ativo seja NOT NULL e DEFAULT TRUE
    2. Todos os clientes existentes tenham ativo=True
    3. Todos os clientes tenham país='Brasil' se o campo estiver vazio
    \"\"\"
    with current_app.app_context():
        try:
            # Verificar se existem clientes inativos
            inativos = Cliente.query.filter_by(ativo=False).count()
            sem_pais = Cliente.query.filter((Cliente.pais == '') | (Cliente.pais.is_(None))).count()
            
            if inativos > 0 or sem_pais > 0:
                current_app.logger.info(f"Encontrados {inativos} clientes inativos e {sem_pais} sem país. Corrigindo...")
                
                # Atualizar clientes inativos
                for cliente in Cliente.query.filter_by(ativo=False).all():
                    cliente.ativo = True
                
                # Atualizar clientes sem país
                for cliente in Cliente.query.filter((Cliente.pais == '') | (Cliente.pais.is_(None))).all():
                    cliente.pais = 'Brasil'
                
                db.session.commit()
                current_app.logger.info("Clientes atualizados com sucesso!")
            
            # Tentar modificar o esquema para PostgreSQL
            engine_name = db.engine.name
            if engine_name == 'postgresql':
                try:
                    db.session.execute(text(\"\"\"
                        ALTER TABLE clientes 
                        ALTER COLUMN ativo SET DEFAULT TRUE,
                        ALTER COLUMN ativo SET NOT NULL;
                    \"\"\"))
                    db.session.commit()
                    current_app.logger.info("Esquema atualizado com sucesso!")
                except Exception as e:
                    current_app.logger.warning(f"Não foi possível atualizar o esquema: {str(e)}")
            
        except Exception as e:
            current_app.logger.error(f"Erro ao garantir cliente ativo: {str(e)}")
            db.session.rollback()
"""

    # Criar arquivo cliente_status.py
    app_dir = os.path.dirname(os.path.abspath(app.root_path))
    status_path = os.path.join(app.root_path, "cliente_status.py")
    
    with open(status_path, "w") as f:
        f.write(conteudo)
    
    print(f"✅ Arquivo criado: {status_path}")
    
    # Modificar app.py para importar e usar o cliente_status
    app_path = os.path.join(app.root_path, "app.py")
    
    with open(app_path, "r") as f:
        app_content = f.read()
    
    if "from app.cliente_status import garantir_cliente_ativo" not in app_content:
        # Encontrar a última importação
        linhas = app_content.split("\n")
        insert_idx = 0
        
        for i, linha in enumerate(linhas):
            if linha.startswith("import ") or linha.startswith("from "):
                insert_idx = i
        
        # Adicionar importação e chamada de função
        linhas.insert(insert_idx + 1, "from app.cliente_status import garantir_cliente_ativo")
        
        # Encontrar a criação do app
        for i, linha in enumerate(linhas):
            if "@app.before_first_request" in linha:
                break
        else:
            # Se não encontrar, adicionar antes da definição de rotas
            for i, linha in enumerate(linhas):
                if "@app.route" in linha:
                    linhas.insert(i, "\n@app.before_first_request\ndef _garantir_dados_consistentes():\n    garantir_cliente_ativo()\n")
                    break
        
        # Escrever de volta no arquivo
        with open(app_path, "w") as f:
            f.write("\n".join(linhas))
        
        print(f"✅ Arquivo modificado: {app_path}")
    else:
        print("⚠️ O arquivo app.py já contém a importação necessária.")

if __name__ == "__main__":
    try:
        print("Criando arquivo para garantir consistência de dados...")
        criar_arquivo_cliente_status()
        print("\nSucesso! Os arquivos foram criados/modificados.")
        print("Faça o deploy destes arquivos para o ambiente Render.")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        sys.exit(1)
