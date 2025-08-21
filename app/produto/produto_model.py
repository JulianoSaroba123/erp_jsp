# produto/produto_model.py

from extensoes import db
from datetime import datetime

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    unidade = db.Column(db.String(10), default='UN')  # UN, KG, M, etc
    
    # Controle de estoque
    estoque_atual = db.Column(db.Float, default=0.0)
    estoque_minimo = db.Column(db.Float, default=0.0)
    
    # Preços e markup
    preco_custo = db.Column(db.Float, nullable=False, default=0.0)
    markup_percentual = db.Column(db.Float, default=0.0)  # % de markup
    preco_venda = db.Column(db.Float, default=0.0)  # Calculado automaticamente
    
    # Dados complementares
    codigo_barras = db.Column(db.String(50))
    ncm = db.Column(db.String(20))  # Código fiscal
    peso = db.Column(db.Float)
    
    # Controle
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Produto {self.nome}>'
    
    def calcular_preco_venda(self):
        """Calcula o preço de venda baseado no custo e markup"""
        if self.preco_custo and self.markup_percentual:
            self.preco_venda = self.preco_custo * (1 + (self.markup_percentual / 100))
        else:
            self.preco_venda = self.preco_custo
        return self.preco_venda
    
    def calcular_markup_valor(self):
        """Calcula o valor em R$ do markup"""
        if self.preco_custo and self.markup_percentual:
            return self.preco_custo * (self.markup_percentual / 100)
        return 0.0
    
    def margem_lucro_percentual(self):
        """Calcula a margem de lucro em %"""
        if self.preco_venda and self.preco_custo and self.preco_venda > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_venda) * 100
        return 0.0
    
    def status_estoque(self):
        """Retorna o status do estoque (Crítico, Baixo, Normal)"""
        if self.estoque_atual <= 0:
            return "Zerado"
        elif self.estoque_atual <= self.estoque_minimo:
            return "Crítico"
        elif self.estoque_atual <= (self.estoque_minimo * 1.5):
            return "Baixo"
        else:
            return "Normal"
