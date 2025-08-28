# config.py
import os
from urllib.parse import quote_plus

# Melhor prática: usar variáveis de ambiente
usuario = os.getenv("DB_USER", "postgres")
senha = quote_plus(os.getenv("DB_PASS", "minhaçsenha"))

SQLALCHEMY_DATABASE_URI = f"postgresql://{usuario}:{senha}@localhost:5432/jsp_erp"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave_super_secreta'
