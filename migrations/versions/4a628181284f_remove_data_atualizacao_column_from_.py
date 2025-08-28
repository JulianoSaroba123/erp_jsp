"""remove data_atualizacao column from produtos"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "4a628181284f"
down_revision = "bc520a607576"
branch_labels = None
depends_on = None


def upgrade():
    # Exemplo se for realmente remover a coluna:
    # op.drop_column("produtos", "data_atualizacao")
    pass


def downgrade():
    # Exemplo rollback:
    # op.add_column("produtos", sa.Column("data_atualizacao", sa.DateTime(), nullable=True))
    pass
