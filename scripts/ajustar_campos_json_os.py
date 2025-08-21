# Script para renomear coluna 'parcelas' para 'parcelas_json' e garantir as colunas JSON extras
# Execute este script uma vez para ajustar o banco de dados manualmente (caso não use Alembic)


# Script independente para ajuste do banco (sem depender do app principal)
import sqlalchemy
import os

# Caminho do banco SQLite
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'database.db')
db_uri = f'sqlite:///{os.path.abspath(db_path)}'

engine = sqlalchemy.create_engine(db_uri)

with engine.connect() as conn:
    # Renomear coluna 'parcelas' para 'parcelas_json' (SQLite >= 3.25)
    try:
        conn.execute(sqlalchemy.text("ALTER TABLE ordens_servico RENAME COLUMN parcelas TO parcelas_json;"))
        print("Coluna 'parcelas' renomeada para 'parcelas_json'.")
    except Exception as e:
        print(f"Erro ao renomear coluna (pode ser esperado se já está renomeada): {e}")

    # Adicionar colunas se não existirem
    for cmd in [
        "ALTER TABLE ordens_servico ADD COLUMN servicos_dados TEXT;",
        "ALTER TABLE ordens_servico ADD COLUMN produtos_dados TEXT;",
        "ALTER TABLE ordens_servico ADD COLUMN parcelas_json TEXT;"
    ]:
        try:
            conn.execute(sqlalchemy.text(cmd))
            print(f"Executado: {cmd}")
        except Exception as e:
            print(f"Erro (pode ser esperado se já existe): {e}")

print("Ajuste de banco finalizado. Pode remover este script após uso.")
