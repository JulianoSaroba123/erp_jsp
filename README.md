# 🏢 JSP ERP System

Sistema ERP completo desenvolvido em Flask para gestão empresarial.

## 📋 Funcionalidades

- 👥 **Gestão de Clientes** - Cadastro e controle de clientes
- 🛠️ **Ordens de Serviço** - Criação e acompanhamento de OS
- 📦 **Gestão de Produtos** - Controle de estoque e produtos
- 🔧 **Gestão de Serviços** - Cadastro e precificação de serviços
- 🏭 **Gestão de Fornecedores** - Controle de fornecedores
- 💰 **Módulo Financeiro** - Controle financeiro integrado
- 📊 **Relatórios** - Geração de relatórios em PDF
- 🔢 **Orçamentos** - Sistema de orçamentação

## 🚀 Tecnologias

- **Backend**: Python 3.13 + Flask
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrações**: Alembic
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **PDF**: WeasyPrint
- **Deploy**: Heroku Ready

## ⚙️ Instalação

### Pré-requisitos
- Python 3.13+
- PostgreSQL
- Git

### Configuração Local

1. **Clone o repositório**
```bash
git clone https://github.com/SEU_USUARIO/erp_jsp.git
cd erp_jsp
```

2. **Crie ambiente virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**
Crie arquivo `.env`:
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/jsp_erp
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
```

5. **Configure banco de dados**
```bash
# Criar banco PostgreSQL
createdb jsp_erp

# Executar migrações
alembic upgrade head
```

6. **Execute a aplicação**
```bash
python run.py
```

Acesse: `http://localhost:5000`

## 🗃️ Estrutura do Projeto

```
erp_jsp/
├── app/
│   ├── cliente/          # Módulo de clientes
│   ├── fornecedor/       # Módulo de fornecedores
│   ├── produto/          # Módulo de produtos
│   ├── servico/          # Módulo de serviços
│   ├── ordem_servico/    # Módulo de ordens de serviço
│   ├── orcamento/        # Módulo de orçamentos
│   ├── financeiro/       # Módulo financeiro
│   ├── static/           # Arquivos estáticos
│   └── templates/        # Templates HTML
├── migrations/           # Migrações do banco
├── requirements.txt      # Dependências Python
├── run.py               # Arquivo principal
├── alembic.ini          # Configuração Alembic
└── Procfile             # Deploy Heroku
```

## 🚀 Deploy

### Heroku
O projeto está configurado para deploy no Heroku:

1. **Crie app no Heroku**
```bash
heroku create seu-app-erp
```

2. **Configure addon PostgreSQL**
```bash
heroku addons:create heroku-postgresql:mini
```

3. **Configure variáveis**
```bash
heroku config:set SECRET_KEY=sua_chave_secreta
```

4. **Deploy**
```bash
git push heroku main
```

5. **Execute migrações**
```bash
heroku run alembic upgrade head
```

## 📊 Funcionalidades Principais

### Ordens de Serviço
- Numeração automática a partir de OS0350
- Cálculo automático de valores
- Integração com módulo financeiro
- Geração de relatórios PDF
- Controle de status

### Gestão Financeira
- Lançamentos automáticos de OS pagas
- Controle de recebimentos
- Relatórios financeiros

### Relatórios
- Relatórios de OS em PDF
- Formatação profissional
- Dados completos de serviços e produtos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas, abra uma issue no GitHub.

---

**Desenvolvido com ❤️ para gestão empresarial eficiente**
