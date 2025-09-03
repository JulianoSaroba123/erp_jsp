# config.py
import os
from urllib.parse import quote_plus

# Carregar variáveis do .env
from dotenv import load_dotenv
load_dotenv()

# Configurações do banco de dados
# Prioridade: DATABASE_URL do .env > SQLite padrão
DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///./database/database.db'

# Correção SSL/TLS para Render PostgreSQL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
if DATABASE_URL and "sslmode" not in DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL += ("&sslmode=require" if "?" in DATABASE_URL else "?sslmode=require")

SQLALCHEMY_DATABASE_URI = DATABASE_URL

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave_super_secreta'
