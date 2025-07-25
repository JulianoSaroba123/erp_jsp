from models import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class OrdemServico(db.Model):
    __tablename__ = 'ordens_servico'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False)

    # 1. Dados do Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    cliente = db.relationship('Cliente', backref='ordens_servico')
    cliente_nome = db.Column(db.String(100))
    cliente_cpf_cnpj = db.Column(db.String(20))
    cliente_telefone = db.Column(db.String(20))
    cliente_email = db.Column(db.String(100))
    cliente_endereco = db.Column(db.String(200))

    # 2. Detalhes da OS
    data_emissao = db.Column(db.Date, default=datetime.utcnow)
    previsao_conclusao = db.Column(db.Date)
    tipo_servico = db.Column(db.String(50))
    tecnico_responsavel = db.Column(db.String(120))

    # 3. Equipamento
    equipamento_nome = db.Column(db.String(120))
    equipamento_marca = db.Column(db.String(120))
    equipamento_modelo = db.Column(db.String(120))
    equipamento_numero_serie = db.Column(db.String(120))
    equipamento_acessorios = db.Column(db.Text)
    equipamento_problema = db.Column(db.Text)

    # 4. Serviços Realizados (json)
    servicos = db.Column(db.Text)  # JSON list

    # 5. Produtos Utilizados (json)
    produtos = db.Column(db.Text)  # JSON list

    # 6. Horário e Atividades
    hora_inicio = db.Column(db.String(10))
    hora_termino = db.Column(db.String(10))
    total_horas = db.Column(db.String(10))

    # 7. Descrição do Serviço Realizado
    descricao_servico_realizado = db.Column(db.Text)

    # 8. Quilometragem / Deslocamento
    km_inicial = db.Column(db.Float)
    km_final = db.Column(db.Float)
    km_total = db.Column(db.Float)
    valor_deslocamento = db.Column(db.Float)

    # 9. Outras Informações / Condições de Pagamento
    condicoes_pagamento = db.Column(db.String(120))
    pago_parcelado = db.Column(db.Boolean, default=False)
    parcelas = db.Column(JSON)  # lista de dicts: [{"data": "YYYY-MM-DD", "valor": 0.0}, ...]

    # 10. Valores
    valor_servicos = db.Column(db.Float)
    valor_produtos = db.Column(db.Float)
    total_geral = db.Column(db.Float)

    # 11. Observações e Atividades
    atividade_realizada = db.Column(db.Text)
    outras_informacoes = db.Column(db.Text)
    tipo_cobranca = db.Column(db.String(20))

    def __repr__(self):
        return f"<OrdemServico {self.codigo}>"

