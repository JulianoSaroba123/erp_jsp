#!/usr/bin/env python3
"""Script para testar criação de OS via POST"""

import requests
from datetime import date

# Dados para criar uma OS de teste
dados_os = {
    'cliente_id': '2',  # ID do cliente existente
    'data_emissao': str(date.today()),
    'status': 'Aberta',
    'equipamento_nome': 'Equipamento Teste',
    'problema_descrito': 'Problema de teste',
    'tecnico_responsavel': 'Técnico Teste',
    'servicos_json': '[]',
    'produtos_json': '[]',
    'parcelas_json': '[]'
}

try:
    # Fazer POST para criar OS
    response = requests.post('http://localhost:5000/os/nova', data=dados_os)
    print(f"Status Code: {response.status_code}")
    print(f"URL final: {response.url}")
    
    if response.status_code == 200:
        print("OS criada com sucesso!")
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Erro na requisição: {e}")
