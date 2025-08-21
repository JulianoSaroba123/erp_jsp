from extensoes import db
from datetime import datetime

class Orcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Aguardando')
    data_emissao = db.Column(db.Date, default=datetime.today)
    validade = db.Column(db.Date)
    valor_total = db.Column(db.Float, default=0)
    servicos_dados = db.Column(db.Text)
    produtos_dados = db.Column(db.Text)
    observacoes = db.Column(db.Text)
    pdf_path = db.Column(db.String(255))
    # Campos extras conforme necessidade

    def __repr__(self):
        return f'<Orcamento {self.codigo}>'
