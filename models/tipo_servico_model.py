# models/tipo_servico_model.py
from models import db

class TipoServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<TipoServico {self.nome}>"
