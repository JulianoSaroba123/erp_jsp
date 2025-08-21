#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime

# Teste de criação de OS
def testar_criar_os():
    url = "http://localhost:5000/os/nova"
    
    # Dados do formulário
    dados = {
        'codigo': 'OS0002',
        'cliente_id': '2',
        'data_emissao': datetime.now().strftime('%Y-%m-%d'),
        'status': 'Aberta',
        'equipamento_nome': 'Notebook Dell',
        'problema_descrito': 'Tela azul da morte',
        'tecnico_responsavel': 'João Silva',
        'servicos_json': '[]',
        'produtos_json': '[]',
        'parcelas_json': '[]'
    }
    
    try:
        print("Enviando dados para criar OS...")
        response = requests.post(url, data=dados)
        
        print(f"Status Code: {response.status_code}")
        print(f"URL final: {response.url}")
        
        if response.status_code == 200:
            print("✅ OS criada com sucesso!")
            print("Redirecionado para:", response.url)
        else:
            print("❌ Erro ao criar OS")
            print("Response:", response.text[:500])
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    testar_criar_os()
