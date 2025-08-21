from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from flask_migrate import Migrate
from extensoes import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

from app.cliente.cliente_routes import cliente_bp
from app.fornecedor.fornecedor_routes import fornecedor_bp
from app.produto.produto_routes import produto_bp
from app.servico.servico_routes import servico_bp
from app.ordem_servico.os_routes import os_bp
from app.test_routes import test_bp
from app.relatorios.relatorio_routes import relatorio_bp
from app.financeiro.financeiro_routes import financeiro_bp
from app.orcamento.orcamento_routes import orcamento_bp
from dotenv import load_dotenv
load_dotenv()




app = Flask(__name__)
migrate = Migrate(app, db)

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

# Configurações do banco
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = 'sua_chave_super_secreta'

# Inicializa o banco
db.init_app(app)


# Registra Blueprints
app.register_blueprint(cliente_bp)
app.register_blueprint(fornecedor_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(servico_bp)
app.register_blueprint(os_bp)
app.register_blueprint(test_bp)
app.register_blueprint(relatorio_bp)
app.register_blueprint(financeiro_bp)
app.register_blueprint(orcamento_bp)

# Importar modelos (após inicialização do app)
from app.cliente.cliente_model import Cliente
from app.fornecedor.fornecedor_model import Fornecedor
from app.produto.produto_model import Produto
from app.servico.servico_model import Servico
from app.ordem_servico.os_model import OrdemServico, OrdemServicoItem

# Criar tabelas do banco de dados
with app.app_context():
    db.create_all()


# Rota raiz - Dashboard

from app.financeiro.financeiro_model import LancamentoFinanceiro
from sqlalchemy import func

@app.route('/')
@login_required
def index():
    # Totais do financeiro
    entradas_total = db.session.query(func.sum(LancamentoFinanceiro.valor)).filter(LancamentoFinanceiro.tipo == 'Receita').scalar() or 0
    saidas_total = db.session.query(func.sum(LancamentoFinanceiro.valor)).filter(LancamentoFinanceiro.tipo == 'Despesa').scalar() or 0
    saldo_total = entradas_total - saidas_total


    # Entradas e saídas por mês (12 meses)
    from sqlalchemy import extract
    meses = list(range(1, 13))
    grafico_entradas = [
        db.session.query(func.sum(LancamentoFinanceiro.valor)).filter(
            LancamentoFinanceiro.tipo == 'Receita',
            extract('month', LancamentoFinanceiro.data) == m
        ).scalar() or 0 for m in meses
    ]
    grafico_saidas = [
        db.session.query(func.sum(LancamentoFinanceiro.valor)).filter(
            LancamentoFinanceiro.tipo == 'Despesa',
            extract('month', LancamentoFinanceiro.data) == m
        ).scalar() or 0 for m in meses
    ]
    # Saldo acumulado mês a mês
    saldo_acumulado = []
    saldo = 0
    for i in range(12):
        saldo += grafico_entradas[i] - grafico_saidas[i]
        saldo_acumulado.append(saldo)

    # Despesas por categoria (top 5)
    cat_query = db.session.query(
        LancamentoFinanceiro.categoria,
        func.sum(LancamentoFinanceiro.valor)
    ).filter(LancamentoFinanceiro.tipo == 'Despesa').group_by(LancamentoFinanceiro.categoria).order_by(func.sum(LancamentoFinanceiro.valor).desc()).limit(5).all()
    categorias = [c[0] for c in cat_query]
    valores_cat = [float(c[1]) for c in cat_query]

    return render_template(
        'index.html',
        saldo_total=f'{saldo_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        entradas_total=f'{entradas_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        saidas_total=f'{saidas_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        grafico_saldo=saldo_acumulado,
        grafico_entradas=grafico_entradas,
        grafico_saidas=grafico_saidas,
        categorias=categorias,
        valores_cat=valores_cat
    )


# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Usuário e senha fixos para exemplo
        if username == 'admin' and password == 'admin':
            session['usuario'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html')


# Rota para página inicial especial
@app.route('/inicio')
@login_required
def inicio():
    return render_template('index.html')


import os
print("SQLALCHEMY_DATABASE_URI =", app.config["SQLALCHEMY_DATABASE_URI"])
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///"):
    rel = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "", 1)
    print("DB ABS PATH =", os.path.abspath(rel))

if __name__ == '__main__':
    app.run(debug=True)
