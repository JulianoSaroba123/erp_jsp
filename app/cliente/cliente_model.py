# cliente/cliente_model.py

from extensoes import db
from datetime import datetime


from sqlalchemy import UniqueConstraint

class Cliente(db.Model):
    __tablename__ = 'clientes'
    __table_args__ = (
        UniqueConstraint('cpf_cnpj', name='uq_clientes_cpf_cnpj'),
    )

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=False)
    
    # Informações principais
    nome = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200))
    cpf_cnpj = db.Column(db.String(18), nullable=False)
    
    # Contato
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20), nullable=False)
    
    # Endereço
    cep = db.Column(db.String(9))
    endereco = db.Column(db.String(200))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    uf = db.Column(db.String(2))  # Mudança: estado -> uf
    pais = db.Column(db.String(50), default='Brasil')
    
    # Informações fiscais
    inscricao_estadual = db.Column(db.String(20))
    inscricao_municipal = db.Column(db.String(20))
    
    # Observações
    observacoes = db.Column(db.Text)
    
    # Controle
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Cliente {self.nome}>'
    
    def gerar_codigo(self):
        """Gera código automático para cliente"""
        ultimo_cliente = Cliente.query.order_by(Cliente.id.desc()).first()
        if ultimo_cliente:
            numero = int(ultimo_cliente.codigo[3:]) + 1
        else:
            numero = 1
        return f'CLI{numero:04d}'
