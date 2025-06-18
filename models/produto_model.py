from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo_barras = db.Column(db.String(50))
    data = db.Column(db.Date, default=datetime.today)
    fornecedor = db.Column(db.String(100))
    unidade = db.Column(db.String(20))
    classificacao = db.Column(db.String(50))
    localizacao = db.Column(db.String(100))
    situacao = db.Column(db.String(20))  # Ativo / Inativo
    valor_venda = db.Column(db.Float)
    valor_compra = db.Column(db.Float)
    estoque = db.Column(db.Integer)
    lucro = db.Column(db.Float)
    fabricante = db.Column(db.String(100))
    numero_serie = db.Column(db.String(100))

    def __repr__(self):
        return f"<Produto {self.nome}>"

