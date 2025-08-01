"""Adiciona campo data em produtos

Revision ID: 824a9b32ab88
Revises: 
Create Date: 2025-08-01 11:37:59.354874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '824a9b32ab88'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('produtos', sa.Column('data', sa.String(length=20), nullable=True))


def downgrade():
    op.drop_column('produtos', 'data')
