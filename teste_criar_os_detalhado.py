#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from datetime import datetime

# Teste simplificado de criação de OS
def testar_criar_os_detalhado():
    url = "http://localhost:5000/os/nova"
    
    # Dados mínimos do formulário
    dados = {
        'codigo': 'OS0003',
        'cliente_id': '2',  # SAROBA
        'data_emissao': datetime.now().strftime('%Y-%m-%d'),
        'status': 'Aberta',
        'equipamento_nome': 'Teste Equipamento',
        'problema_descrito': 'Teste Problema',
        'tecnico_responsavel': 'Teste Técnico'
    }
    
    print("=== TESTE DETALHADO DE CRIAÇÃO DE OS ===")
    print(f"URL: {url}")
    print(f"Dados enviados: {dados}")
    
    try:
        # Fazer POST
        response = requests.post(url, data=dados, allow_redirects=False)
        
        print(f"\n📋 RESPOSTA:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 302:
            location = response.headers.get('Location', 'Não informado')
            print(f"🔄 Redirecionamento para: {location}")
            
            # Seguir redirecionamento
            if location:
                follow_response = requests.get(location)
                print(f"📄 Página de destino - Status: {follow_response.status_code}")
                
        elif response.status_code == 200:
            print("📄 Permaneceu na mesma página (possível erro)")
            
        print(f"\n📝 Conteúdo da resposta (primeiros 500 chars):")
        print(response.text[:500])
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    testar_criar_os_detalhado()
