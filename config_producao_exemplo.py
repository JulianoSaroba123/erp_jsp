# Exemplo de config.py para produção (Render)
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Banco de dados: use variável de ambiente DATABASE_URL se disponível (Render/Postgres), senão SQLite local
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
    "sqlite:///" + os.path.join(PROJECT_ROOT, "database.db")
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Chave secreta para sessões Flask
SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")

# Outras configs de produção podem ser adicionadas aqui
