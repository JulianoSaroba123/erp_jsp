#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para criar tabelas de ordem de serviço
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.extensoes import db
from app.ordem_servico.os_model import OrdemServico, OrdemServicoItem

# Importar app do run.py
from run import app

def criar_tabelas_os():
    """Cria tabelas de ordem de serviço no banco"""
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas de ordem de serviço criadas com sucesso!")
            
            # Verificar se existe OS de exemplo
            count = OrdemServico.query.count()
            print(f"📊 Total de ordens de serviço cadastradas: {count}")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")

if __name__ == "__main__":
    criar_tabelas_os()
