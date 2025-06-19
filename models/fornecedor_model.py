from flask_sqlalchemy import SQLAlchemy
from models import db

class Fornecedor(db.Model:
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False)       # Com formatação XX.XXX.XXX/0001-XX
    telefone = db.Column(db.String(15), nullable=False)   # Com formatação (XX) XXXXX-XXXX
    cep = db.Column(db.String(9), nullable=False)         # Formato XXXXX-XXX
    cidade = db.Column(db.String(50), nullable=False)
    endereco = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<Fornecedor {self.nome}>"
