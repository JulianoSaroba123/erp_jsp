"""Migração limpa para corrigir problemas nos clientes

Revision ID: e1234567890a
Revises: c1fef14f0146
Create Date: 2025-09-03 18:50:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e1234567890a'
down_revision = 'c1fef14f0146'
branch_labels = None
depends_on = None

def upgrade():
    # Corrigir dados de clientes que podem ter problemas
    try:
        # Garantir que todos os clientes tenham ativo = True por padrão
        op.execute("UPDATE clientes SET ativo = TRUE WHERE ativo IS NULL")
        
        # Garantir que todos os clientes tenham país = Brasil por padrão  
        op.execute("UPDATE clientes SET pais = 'Brasil' WHERE pais IS NULL OR pais = ''")
        
        print("✅ Dados de clientes corrigidos com sucesso")
    except Exception as e:
        print(f"Erro na correção: {e}")
        pass

def downgrade():
    # Não há necessidade de rollback para correções de dados
    pass
