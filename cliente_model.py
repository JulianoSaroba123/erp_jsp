from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20))  # Novo campo: código do cliente
    nome = db.Column(db.String(100), nullable=False)
    cpf_cnpj = db.Column(db.String(18), nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    endereco = db.Column(db.String(200))
    numero = db.Column(db.String(10))  # Novo campo: número da residência
