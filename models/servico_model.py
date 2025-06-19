from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from models import db

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(10), nullable=False)
    situacao = db.Column(db.String(20), default='Ativo')  # Ativo/Inativo
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Servico {self.nome}>"

