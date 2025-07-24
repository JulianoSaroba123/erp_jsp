from models import db
from datetime import datetime

class OrdemServico(db.Model):
    __tablename__ = 'ordens_servico'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20))

    # Dados do cliente (salvos na OS)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    cliente = db.relationship('Cliente', backref='ordens_servico')
    cliente_nome = db.Column(db.String(100))
    cliente_cpf_cnpj = db.Column(db.String(20))
    cliente_telefone = db.Column(db.String(20))
    cliente_email = db.Column(db.String(100))
    cliente_endereco = db.Column(db.String(200))

    data_emissao = db.Column(db.Date)
    previsao_conclusao = db.Column(db.Date)
    tipo_servico = db.Column(db.String(50))
    tecnico_responsavel = db.Column(db.String(100))
    tecnico = db.Column(db.String(120))  # Adicione este campo
    hora_inicio = db.Column(db.String(10))
    hora_termino = db.Column(db.String(10))
    total_horas = db.Column(db.String(10))
    atividade_realizada = db.Column(db.Text)

    servico_nome = db.Column(db.String(100))
    descricao_servico = db.Column(db.Text)
    qtd_servico = db.Column(db.String(10))
    valor_unit_servico = db.Column(db.String(20))

    servicos = db.Column(db.Text)  # Para armazenar os serviços em JSON
    produtos = db.Column(db.Text)  # Para armazenar os produtos em JSON

    km_inicial = db.Column(db.Float)
    km_final = db.Column(db.Float)
    km_total = db.Column(db.Float)
    valor_servicos = db.Column(db.Float)
    valor_produtos = db.Column(db.Float)
    valor_deslocamento = db.Column(db.Float)
    total_geral = db.Column(db.Float)

    condicoes_pagamento = db.Column(db.String(100), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<OrdemServico {self.codigo}>"

