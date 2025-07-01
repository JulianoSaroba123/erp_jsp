# Importa a instância do banco configurada em db_config.py
from models.db_config import db
from datetime import datetime


class Cliente(db.Model):
    __tablename__ = 'clientes'  # Nome da tabela no banco de dados

    # ID único do cliente (chave primária)
    id = db.Column(db.Integer, primary_key=True)

    # Código do cliente (ex: CLT001), deve ser único
    codigo = db.Column(db.String(20), unique=True)

    # Nome completo ou razão social (obrigatório)
    nome = db.Column(db.String(100), nullable=False)

    # CPF ou CNPJ (obrigatório)
    cpf_cnpj = db.Column(db.String(20), nullable=False)

    # Telefone de contato
    telefone = db.Column(db.String(20))

    # E-mail do cliente
    email = db.Column(db.String(100))

    # Endereço completo
    endereco = db.Column(db.String(150))

    # Número do endereço (ex: 123A)
    numero = db.Column(db.String(10))

    # Data e hora de criação do registro
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Cliente {self.nome}>'
