# Criação das tabelas no banco de dados
from app import app
from app.extensoes import db

# Cria as tabelas
with app.app_context():
    db.create_all()
    print("✅ Tabelas criadas com sucesso!")
    
    # Verifica as tabelas criadas
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📋 Tabelas no banco: {tables}")
