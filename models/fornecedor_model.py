from flask_sqlalchemy import SQLAlchemy
from models import db

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    endereco = db.Column(db.String(100))
    numero = db.Column(db.String(10))

    def __repr__(self):
        return f"<Fornecedor {self.nome}>"
