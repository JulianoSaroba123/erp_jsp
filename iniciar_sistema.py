#!/usr/bin/env python3
"""
Script de inicialização do ERP JSP Elétrica
Configura o banco de dados e inicia o sistema
"""

import os
import sys
from pathlib import Path

def setup_database():
    """Configura o banco de dados SQLite"""
    print("🔧 Configurando banco de dados...")
    
    # Criar diretório database se não existir
    db_dir = Path("database")
    db_dir.mkdir(exist_ok=True)
    
    try:
        from app.extensoes import db
        from app.app import app
        
        with app.app_context():
            print("📦 Criando tabelas...")
            db.create_all()
            print("✅ Banco de dados configurado com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao configurar banco: {e}")
        return False

def start_server():
    """Inicia o servidor Flask"""
    print("🚀 Iniciando servidor JSP ERP...")
    
    try:
        from app.app import app
        
        print("\n" + "="*50)
        print("🏢 JSP ELÉTRICA - Sistema ERP")
        print("📍 URL: http://localhost:5000")
        print("🔧 Ambiente: Desenvolvimento")
        print("💾 Banco: SQLite (database/database.db)")
        print("="*50 + "\n")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
        
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return False

def main():
    """Função principal"""
    print("🏢 JSP ELÉTRICA - Inicializador do Sistema")
    print("-" * 40)
    
    # Configurar banco
    if not setup_database():
        print("❌ Falha na configuração do banco. Abortando...")
        sys.exit(1)
    
    # Iniciar servidor
    start_server()

if __name__ == "__main__":
    main()
