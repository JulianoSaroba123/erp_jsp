#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from datetime import datetime

def test_form_simple():
    """Teste com HTML simples para isolar o problema"""
    
    # Primeiro, vamos obter a página GET para ter uma sessão válida
    get_response = requests.get("http://localhost:5000/os/nova")
    
    if get_response.status_code != 200:
        print(f"❌ Erro ao carregar página: {get_response.status_code}")
        return
    
    print("✅ Página carregada com sucesso")
    
    # Usar a mesma sessão para fazer o POST
    session = requests.Session()
    
    # Fazer GET primeiro
    get_resp = session.get("http://localhost:5000/os/nova")
    print(f"GET Response: {get_resp.status_code}")
    
    # Dados com valores para teste de cálculo
    dados = {
        'codigo': 'OS0006',
        'cliente_id': '2',
        'data_emissao': '2025-08-06',
        'equipamento_nome': 'Notebook Dell',
        'problema_descrito': 'Tela azul da morte',
        'tecnico_responsavel': 'João Silva',
        'hora_inicio': '08:00',
        'hora_termino': '12:00',
        'km_inicial': '1000',
        'km_final': '1050',
        'servicos_json': '[{"id": 1, "nome": "Formatação", "valor_unitario": 150.00, "quantidade": 1}]',
        'produtos_json': '[{"id": 1, "nome": "HD 1TB", "valor_unitario": 300.00, "quantidade": 1}]',
        'parcelas_json': '[]'
    }
    
    print(f"Dados para POST: {dados}")
    
    # Fazer POST
    post_resp = session.post("http://localhost:5000/os/nova", data=dados, allow_redirects=False)
    
    print(f"POST Response: {post_resp.status_code}")
    print(f"Headers: {dict(post_resp.headers)}")
    
    if 'Location' in post_resp.headers:
        print(f"Redirecionando para: {post_resp.headers['Location']}")
    
    # Mostrar parte do conteúdo
    print(f"Conteúdo (200 chars): {post_resp.text[:200]}")

if __name__ == "__main__":
    test_form_simple()
