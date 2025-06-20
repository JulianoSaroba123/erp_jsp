from models import db
from datetime import datetime

class OrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # 1. Dados do Cliente
    cliente_nome = db.Column(db.String(120), nullable=False)
    cliente_cnpj_cpf = db.Column(db.String(20), nullable=True)
    cliente_telefone = db.Column(db.String(20), nullable=True)
    cliente_email = db.Column(db.String(100), nullable=True)
    cliente_endereco = db.Column(db.String(200), nullable=True)

    # 2. Detalhes da OS
    numero_os = db.Column(db.String(20), nullable=False)
    data_emissao = db.Column(db.Date, default=datetime.utcnow)
    previsao_conclusao = db.Column(db.Date, nullable=True)
    tipo_servico = db.Column(db.String(30), nullable=True)  # manutenção, instalação, etc.
    descricao_servico = db.Column(db.Text, nullable=True)

    # 3. Produtos/Peças (armazenado como JSON)
    produtos_json = db.Column(db.Text, nullable=True)  # Salvar lista de produtos/peças como texto JSON

    # 4. Horas Trabalhadas
    tecnico_responsavel = db.Column(db.String(100), nullable=True)
    hora_inicio = db.Column(db.String(10), nullable=True)    # Exemplo: "08:30"
    hora_termino = db.Column(db.String(10), nullable=True)   # Exemplo: "12:15"
    total_horas = db.Column(db.String(10), nullable=True)    # Exemplo: "3:45"
    atividade_realizada = db.Column(db.Text, nullable=True)

    # 5. Deslocamento
    km_inicial = db.Column(db.Integer, nullable=True)
    km_final = db.Column(db.Integer, nullable=True)
    total_km = db.Column(db.Integer, nullable=True)

    # 6. Valores
    valor_servicos = db.Column(db.Float, nullable=True)
    valor_produtos = db.Column(db.Float, nullable=True)
    valor_deslocamento = db.Column(db.Float, nullable=True)
    total_geral = db.Column(db.Float, nullable=True)
    condicoes_pagamento = db.Column(db.String(100), nullable=True)

    # 7. Observações
    observacoes = db.Column(db.Text, nullable=True)

    # 8. Assinaturas
    assinatura_tecnico = db.Column(db.Text, nullable=True)
    assinatura_cliente = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<OrdemServico {self.numero_os} - {self.cliente_nome}>"
