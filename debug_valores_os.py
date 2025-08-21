#!/usr/bin/env python3
"""
Script para debugar valores da OS14
"""

import sys
import os

# Adiciona o diretório app ao path para importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import app
from ordem_servico.os_model import OrdemServico

def debug_os_14():
    with app.app_context():
        os = OrdemServico.query.get(14)
        if os:
            print(f"=== OS ID: {os.id} ===")
            print(f"Código: {os.codigo}")
            print(f"Cliente: {os.cliente.nome if os.cliente else 'N/A'}")
            print(f"Status: {os.status}")
            print(f"Valor Total: {os.valor_total}")
            print(f"Valor Serviços: {os.valor_servicos}")
            print(f"Valor Produtos: {os.valor_produtos}")
            print(f"Total Horas: {os.total_horas}")
            
            print(f"\n=== ITENS DA OS ===")
            if hasattr(os, 'itens') and os.itens:
                for i, item in enumerate(os.itens):
                    print(f"Item {i+1}:")
                    print(f"  Tipo: {getattr(item, 'tipo_item', 'N/A')}")
                    print(f"  Descrição: {getattr(item, 'descricao', 'N/A')}")
                    print(f"  Quantidade: {getattr(item, 'quantidade', 'N/A')}")
                    print(f"  Valor Unitário: {getattr(item, 'valor_unitario', 'N/A')}")
                    print(f"  Valor Total: {getattr(item, 'valor_total', 'N/A')}")
            else:
                print("Nenhum item detalhado encontrado")
                
            print(f"\n=== SERVIÇOS ===")
            if hasattr(os, 'servicos'):
                for i, servico in enumerate(os.servicos):
                    print(f"Serviço {i+1}:")
                    print(f"  Nome: {servico.nome}")
                    print(f"  Horas: {servico.horas}")
                    print(f"  Valor por Hora: {servico.valor_por_hora}")
                    print(f"  Valor Total: {servico.valor_total}")
            else:
                print("Nenhum serviço encontrado")
                
            print(f"\n=== PRODUTOS ===")
            if hasattr(os, 'produtos'):
                for i, produto in enumerate(os.produtos):
                    print(f"Produto {i+1}:")
                    print(f"  Nome: {produto.nome}")
                    print(f"  Quantidade: {produto.quantidade}")
                    print(f"  Valor Unitário: {produto.valor_unitario}")
                    print(f"  Valor Total: {produto.valor_total}")
            else:
                print("Nenhum produto encontrado")
                
        else:
            print("OS 14 não encontrada")

if __name__ == '__main__':
    try:
        debug_os_14()
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
