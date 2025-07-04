"""migração inicial

Revision ID: 45040291b052
Revises: 
Create Date: 2025-07-01 08:35:42.599210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45040291b052'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fornecedor')
    op.drop_table('cliente')
    op.drop_table('produto')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('produto',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('codigo', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('nome', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('codigo_barras', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('data', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('fornecedor', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('unidade', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('classificacao', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('localizacao', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('situacao', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('valor_venda', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('valor_compra', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('estoque', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lucro', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('fabricante', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('numero_serie', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('produto_pkey')),
    sa.UniqueConstraint('codigo', name=op.f('produto_codigo_key'))
    )
    op.create_table('cliente',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('codigo', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('nome', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('cpf_cnpj', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('telefone', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('endereco', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('numero', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('cliente_pkey')),
    sa.UniqueConstraint('codigo', name=op.f('cliente_codigo_key'))
    )
    op.create_table('fornecedor',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('codigo', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('nome', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('cnpj', sa.VARCHAR(length=18), autoincrement=False, nullable=False),
    sa.Column('telefone', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('cep', sa.VARCHAR(length=9), autoincrement=False, nullable=True),
    sa.Column('endereco', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('cidade', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('fornecedor_pkey')),
    sa.UniqueConstraint('codigo', name=op.f('fornecedor_codigo_key'))
    )
    # ### end Alembic commands ###
