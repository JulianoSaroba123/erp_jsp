# servico/servico_model.py

from extensoes import db
from datetime import datetime

class Servico(db.Model):
    __tablename__ = 'servicos'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    
    # Informações principais
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    unidade = db.Column(db.String(10), default='UN')  # UN, H (hora), M2, etc
    
    # Preço
    valor = db.Column(db.Float, nullable=False, default=0.0)
    
    # Controle
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Servico {self.nome}>'
    
    def gerar_codigo(self):
        """Gera código automático para serviço"""
        ultimo_servico = Servico.query.order_by(Servico.id.desc()).first()
        if ultimo_servico:
            numero = int(ultimo_servico.codigo[3:]) + 1
        else:
            numero = 1
        return f'SRV{numero:04d}'
