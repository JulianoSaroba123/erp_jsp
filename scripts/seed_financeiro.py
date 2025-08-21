from app.financeiro.financeiro_model import LancamentoFinanceiro
from extensoes import db

categorias = [
    dict(tipo='Receita', categoria='Serviços', descricao='Receita de Serviços', valor=1000, data=None, forma_pagamento='Dinheiro', status='Pago', observacoes='Exemplo'),
    dict(tipo='Receita', categoria='Peças', descricao='Receita de Peças', valor=500, data=None, forma_pagamento='Cartão', status='Pendente', observacoes='Exemplo'),
    dict(tipo='Despesa', categoria='Deslocamento', descricao='Despesa de Deslocamento', valor=200, data=None, forma_pagamento='Boleto', status='Atrasado', observacoes='Exemplo'),
]

def seed():
    for c in categorias:
        lanc = LancamentoFinanceiro(
            tipo=c['tipo'],
            categoria=c['categoria'],
            descricao=c['descricao'],
            valor=c['valor'],
            data=None,
            forma_pagamento=c['forma_pagamento'],
            status=c['status'],
            observacoes=c['observacoes']
        )
        db.session.add(lanc)
    db.session.commit()
    print('Seed financeiro inserido.')

if __name__ == '__main__':
    seed()
