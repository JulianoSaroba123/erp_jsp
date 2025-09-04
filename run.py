#!/usr/bin/env python3
"""
Ponto de entrada principal do ERP JSP - Elétrica Industrial
Execute este arquivo para iniciar a aplicação Flask
"""

import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para permitir imports do pacote app
sys.path.insert(0, os.path.dirname(__file__))

from app.app import app

if __name__ == '__main__':
    # Configuração para produção (Render) e desenvolvimento
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'  # Debug ativado por padrão
    app.run(host='0.0.0.0', port=port, debug=debug)
