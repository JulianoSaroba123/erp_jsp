import requests
import json

try:
    print("Testando API de busca de clientes...")
    
    # Testar vários termos
    termos = ['sergi', 'ser', 'Sergi', 'Yoshio', '077']
    
    for termo in termos:
        print(f"\n--- Testando termo: '{termo}' ---")
        url = f"http://127.0.0.1:5000/clientes/api/busca?q={termo}"
        print(f"URL: {url}")
        
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Dados retornados: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"Erro: {response.text}")
    
    print("\n--- Testando API sem parâmetros ---")
    url = "http://127.0.0.1:5000/clientes/api/busca"
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Dados: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"Erro: {response.text}")
        
except Exception as e:
    print(f"Erro ao testar API: {e}")
    import traceback
    traceback.print_exc()
