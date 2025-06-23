from models import db

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)            # Código automático: PRD00001
    nome = db.Column(db.String(100), nullable=False)          # Nome do Produto
    codigo_barras = db.Column(db.String(50), nullable=True)   # Código de Barras (opcional)
    data = db.Column(db.Date, nullable=True)                  # Data de cadastro/entrada
    fornecedor = db.Column(db.String(100), nullable=True)     # Nome do fornecedor
    unidade = db.Column(db.String(20), nullable=True)         # Unidade de medida (ex: UN, PÇ, KG)
    classificacao = db.Column(db.String(50), nullable=True)   # Categoria ou tipo
    localizacao = db.Column(db.String(100), nullable=True)    # Onde está no estoque
    situacao = db.Column(db.String(20), default='Ativo')      # Ativo/Inativo
    valor_venda = db.Column(db.Float, nullable=True)          # Preço de venda
    valor_compra = db.Column(db.Float, nullable=True)         # Preço de compra
    estoque = db.Column(db.Integer, nullable=True)            # Quantidade em estoque
    lucro = db.Column(db.Float, nullable=True)                # Percentual de lucro
    fabricante = db.Column(db.String(100), nullable=True)     # Fabricante
    numero_serie = db.Column(db.String(100), nullable=True)   # Número de série (opcional)

    def __repr__(self):
        return f"<Produto {self.nome}>"
