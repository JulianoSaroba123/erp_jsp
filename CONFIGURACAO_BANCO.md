# 🗂️ Configuração PostgreSQL para ERP JSP

## ✅ Sistema funcionando com SQLite
O sistema está configurado e funcionando com SQLite no arquivo `database/database.db`.

## 🐘 Para usar PostgreSQL (quando necessário)

### 1. Instalar PostgreSQL com encoding UTF-8
```bash
# No Windows, baixe do site oficial e configure:
# - Locale: English (United States)
# - Encoding: UTF8
```

### 2. Configurar banco de dados
```sql
-- Conectar ao PostgreSQL como superuser
CREATE DATABASE jsp_erp WITH ENCODING = 'UTF8';
CREATE USER jsp_user WITH PASSWORD 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON DATABASE jsp_erp TO jsp_user;
```

### 3. Atualizar .env para PostgreSQL
```env
# Descomentar e configurar para PostgreSQL
DATABASE_URL=postgresql://jsp_user:sua_senha_aqui@localhost:5432/jsp_erp
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=sua_chave_super_secreta_para_producao
```

### 4. Instalar driver PostgreSQL
```bash
pip install psycopg2-binary
```

## 🚀 Executar sistema
```bash
# Com SQLite (atual)
python run.pyDATABASE_URL=postgresql+psycopg2://jsp_user:jsp123456@localhost:5432/jsp_erp


# Com PostgreSQL (após configurar)
python run.py
```

## 📝 Notas importantes
- O SQLite é perfeito para desenvolvimento e testes
- PostgreSQL é recomendado para produção
- O sistema detecta automaticamente qual banco usar via DATABASE_URL
