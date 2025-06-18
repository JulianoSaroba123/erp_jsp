# models/servico_model.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    valor = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(20))
    situacao = db.Column(db.String(20))  # Ativo / Inativo

    def __repr__(self):
        return f"<Servico {self.nome}>"

