from models import db

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)          # Código automático, tipo SRV00001
    nome = db.Column(db.String(100), nullable=False)        # Nome do serviço (Ex: Instalação Elétrica)
    valor = db.Column(db.Float, nullable=False)             # Valor do serviço
    unidade = db.Column(db.String(20), nullable=False)      # Unidade (Ex: Hora, Serviço, m²)
    situacao = db.Column(db.String(20), default='Ativo')    # Ativo/Inativo

    def __repr__(self):
        return f"<Servico {self.nome}>"
