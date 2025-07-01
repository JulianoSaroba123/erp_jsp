#from models import db
from models.db_config import db

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)          # Código automático, tipo SRV00001
    nome = db.Column(db.String(100), nullable=False)        # Nome do serviço (Ex: Instalação Elétrica)
    descricao = db.Column(db.Text, nullable=True)           # Descrição detalhada (opcional, mas útil!)
    valor = db.Column(db.Float, nullable=False)             # Valor do serviço
    unidade = db.Column(db.String(20), nullable=False)      # Unidade (Ex: Hora, Serviço, m²)
    situacao = db.Column(db.String(20), default='Ativo')    # Ativo/Inativo

    def __repr__(self):
        return f"<Servico {self.nome}>"