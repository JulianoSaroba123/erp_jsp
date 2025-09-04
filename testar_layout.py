"""
Script para testar as melhorias de layout no ambiente local.
Este script inicia o servidor Flask para você verificar as alterações.
"""

import os
import sys

def iniciar_servidor_teste():
    """Inicia o servidor Flask em modo de desenvolvimento"""
    try:
        print("=== TESTE DE LAYOUT - CENTRALIZAÇÂO ===")
        print("Iniciando servidor Flask para teste...")
        print("\nApós iniciar o servidor:")
        print("1. Acesse http://localhost:5000")
        print("2. Faça login no sistema")
        print("3. Vá para a página de Clientes")
        print("4. Verifique se o layout está centralizado")
        print("\nPresione Ctrl+C para parar o servidor")
        print("=" * 50)
        
        # Definir variáveis de ambiente para desenvolvimento
        os.environ['DEBUG'] = 'True'
        os.environ['FLASK_ENV'] = 'development'
        
        # Importar e executar a aplicação
        from app.app import app
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except KeyboardInterrupt:
        print("\n\nServidor interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro ao iniciar servidor: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("Iniciando teste de layout...")
    iniciar_servidor_teste()
