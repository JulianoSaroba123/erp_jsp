import sqlite3
import os

def test_db_structure():
    db_path = os.getenv('DATABASE_URL', 'database/database.db').replace('sqlite:///', '')
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # 1. Não deve haver tabelas temporárias
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '_alembic_tmp_%'")
    assert not cur.fetchall(), "Existem tabelas temporárias do Alembic!"

    # 2. Tabela clientes deve existir
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clientes'")
    assert cur.fetchone(), "Tabela clientes não existe!"

    # 3. Verificar se a coluna cpf_cnpj tem uma constraint única
    cur.execute("PRAGMA index_list(clientes)")
    indexes = cur.fetchall()
    found = False

    for idx in indexes:
        index_name = idx[1]
        is_unique = idx[2]  # 1 = UNIQUE
        cur.execute(f"PRAGMA index_info('{index_name}')")
        columns = [col[2] for col in cur.fetchall()]
        if 'cpf_cnpj' in columns and is_unique:
            found = True
            break

    assert found, "Constraint única na coluna 'cpf_cnpj' não existe!"

    con.close()
    print("Banco validado com sucesso!")

if __name__ == '__main__':
    test_db_structure()
