from app.extensoes import db
from datetime import datetime


class Orcamento(db.Model):
    __tablename__ = 'orcamentos'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data = db.Column(db.Date, default=datetime.utcnow)
    validade = db.Column(db.Integer, nullable=True)
    servicos_json = db.Column(db.Text, nullable=True)
    produtos_json = db.Column(db.Text, nullable=True)
    valor_total = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), default='Pendente')
    condicao_pagamento_id = db.Column(db.Integer, db.ForeignKey('condicoes_pagamento.id'), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    cliente = db.relationship('Cliente', backref='orcamentos')
    condicao_pagamento = db.relationship('CondicaoPagamento', backref='orcamentos')

    def __repr__(self):
        return f'<Orcamento {self.codigo}>'

    def gerar_codigo(self):
        """Gera código automático para orçamento"""
        ultimo_orcamento = Orcamento.query.order_by(Orcamento.id.desc()).first()
        if ultimo_orcamento:
            numero = int(ultimo_orcamento.codigo[3:]) + 1
        else:
            numero = 1
        return f'ORC{numero:04d}'
