# JSP ELÉTRICA - Sistema ERP
## Gestão de Ordens de Serviço

### 🚀 **Inicialização Rápida**

#### **Opção 1: Executáveis (.bat)**
1. **`instalar.bat`** - Primeira execução (configura tudo automaticamente)
2. **`iniciar_sistema.bat`** - Inicialização completa com interface gráfica
3. **`iniciar_servidor.bat`** - Inicialização simples

#### **Opção 2: Python**
```bash
python iniciar_sistema.py
```

### 📋 **Pré-requisitos**
- **Python 3.8+** (Download: https://python.org)
- **Navegador Web** (Chrome, Firefox, Edge)


---

## 🚀 Deploy no Render.com

1. Faça push deste projeto para um repositório no GitHub.
2. Crie um novo serviço Web no Render e conecte ao seu repositório.
3. Configure:
	 - **Build Command:** `pip install -r requirements.txt`
	 - **Start Command:** `gunicorn app.app:app`
	 - **Python Version:** 3.10 ou superior
	 - **(Opcional) Variáveis de ambiente:**
		 - `SECRET_KEY` (chave secreta Flask)
		 - `DATABASE_URL` (caso use banco externo)
4. O Render detecta automaticamente o Procfile.
5. Acesse a URL gerada para usar o sistema online!

---

### 🛠️ **Instalação**

#### **Instalação Automática (Recomendada)**
1. Execute `instalar.bat`
2. Aguarde a conclusão
3. Execute `iniciar_sistema.bat`

#### **Instalação Manual**
```bash
# 1. Criar ambiente virtual
python -m venv .venv

# 2. Ativar ambiente virtual
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar sistema
python iniciar_sistema.py
```

### 🌐 **Acesso ao Sistema**
- **URL Local**: http://localhost:5000
- **Porta**: 5000 (padrão Flask)

### 📁 **Estrutura de Arquivos**

```
📦 JSP ELÉTRICA ERP
├── 🚀 instalar.bat              # Instalação automática
├── 🚀 iniciar_sistema.bat       # Inicializador completo
├── 🚀 iniciar_servidor.bat      # Inicializador simples
├── 🐍 iniciar_sistema.py        # Inicializador Python
├── ⚙️ run.py                   # Aplicação Flask principal
├── 📋 requirements.txt         # Dependências Python
├── 🗂️ app/                     # Código da aplicação
│   ├── 👥 cliente/             # Módulo de clientes
│   ├── 👥 Financeiro/          # Módulo de Financeiro
│   ├── 📋 ordem_servico/       # Módulo de ordens de serviço
│   ├── 💰 financeiro/          # Módulo financeiro
│   ├── 🛠️ servico/             # Módulo de serviços
│   ├── 📦 produto/             # Módulo de produtos
│   └── 🎨 templates/           # Templates HTML
├── 🗄️ database/               # Banco de dados SQLite
└── 📊 static/                 # Arquivos estáticos
```

### 🎯 **Funcionalidades**

#### **Gestão de Clientes**
- ✅ Cadastro de clientes
- ✅ Busca e autocomplete
- ✅ Edição e visualização

#### **Ordens de Serviço**
- ✅ Criação de OS
- ✅ Cálculo automático de valores
- ✅ Geração de PDF profissional
- ✅ Controle de status
- ✅ Upload de arquivos

#### **Módulo Financeiro**
- ✅ Lançamentos automáticos
- ✅ Controle de receitas/despesas
- ✅ Integração com OS

#### **Relatórios**
- ✅ PDF das ordens de serviço
- ✅ Visualização HTML
- ✅ Template profissional JSP

### 🔧 **Configuração**

#### **Variáveis de Ambiente**
```bash
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
```

#### **Banco de Dados**
- **Tipo**: SQLite
- **Localização**: `database/database.db`
- **Migração**: Automática na primeira execução

### 🐛 **Solução de Problemas**

#### **Erro: Python não encontrado**
- Instale Python 3.8+ de https://python.org
- Marque "Add to PATH" durante a instalação

#### **Erro: Módulo não encontrado**
```bash
# Reinstalar dependências
pip install -r requirements.txt
```

#### **Erro: Porta 5000 em uso**
- Feche outras aplicações Flask
- Ou altere a porta em `run.py`

#### **Erro: Ambiente virtual**
```bash
# Recriar ambiente virtual
rmdir /s .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 📞 **Suporte**
- **Sistema**: JSP ELÉTRICA ERP
- **Versão**: 1.0
- **Desenvolvido**: 2025

### 🚀 **Início Rápido - 3 Passos**

1. **Execute**: `instalar.bat`
2. **Execute**: `iniciar_sistema.bat`  
3. **Acesse**: http://localhost:5000

**🎉 Pronto! Seu sistema ERP está funcionando!**
