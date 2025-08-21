import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Usa DATABASE_URL do ambiente (Render), senão SQLite local
db_path = os.path.join(basedir, 'database', 'database.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or f"sqlite:///{db_path.replace(os.sep, '/')}"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY', 'jsp-erp-secret-key-2025-ultra-secure-flask-sessions')
