import os
os.environ['FLASK_APP'] = 'run.py'

from app.app import app
from flask_migrate import upgrade

with app.app_context():
    try:
        print("Aplicando migrações...")
        upgrade()
        print("✅ Migrações aplicadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao aplicar migrações: {e}")
        
    # Verificar clientes
    from app.cliente.cliente_model import Cliente
    from app.extensoes import db
    
    try:
        total = Cliente.query.count()
        print(f"Total de clientes no banco: {total}")
        
        if total > 0:
            cliente = Cliente.query.first()
            print(f"Primeiro cliente ativo: {cliente.ativo}")
            print(f"Primeiro cliente país: {cliente.pais}")
    except Exception as e:
        print(f"Erro ao verificar clientes: {e}")
