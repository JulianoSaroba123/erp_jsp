# Script para adicionar campos JSON ao modelo OrdemServico
# Execute este script uma vez para atualizar o banco de dados manualmente (caso não use Alembic)

from app.ordem_servico.os_model import OrdemServico
from extensoes import db
from sqlalchemy import text

# Adiciona as colunas se não existirem
alter_commands = [
    "ALTER TABLE ordens_servico ADD COLUMN servicos_dados TEXT;",
    "ALTER TABLE ordens_servico ADD COLUMN produtos_dados TEXT;",
    "ALTER TABLE ordens_servico ADD COLUMN parcelas TEXT;"
]

with db.engine.connect() as conn:
    for cmd in alter_commands:
        try:
            conn.execute(text(cmd))
            print(f"Executado: {cmd}")
        except Exception as e:
            print(f"Erro (pode ser esperado se já existe): {e}")

print("Campos adicionados (ou já existiam). Pode remover este script após uso.")
