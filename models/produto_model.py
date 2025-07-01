from models.db_config import db
from datetime import datetime


class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)

    # Código de barras do produto
    codigo_barras = db.Column(db.String(50), unique=True)

    # Nome do produto
    nome = db.Column(db.String(100), nullable=False)

    # Data de cadastro
    data = db.Column(db.Date, default=datetime.utcnow)

    # Fornecedor (relacionamento opcional, se quiser fazer depois)
    fornecedor = db.Column(db.String(100))

    # Unidade de medida (ex: UN, KG, PÇ)
    unidade = db.Column(db.String(10))

    # Classificação do produto (categoria)
    classificacao = db.Column(db.String(50))

    # Localização física (ex: prateleira A2)
    localizacao = db.Column(db.String(50))

    # Situação: Ativo ou Inativo
    situacao = db.Column(db.String(20), default='Ativo')

    # Valores de venda e compra
    valor_venda = db.Column(db.Float)
    valor_compra = db.Column(db.Float)

    # Estoque atual
    estoque = db.Column(db.Integer)

    # Percentual de lucro
    lucro_percentual = db.Column(db.Float)

    # Fabricante
    fabricante = db.Column(db.String(100))

    # Número de série do produto (caso aplicável)
    numero_serie = db.Column(db.String(100))

    def __repr__(self):
        return f'<Produto {self.nome}>'
