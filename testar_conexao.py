from app.extensoes import db
from app.app import app

# Testar conexão com o banco de dados
with app.app_context():
    try:
        db.session.execute('SELECT 1')
        print("Conexão com o banco de dados bem-sucedida!")
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
