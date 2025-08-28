# config.py
import os
from urllib.parse import quote_plus

# Carregar variáveis do .env
from dotenv import load_dotenv
load_dotenv()

# Configurações do banco de dados
# Prioridade: DATABASE_URL do .env > SQLite padrão
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///./database/database.db'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave_super_secreta'
