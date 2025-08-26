# config.py
import os

# Configurações do banco de dados
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://usuario:senha@localhost:5432/jsp_erp'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua_chave_super_secreta_para_producao'
