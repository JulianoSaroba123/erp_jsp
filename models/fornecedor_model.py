from models.db_config import db
from datetime import datetime


class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'  # <- ESSENCIAL! Nome da tabela
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Fornecedor {self.nome}>"


       # Código identificador do fornecedor
    codigo = db.Column(db.String(20), unique=True)

    # Nome ou razão social do fornecedor
    nome = db.Column(db.String(100), nullable=False)

    # CNPJ do fornecedor
    cnpj = db.Column(db.String(20), unique=True)

    # Telefone de contato
    telefone = db.Column(db.String(20))

    # E-mail
    email = db.Column(db.String(100))

    # E-mail
    cep = db.Column(db.String(9))

    # Endereço completo
    endereco = db.Column(db.String(150))

    # Número (ex: 123, 123A)
    numero = db.Column(db.String(10))

    # Nome da cidade
    cidade = db.Column(db.String(100))

    # Estado (sigla ex: SP, RJ)
    estado = db.Column(db.String(2))

    # Data e hora de cadastro
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'
