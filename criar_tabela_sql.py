import sqlite3
import os
from flask import render_template
from models import OrdemServico
from sqlalchemy.orm import joinedload
import json

# Caminho para o banco de dados
db_path = os.path.join('database', 'database.db')

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criar tabela os_parcelas
sql = """
CREATE TABLE IF NOT EXISTS os_parcelas (
    id INTEGER PRIMARY KEY,
    ordem_servico_id INTEGER NOT NULL,
    numero_parcela INTEGER NOT NULL,
    valor_parcela REAL NOT NULL,
    data_vencimento DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Pendente',
    data_pagamento DATE,
    valor_pago REAL,
    forma_pagamento VARCHAR(50),
    FOREIGN KEY (ordem_servico_id) REFERENCES ordens_servico (id)
)
"""

cursor.execute(sql)
conn.commit()
conn.close()

print('Tabela os_parcelas criada com sucesso!')

@os_bp.route('/<int:os_id>/relatorio')
def relatorio_os(os_id):
    """Visualiza o relatório da OS em HTML"""
    ordem = OrdemServico.query.options(
        joinedload(OrdemServico.cliente),
        joinedload(OrdemServico.itens)
    ).get_or_404(os_id)

    # Carregar dados JSON se existirem
    servicos_dados = []
    produtos_dados = []
    parcelas = []
    try:
        if ordem.servicos_dados:
            servicos_dados = json.loads(ordem.servicos_dados)
        if ordem.produtos_dados:
            produtos_dados = json.loads(ordem.produtos_dados)
        if ordem.parcelas:
            parcelas = json.loads(ordem.parcelas)
    except Exception:
        pass

    return render_template(
        'relatorio_os.html',
        os=ordem,
        servicos_dados=servicos_dados,
        produtos_dados=produtos_dados,
        parcelas=parcelas,
        total_servicos=ordem.valor_servicos,
        total_produtos=ordem.valor_produtos,
        valor_total=ordem.valor_total
    )
