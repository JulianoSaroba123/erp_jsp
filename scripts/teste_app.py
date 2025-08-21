#!/usr/bin/env python3
"""
Teste simples para verificar se a aplicação inicia sem erros
"""
import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("✅ Aplicação importada com sucesso!")
    
    # Verificar se as rotas foram registradas
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"  📍 {rule.rule} -> {rule.endpoint}")
    
    print("\n✅ Todas as rotas foram registradas corretamente!")
    print("🚀 A aplicação está pronta para ser executada!")
    
except Exception as e:
    print(f"❌ Erro ao importar aplicação: {e}")
    import traceback
    traceback.print_exc()
