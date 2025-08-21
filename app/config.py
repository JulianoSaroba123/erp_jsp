import os
import pathlib

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or \
    f"sqlite:///{pathlib.Path(__file__).parent.parent / 'database' / 'database.db'}"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY", "jsp-erp-secret-key-2025-ultra-secure-flask-sessions")
# Certifique-se de que o diretório 'database' exista