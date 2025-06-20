from models import db

class OrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    cliente_nome = db.Column(db.String(100), nullable=False)
    cliente_cnpj_cpf = db.Column(db.String(20), nullable=True)
    cliente_telefone = db.Column(db.String(20), nullable=True)
    cliente_email = db.Column(db.String(100), nullable=True)
    cliente_endereco = db.Column(db.String(150), nullable=True)
    data_emissao = db.Column(db.Date, nullable=True)
    previsao_conclusao = db.Column(db.Date, nullable=True)
    tipo_servico = db.Column(db.String(50), nullable=True)
    descricao_servico = db.Column(db.Text, nullable=True)
    produtos = db.Column(db.Text, nullable=True)  # JSON string
    tecnico_responsavel = db.Column(db.String(100), nullable=True)
    hora_inicio = db.Column(db.String(10), nullable=True)
    hora_termino = db.Column(db.String(10), nullable=True)
    total_horas = db.Column(db.String(10), nullable=True)
    atividade_realizada = db.Column(db.Text, nullable=True)
    km_inicial = db.Column(db.String(10), nullable=True)
    km_final = db.Column(db.String(10), nullable=True)
    km_total = db.Column(db.String(10), nullable=True)
    valor_servicos = db.Column(db.Float, nullable=True)
    valor_produtos = db.Column(db.Float, nullable=True)
    valor_deslocamento = db.Column(db.Float, nullable=True)
    total_geral = db.Column(db.Float, nullable=True)
    condicoes_pagamento = db.Column(db.String(100), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<OrdemServico {self.codigo}>"
