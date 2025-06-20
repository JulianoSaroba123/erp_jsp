from models import db
from datetime import datetime

class OrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, nullable=False)  # ID do cliente
    nome_cliente = db.Column(db.String(100), nullable=False)
    documento_cliente = db.Column(db.String(20), nullable=True)
    telefone_cliente = db.Column(db.String(20), nullable=True)
    email_cliente = db.Column(db.String(100), nullable=True)
    endereco_servico = db.Column(db.String(200), nullable=True)

    numero_os = db.Column(db.String(20), nullable=False)
    data_emissao = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    previsao_conclusao = db.Column(db.Date, nullable=True)
    tipo_servico = db.Column(db.String(30), nullable=False)
    descricao_servico = db.Column(db.Text, nullable=True)

    # Produtos/Peças (armazenar como JSON para facilitar os "extras")
    produtos = db.Column(db.Text, nullable=True)

    tecnico_responsavel = db.Column(db.String(100), nullable=False)
    hora_inicio = db.Column(db.String(5), nullable=True)
    hora_termino = db.Column(db.String(5), nullable=True)
    total_horas = db.Column(db.String(10), nullable=True)
    atividade_realizada = db.Column(db.Text, nullable=True)

    km_inicial = db.Column(db.Float, nullable=True)
    km_final = db.Column(db.Float, nullable=True)
    total_km = db.Column(db.Float, nullable=True)

    valor_servicos = db.Column(db.Float, nullable=True)
    valor_produtos = db.Column(db.Float, nullable=True)
    valor_deslocamento = db.Column(db.Float, nullable=True)
    total_geral = db.Column(db.Float, nullable=True)
    condicoes_pagamento = db.Column(db.String(100), nullable=True)

    observacoes = db.Column(db.Text, nullable=True)

    assinatura_tecnico = db.Column(db.String(200), nullable=True)  # (futuro: base64/img)
    assinatura_cliente = db.Column(db.String(200), nullable=True)
