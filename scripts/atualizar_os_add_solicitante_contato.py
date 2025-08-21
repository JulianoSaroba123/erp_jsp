import sqlite3

DB_PATH = 'database/database.db'

sqls = [
    "ALTER TABLE ordens_servico ADD COLUMN solicitante VARCHAR(100);",
    "ALTER TABLE ordens_servico ADD COLUMN contato VARCHAR(100);"
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

for sql in sqls:
    try:
        c.execute(sql)
        print(f'Executado: {sql}')
    except Exception as e:
        print(f'Erro ou já existe: {sql} -> {e}')

conn.commit()
conn.close()
print('Migration concluída!')
