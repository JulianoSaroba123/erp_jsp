import sqlite3

# Caminho do banco SQLite
conn = sqlite3.connect('database.db')  # Nome do arquivo de banco do projeto
cursor = conn.cursor()

# Adicionar coluna nome_fantasia na tabela clientes
try:
    cursor.execute("ALTER TABLE clientes ADD COLUMN nome_fantasia TEXT")
    print("✅ Coluna 'nome_fantasia' adicionada na tabela clientes.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Coluna clientes.nome_fantasia já existe ou erro: {e}")

# Adicionar coluna complemento na tabela clientes
try:
    cursor.execute("ALTER TABLE clientes ADD COLUMN complemento TEXT")
    print("✅ Coluna 'complemento' adicionada na tabela clientes.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Coluna clientes.complemento já existe ou erro: {e}")

# Adicionar coluna nome_fantasia na tabela fornecedores
try:
    cursor.execute("ALTER TABLE fornecedores ADD COLUMN nome_fantasia TEXT")
    print("✅ Coluna 'nome_fantasia' adicionada na tabela fornecedores.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Coluna fornecedores.nome_fantasia já existe ou erro: {e}")

conn.commit()
conn.close()
print("🎯 Atualização do banco de dados concluída!")