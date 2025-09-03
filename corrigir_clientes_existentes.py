#!/usr/bin/env python3
"""
Script para corrigir clientes existentes no banco:
- Definir país como 'Brasil' onde estiver None/NULL
- Definir ativo como True onde estiver False/NULL
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.app import app
from app.extensoes import db
from app.cliente.cliente_model import Cliente

def corrigir_clientes():
    with app.app_context():
        print("🔧 Corrigindo clientes existentes...")
        
        # Buscar clientes com problemas
        clientes_com_problema = Cliente.query.filter(
            (Cliente.pais.is_(None)) | 
            (Cliente.pais == '') |
            (Cliente.ativo.is_(None)) |
            (Cliente.ativo == False)
        ).all()
        
        if not clientes_com_problema:
            print("✅ Nenhum cliente com problema encontrado!")
            return
        
        print(f"📋 Encontrados {len(clientes_com_problema)} clientes para corrigir:")
        
        for cliente in clientes_com_problema:
            print(f"  - {cliente.nome} (ID: {cliente.id})")
            
            # Corrigir país
            if not cliente.pais or cliente.pais.strip() == '':
                cliente.pais = 'Brasil'
                print(f"    ✅ País definido como 'Brasil'")
            
            # Corrigir ativo
            if cliente.ativo is None or cliente.ativo is False:
                cliente.ativo = True
                print(f"    ✅ Status definido como Ativo")
        
        # Salvar alterações
        try:
            db.session.commit()
            print(f"\n🎉 {len(clientes_com_problema)} clientes corrigidos com sucesso!")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erro ao salvar: {e}")

if __name__ == '__main__':
    corrigir_clientes()
