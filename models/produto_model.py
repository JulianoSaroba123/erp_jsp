from models import db
from datetime import datetime

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nome = db.Column(db.String(100), nullable=False)

    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))
    fornecedor = db.relationship('Fornecedor', backref='produtos')

    unidade = db.Column(db.String(20))
    classificacao = db.Column(db.String(50))
    localizacao = db.Column(db.String(50))
    situacao = db.Column(db.String(20))
    valor_compra = db.Column(db.Float, default=0.0)
    valor_venda = db.Column(db.Float, default=0.0)
    markup_percentual = db.Column(db.Float, default=0.0)
    lucro_percentual = db.Column(db.Float, default=0.0)
    estoque = db.Column(db.Integer, default=0)

    fabricante = db.Column(db.String(100))
    

    def __repr__(self):
        return f"<Produto {self.codigo} - {self.nome}>"