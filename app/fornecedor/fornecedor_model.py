# fornecedor/fornecedor_model.py


from extensoes import db
from datetime import datetime
from sqlalchemy import UniqueConstraint


class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'
    __table_args__ = (
        UniqueConstraint('cpf_cnpj', name='uq_fornecedores_cpf_cnpj'),
        UniqueConstraint('codigo', name='uq_fornecedores_codigo'),
    )

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=False)  # Ex: FOR0001
    
    # Informações principais
    nome = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200))
    cpf_cnpj = db.Column(db.String(18), nullable=False)  # Mudança: cnpj -> cpf_cnpj
    
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
    
    # Informações comerciais (específicas para fornecedor)
    contato_comercial = db.Column(db.String(100))
    telefone_comercial = db.Column(db.String(20))
    email_comercial = db.Column(db.String(120))
    
    # Observações
    observacoes = db.Column(db.Text)
    
    # Controle
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'
    
    def gerar_codigo(self):
        """Gera código automático para fornecedor"""
        ultimo_fornecedor = Fornecedor.query.order_by(Fornecedor.id.desc()).first()
        if ultimo_fornecedor:
            numero = int(ultimo_fornecedor.codigo[3:]) + 1
        else:
            numero = 1
        return f'FOR{numero:04d}'
