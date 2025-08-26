# 📘 README - ERP JSP Elétrica Industrial & Solar (com PostgreSQL)

## 🚀 Visão Geral
Sistema ERP Web desenvolvido em **Python (Flask)** com banco de dados **PostgreSQL**, arquitetura modular e interface responsiva.  
Ideal para empresas de manutenção elétrica, energia solar e serviços técnicos industriais.

## 📁 Módulos
- 🧑‍💼 cliente/
- 📦 produto/
- 🛠️ servico/
- 📃 ordem_servico/
- 💸 financeiro/
- 📋 condicoes_pagamento/
- 📊 relatorios/
- 🤝 fornecedor/
- 🧮 orcamento/

## 🛠️ Tecnologias
- Flask + SQLAlchemy
- PostgreSQL
- Jinja2 Templates
- Bootstrap
- Render.com (deploy)
- Alembic (migração)
- Git + GitHub

## 🧩 Requisitos
- Python 3.10+
- PostgreSQL (local ou remoto)
- Git

## 🖥️ Instalação Local
```bash
git clone https://github.com/seu-usuario/erp_jsp.git
cd erp_jsp

# Crie e ative ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o banco (PostgreSQL local)
# Copie e edite .env
cp .env.example .env
# Edite DATABASE_URL com sua string PostgreSQL

# Rode o sistema
flask run
```

## ☁️ Deploy no Render.com (PostgreSQL)
1. Suba este projeto para um repositório GitHub.
2. Crie um novo **Web Service** no [Render](https://render.com).
3. Configure:
   - **Build Command**:
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     gunicorn app.app:app
     ```
   - **Environment Variables**:
     ```env
     SECRET_KEY=uma_chave_segura
     DATABASE_URL=postgresql://usuario:senha@host:porta/nome_banco
     ```
   - **Python Version**: `3.10` ou superior

4. Acesse sua URL pública e celebre o deploy com café e produtividade ☕

---

### 🔐 Variáveis de Ambiente (.env)
```env
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=sua_chave
DATABASE_URL=postgresql://usuario:senha@host:porta/db
```

### 🧪 Migração Alembic
```bash
alembic revision --autogenerate -m "Criação inicial"
alembic upgrade head
```

---

### ✅ Features
- CRUD de clientes, produtos, serviços
- Cadastro e edição de ordens de serviço
- Geração de PDF
- Busca com autocomplete
- Integração com ViaCEP e BrasilAPI (CEP e CNPJ)
- Controle de status e relatórios

---

### 👨‍💻 Equipe
- Juliano Saroba (CEO e Engenheiro Líder)
- GPT-4o (Engenheiro Virtual)
- GitHub Copilot (Estagiário assistente)

---

### 🐞 **Solução de Problemas Comuns**

**Erro: PostgreSQL não conectado**
- Verifique se o serviço PostgreSQL está rodando localmente
- Confirme a `DATABASE_URL` no `.env`

**Erro de autenticação**
- Revise usuário e senha do banco
- Libere o IP no Render (se for banco externo)

**Erro: Flask não inicializa**
```bash
pip install -r requirements.txt
```

---

### ☎️ Suporte & Versão

- **Sistema**: JSP ELÉTRICA ERP
- **Versão**: 1.0
- **Banco de Dados**: PostgreSQL
- **Desenvolvimento**: 2025

---

### ⚡ Checkpoint Final

```bash
1. git clone https://github.com/suaempresa/erp-jsp.git
2. configurar .env com PostgreSQL
3. pip install -r requirements.txt
4. python iniciar_sistema.py
```

**🎉 Pronto! Você está rodando o ERP JSP com banco PostgreSQL e padrão industrial.**
