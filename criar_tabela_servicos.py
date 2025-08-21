#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para criar tabela de serviços
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.extensoes import db
from app.servico.servico_model import Servico

# Importar app do run.py
from run import app

def criar_tabela_servicos():
    """Cria tabela de serviços no banco"""
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabela de serviços criada com sucesso!")
            
            # Verificar se existe serviços de exemplo
            count = Servico.query.count()
            print(f"📊 Total de serviços cadastrados: {count}")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabela: {e}")

if __name__ == "__main__":
    criar_tabela_servicos()
