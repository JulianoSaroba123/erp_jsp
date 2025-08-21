import sys
import os
sys.path.insert(0, '.')

from flask import Flask
from extensoes import db

app = Flask(__name__)
# Caminho absoluto para o banco
db_path = os.path.join(os.getcwd(), 'database', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    from app.ordem_servico.arquivo_model import OSArquivo
    db.create_all()
    
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tabelas = inspector.get_table_names()
    
    print("Tabelas no banco:", tabelas)
    print("Tabela os_arquivos criada:", 'os_arquivos' in tabelas)
    
    if 'os_arquivos' in tabelas:
        colunas = inspector.get_columns('os_arquivos')
        print("Colunas da tabela os_arquivos:")
        for coluna in colunas:
            print(f"  - {coluna['name']}")
