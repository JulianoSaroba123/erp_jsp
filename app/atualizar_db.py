from app import app
from extensoes import db

with app.app_context():
    db.create_all()
    print("✅ Banco de dados atualizado com sucesso!")
    print("📋 Estruturas criadas para Cliente, Fornecedor e Produto")
