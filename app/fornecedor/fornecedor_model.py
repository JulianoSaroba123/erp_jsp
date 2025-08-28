# fornecedor_model.py
from app.extensoes import db
from datetime import datetime

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    cep = db.Column(db.String(10), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'cnpj': self.cnpj,
            'telefone': self.telefone,
            'cep': self.cep,
            'cidade': self.cidade,
            'endereco': self.endereco
        }
