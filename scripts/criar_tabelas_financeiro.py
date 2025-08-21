from app import app
from extensoes import db
from app.financeiro import financeiro_model  # importa para registrar models

with app.app_context():
    db.create_all()
    print("Tabelas do Financeiro criadas.")
