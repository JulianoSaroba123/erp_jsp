from models.db_config import db
from datetime import datetime

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)

    # Código do produto (ex: PRD0001), gerado automaticamente
    codigo = db.Column(db.String(20), unique=True)

    # Nome do produto (obrigatório)
    nome = db.Column(db.String(100), nullable=False)

    # Fornecedor vinculado (relacionamento externo)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))
    fornecedor = db.relationship('Fornecedor', backref='produtos')

    # Dados de estoque e financeiro
    unidade = db.Column(db.String(20))
    classificacao = db.Column(db.String(50))
    localizacao = db.Column(db.String(50))
    situacao = db.Column(db.String(20))
    valor_compra = db.Column(db.Float, default=0.0)
    valor_venda = db.Column(db.Float, default=0.0)
    markup_percentual = db.Column(db.Float, default=0.0)
    lucro_percentual = db.Column(db.Float, default=0.0)
    estoque = db.Column(db.Integer, default=0)

    # Informações adicionais
    fabricante = db.Column(db.String(100))
    numero_serie = db.Column(db.String(50))

    
    def __repr__(self):
        return f"<Produto {self.codigo} - {self.nome}>"
