# condicoes_pagamento/condicoes_pag_model.py

from extensoes import db
from datetime import datetime, timedelta

class CondicaoPagamento(db.Model):
    __tablename__ = 'condicoes_pagamento'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    
    # Configurações da condição
    tipo = db.Column(db.String(20), nullable=False)  # 'avista', 'parcelado', 'prazo'
    numero_parcelas = db.Column(db.Integer, default=1)
    dias_primeira_parcela = db.Column(db.Integer, default=0)  # Dias para primeira parcela
    intervalo_parcelas = db.Column(db.Integer, default=30)  # Dias entre parcelas
    
    # Controle
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CondicaoPagamento {self.nome}>'


class OSParcela(db.Model):
    __tablename__ = 'os_parcelas'
    
    id = db.Column(db.Integer, primary_key=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico.id'), nullable=False)
    
    # Dados da parcela
    numero_parcela = db.Column(db.Integer, nullable=False)
    valor_parcela = db.Column(db.Float, nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='Pendente')  # Pendente, Pago, Vencido
    data_pagamento = db.Column(db.Date)
    valor_pago = db.Column(db.Float)
    forma_pagamento = db.Column(db.String(50))
    
    # Relacionamento
    ordem_servico = db.relationship('OrdemServico', backref='parcelas')
    
    def __repr__(self):
        return f'<OSParcela OS:{self.ordem_servico_id} Parcela:{self.numero_parcela}>'
    
    @property
    def status_class(self):
        """Retorna classe CSS baseada no status"""
        if self.status == 'Pago':
            return 'success'
        elif self.status == 'Vencido':
            return 'danger'
        else:
            return 'warning'
