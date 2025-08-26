# init_db.py
"""
Script para inicializar o banco de dados no Render
"""
from app.app import app
from app.extensoes import db
from app.cliente.cliente_model import Cliente
from app.fornecedor.fornecedor_model import Fornecedor

def init_database():
    """Inicializa o banco de dados criando todas as tabelas"""
    with app.app_context():
        # Cria todas as tabelas
        db.create_all()
        print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_database()
