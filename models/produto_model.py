from models import db

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo_barras = db.Column(db.String(50), nullable=True)
    data = db.Column(db.Date, nullable=True)
    fornecedor = db.Column(db.String(100), nullable=True)
    unidade = db.Column(db.String(20), nullable=True)
    classificacao = db.Column(db.String(50), nullable=True)
    localizacao = db.Column(db.String(100), nullable=True)
    situacao = db.Column(db.String(20), default='Ativo')
    valor_venda = db.Column(db.Float, nullable=True)
    valor_compra = db.Column(db.Float, nullable=True)
    estoque = db.Column(db.Integer, nullable=True)
    lucro = db.Column(db.Float, nullable=True)
    fabricante = db.Column(db.String(100), nullable=True)
    numero_serie = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Produto {self.nome}>"

