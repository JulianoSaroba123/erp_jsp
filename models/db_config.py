# models/db_config.py

# Responsável por criar a instância do SQLAlchemy
# que será compartilhada entre os modelos e o app

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
