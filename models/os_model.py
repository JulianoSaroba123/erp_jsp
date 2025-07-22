# models/os_model.py

from models import db                # usa o mesmo db do app
from datetime import date, time
from models.cliente_model import Cliente


class OrdemServico(db.Model):
    __tablename__ = 'ordens_servico'

    id                  = db.Column(db.Integer,   primary_key=True)
    cliente_id          = db.Column(db.Integer,   db.ForeignKey('clientes.id'), nullable=False)
    cliente             = db.relationship('Cliente', backref=db.backref('ordens', lazy=True))

    codigo              = db.Column(db.String(20), unique=True, nullable=False)
    data_emissao        = db.Column(db.Date,       nullable=False, default=date.today)
    previsao_conclusao  = db.Column(db.Date,       nullable=True)

    tipo_servico        = db.Column(db.String(50), nullable=False)
    tecnico             = db.Column(db.String(100),nullable=False)

    hora_inicio         = db.Column(db.Time,       nullable=True)
    hora_termino        = db.Column(db.Time,       nullable=True)
    total_horas         = db.Column(db.String(5),  nullable=True)

    km_inicial          = db.Column(db.Float,      nullable=True)
    km_final            = db.Column(db.Float,      nullable=True)
    km_total            = db.Column(db.Float,      nullable=True)
    valor_deslocamento  = db.Column(db.Float,      nullable=True)

    servicos_json       = db.Column(db.Text,       nullable=True)
    produtos_json       = db.Column(db.Text,       nullable=True)

    valor_servicos      = db.Column(db.Float,      nullable=True)
    valor_produtos      = db.Column(db.Float,      nullable=True)
    valor_total         = db.Column(db.Float,      nullable=True)

    condicoes_pagamento = db.Column(db.String(200),nullable=True)
    observacoes         = db.Column(db.Text,       nullable=True)

    @property
    def servicos_realizados(self):
        """Retorna lista de serviços (nome, qtd, valor) como dicts."""
        return json.loads(self.servicos_json or '[]')

    @property
    def produtos_utilizados(self):
        """Retorna lista de produtos (nome, qtd, valor) como dicts."""
        return json.loads(self.produtos_json or '[]')

    def __repr__(self):
        return f"<OS {self.codigo} – Cliente {self.cliente_id}>"
