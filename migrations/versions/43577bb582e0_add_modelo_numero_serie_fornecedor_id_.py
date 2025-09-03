"""add modelo numero_serie fornecedor_id em produtos

Revision ID: 43577bb582e0
Revises: 4a628181284f
Create Date: 2025-08-27 19:10:02.861105

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "43577bb582e0"
down_revision = "4a628181284f"
branch_labels = None
depends_on = None


def upgrade():
    # SQLite: use batch + dê NOME às constraints
    with op.batch_alter_table("produtos", schema=None) as batch:
        # Verificar se as colunas já existem antes de adicionar
        from sqlalchemy import inspect
        conn = op.get_bind()
        inspector = inspect(conn)
        columns = [col['name'] for col in inspector.get_columns('produtos')]
        
        if 'modelo' not in columns:
            batch.add_column(sa.Column("modelo", sa.String(length=120), nullable=True))
        if 'numero_serie' not in columns:
            batch.add_column(sa.Column("numero_serie", sa.String(length=120), nullable=True))
        if 'fornecedor_id' not in columns:
            batch.add_column(sa.Column("fornecedor_id", sa.Integer(), nullable=True))

        # FK COM NOME EXPLÍCITO - verificar se já existe
        fks = inspector.get_foreign_keys('produtos')
        fk_exists = any(fk['name'] == 'fk_produtos_fornecedor_id_fornecedores' for fk in fks)
        
        if not fk_exists and 'fornecedor_id' in columns or 'fornecedor_id' not in columns:
            batch.create_foreign_key(
                "fk_produtos_fornecedor_id_fornecedores",  # <- nome obrigatório
                referent_table="fornecedores",
                local_cols=["fornecedor_id"],
                remote_cols=["id"],
            ondelete="SET NULL",
        )


def downgrade():
    with op.batch_alter_table("produtos", schema=None) as batch:
        # Remova a FK PELO NOME
        batch.drop_constraint(
            "fk_produtos_fornecedor_id_fornecedores",
            type_="foreignkey",
        )
        batch.drop_column("fornecedor_id")
        batch.drop_column("numero_serie")
        batch.drop_column("modelo")
