"""servicos: add markup_percentual + checks + backfill (Postgres)

- Adiciona markup_percentual (se não existir)
- Garante preco_venda/valor (se não existirem)
- Recalcula preco_venda e valor = preco_custo * (1 + markup/100)
- Adiciona CHECKs de não-negatividade (idempotente)
"""

from alembic import op
import sqlalchemy as sa

# >>> atualize down_revision para a SUA revisão anterior (veja `alembic history -v`)
revision = "c1fef14f0146"
down_revision = "43577bb582e0"
branch_labels = None
depends_on = None


def upgrade():
    # --- Criação de colunas (idempotente) ---
    op.execute("""
    DO $$
    BEGIN
      -- markup_percentual
      IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='servicos' AND column_name='markup_percentual'
      ) THEN
        ALTER TABLE servicos
          ADD COLUMN markup_percentual double precision NOT NULL DEFAULT 0;
        -- remove default para não "grudar" no schema
        ALTER TABLE servicos ALTER COLUMN markup_percentual DROP DEFAULT;
      END IF;

      -- preco_venda
      IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='servicos' AND column_name='preco_venda'
      ) THEN
        ALTER TABLE servicos
          ADD COLUMN preco_venda double precision NOT NULL DEFAULT 0;
        ALTER TABLE servicos ALTER COLUMN preco_venda DROP DEFAULT;
      END IF;

      -- valor (usado na listagem)
      IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='servicos' AND column_name='valor'
      ) THEN
        ALTER TABLE servicos
          ADD COLUMN valor double precision NOT NULL DEFAULT 0;
        ALTER TABLE servicos ALTER COLUMN valor DROP DEFAULT;
      END IF;
    END$$;
    """)

    # --- Backfill (recalcula preco_venda e espelha em valor) ---
    op.execute("""
      UPDATE servicos
         SET preco_venda = COALESCE(preco_custo,0) * (1 + COALESCE(markup_percentual,0)/100.0),
             valor       = COALESCE(preco_custo,0) * (1 + COALESCE(markup_percentual,0)/100.0);
    """)

    # --- CHECKs de qualidade (idempotente) ---
    op.execute("""
    DO $$
    BEGIN
      IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='ck_serv_preco_custo_nonneg') THEN
        ALTER TABLE servicos ADD CONSTRAINT ck_serv_preco_custo_nonneg CHECK (preco_custo >= 0);
      END IF;

      IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='ck_serv_preco_venda_nonneg') THEN
        ALTER TABLE servicos ADD CONSTRAINT ck_serv_preco_venda_nonneg CHECK (preco_venda >= 0);
      END IF;

      IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='ck_serv_markup_nonneg') THEN
        ALTER TABLE servicos ADD CONSTRAINT ck_serv_markup_nonneg CHECK (markup_percentual >= 0);
      END IF;
    END$$;
    """)


def downgrade():
    # Remove apenas o que adicionamos (sem apagar colunas que já existiam)
    op.execute("""
    DO $$
    BEGIN
      IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname='ck_serv_markup_nonneg') THEN
        ALTER TABLE servicos DROP CONSTRAINT ck_serv_markup_nonneg;
      END IF;
    END$$;
    """)

    op.execute("""
    ALTER TABLE servicos
      DROP COLUMN IF EXISTS markup_percentual;
    """)
