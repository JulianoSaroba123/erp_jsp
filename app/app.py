from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
# from flask_migrate import Migrate  # Temporariamente desabilitado
from app.extensoes import db
from app.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY, TEMPLATES_AUTO_RELOAD, SEND_FILE_MAX_AGE_DEFAULT

from dotenv import load_dotenv
load_dotenv()

from flask import Flask
import os

BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(BASE_DIR)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(ROOT_DIR, "static"),
    static_url_path="/static"
)

# migrate = Migrate(app, db)  # Temporariamente desabilitado

# IMPORTS DOS BLUEPRINTS APÓS CRIAÇÃO DO APP E DB

# Importa blueprints


from app.cliente.cliente_routes import cliente_bp
from app.fornecedor.fornecedor_routes import fornecedor_bp
from app.produto.produto_routes import produto_bp
from app.servico.servico_routes import servico_bp
from app.orcamento.orcamento_routes import orcamento_bp
from app.configuracoes.condicoes_pagamento.condicoes_pagamento_routes import condicoes_pagamento_bp
from app.ordem_servico.os_routes import os_bp
from app.financeiro.financeiro_routes import financeiro_bp

# Decorator para exigir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

# Rota de Logout
@app.route('/logout')
@login_required
def logout():
    session.pop('usuario', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = TEMPLATES_AUTO_RELOAD
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = SEND_FILE_MAX_AGE_DEFAULT

# Força recarregamento de templates em desenvolvimento
if os.environ.get('DEBUG', 'True').lower() == 'true':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

# Inicializa o banco
db.init_app(app)


# Registra Blueprints



app.register_blueprint(cliente_bp)
app.register_blueprint(fornecedor_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(servico_bp)
app.register_blueprint(orcamento_bp)
app.register_blueprint(condicoes_pagamento_bp)
app.register_blueprint(os_bp)
app.register_blueprint(financeiro_bp)

# Criar tabelas do banco de dados
with app.app_context():
    db.create_all()
    
    # Executar migrações automáticas
    try:
        from app.migracoes_db import executar_migracoes
        executar_migracoes()
    except Exception as e:
        print(f"Erro ao executar migrações: {e}")


# Rota raiz - Dashboard




# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'Juliano' and password == 'admin':
            session['usuario'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html')


# Rota para página inicial especial
@app.route('/inicio')
def inicio():
    # Dados simulados para o dashboard
    dados_dashboard = {
        'saldo_total': '125.430,00',
        'entradas_total': '180.250,00', 
        'saidas_total': '54.820,00',
        'grafico_entradas': [15000, 18000, 22000, 16000, 25000, 19000, 21000, 23000, 17000, 20000, 24000, 18000],
        'grafico_saidas': [8000, 9500, 11000, 7500, 12000, 8800, 9200, 10500, 7800, 9000, 11500, 8200],
        'categorias': ['Material Elétrico', 'Mão de Obra', 'Transporte', 'Ferramentas', 'Outros'],
        'valores_cat': [25000, 15000, 8000, 4000, 2820]
    }
    
    return render_template('index.html', **dados_dashboard)

# Rota para dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

@app.route('/')
def home():
    if 'usuario' in session:
        # Dados simulados para o dashboard
        dados_dashboard = {
            'saldo_total': '125.430,00',
            'entradas_total': '180.250,00', 
            'saidas_total': '54.820,00',
            'grafico_entradas': [15000, 18000, 22000, 16000, 25000, 19000, 21000, 23000, 17000, 20000, 24000, 18000],
            'grafico_saidas': [8000, 9500, 11000, 7500, 12000, 8800, 9200, 10500, 7800, 9000, 11500, 8200],
            'categorias': ['Material Elétrico', 'Mão de Obra', 'Transporte', 'Ferramentas', 'Outros'],
            'valores_cat': [25000, 15000, 8000, 4000, 2820]
        }
        return render_template('index.html', **dados_dashboard)
    return redirect(url_for('login'))

# Rota específica para /cliente/novo
@app.route('/cliente/novo')
@login_required  
def cliente_novo():
    return redirect(url_for('cliente.novo_cliente'))


import os
print("SQLALCHEMY_DATABASE_URI =", app.config["SQLALCHEMY_DATABASE_URI"])
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///"):
    rel = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "", 1)
    print("DB ABS PATH =", os.path.abspath(rel))

# Inicializar banco de dados automaticamente
with app.app_context():
    try:
        db.create_all()
        print("Tabelas do banco de dados criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")

if __name__ == '__main__':
    app.run(debug=True)
