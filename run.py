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
from flask_migrate import upgrade

def deploy():
    """Run deployment tasks."""
    # Create database tables
    upgrade()

if __name__ == '__main__':
    # Em produção (Render), executar migrações automaticamente
    if os.environ.get('DATABASE_URL'):
        deploy()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
