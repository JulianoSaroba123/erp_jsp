#!/usr/bin/env python3
"""
Teste de debug para verificar erros na aplicação
"""
import sys
import os
import traceback

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔍 Iniciando debug da aplicação...")
    
    # Testar importação do app
    from app import app
    print("✅ App importado com sucesso!")
    
    # Testar as rotas
    with app.app_context():
        print("\n📍 Rotas registradas:")
        for rule in app.url_map.iter_rules():
            print(f"  - {rule.rule} -> {rule.endpoint}")
    
    # Testar se o template index.html existe
    print(f"\n📁 Verificando templates...")
    import os
    template_path = os.path.join(os.getcwd(), 'templates', 'index.html')
    if os.path.exists(template_path):
        print(f"✅ Template index.html encontrado: {template_path}")
    else:
        print(f"❌ Template index.html NÃO encontrado: {template_path}")
    
    # Testar renderização
    print(f"\n🎨 Testando renderização...")
    with app.test_client() as client:
        response = client.get('/')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Rota principal funcionando!")
            print(f"Primeiros 200 chars: {response.get_data(as_text=True)[:200]}...")
        else:
            print(f"❌ Erro na rota principal: {response.status_code}")
            print(f"Dados: {response.get_data(as_text=True)}")
            
except Exception as e:
    print(f"❌ ERRO: {e}")
    print("\n🔍 Traceback completo:")
    traceback.print_exc()
