"""Adiciona tabela de lançamentos financeiros vinculados à OS

Revision ID: 0003_lancamentos_financeiros_os
Revises: (usar o último ID atual)
Create Date: 2025-09-05

"""
from alembic import op
import sqlalchemy as sa
from decimal import Decimal

# revision identifiers
revision = '0003_lancamentos_financeiros_os'
down_revision = None  # Insira aqui o último ID de revisão

def upgrade():
    # Criação da tabela de lançamentos financeiros de OS
    op.create_table(
        'financeiro_lancamentos_os',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('os_id', sa.Integer(), nullable=True),
        sa.Column('descricao', sa.String(length=255), nullable=False),
        sa.Column('valor', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('data_vencimento', sa.Date(), nullable=False),
        sa.Column('data_pagamento', sa.Date(), nullable=True),
        sa.Column('forma_pagamento', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=20), server_default='Pendente', nullable=True),
        sa.Column('parcela', sa.Integer(), nullable=True),
        sa.Column('total_parcelas', sa.Integer(), nullable=True),
        sa.Column('origem', sa.String(length=30), server_default='OS', nullable=True),
        sa.ForeignKeyConstraint(['os_id'], ['ordens_servico.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Cria índice para busca por OS
    op.create_index(op.f('ix_financeiro_lancamentos_os_os_id'), 'financeiro_lancamentos_os', ['os_id'], unique=False)
    
    # Adicionar campos relacionados na tabela de OS
    op.add_column('ordens_servico', sa.Column('condicao_pagamento', sa.String(length=50), nullable=True))
    op.add_column('ordens_servico', sa.Column('qtd_parcelas', sa.Integer(), nullable=True))
    op.add_column('ordens_servico', sa.Column('valor_entrada', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('ordens_servico', sa.Column('status_pagamento', sa.String(length=20), nullable=True))
    op.add_column('ordens_servico', sa.Column('schedule_json', sa.Text(), nullable=True))


def downgrade():
    # Remover campos adicionados à OS
    op.drop_column('ordens_servico', 'schedule_json')
    op.drop_column('ordens_servico', 'status_pagamento')
    op.drop_column('ordens_servico', 'valor_entrada')
    op.drop_column('ordens_servico', 'qtd_parcelas')
    op.drop_column('ordens_servico', 'condicao_pagamento')
    
    # Remover índice
    op.drop_index(op.f('ix_financeiro_lancamentos_os_os_id'), table_name='financeiro_lancamentos_os')
    
    # Remover tabela de lançamentos
    op.drop_table('financeiro_lancamentos_os')
