from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
# from flask_migrate import Migrate  # Temporariamente desabilitado
from app.extensoes import db
from app.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# migrate = Migrate(app, db)  # Temporariamente desabilitado

# IMPORTS DOS BLUEPRINTS APÓS CRIAÇÃO DO APP E DB

# Importa blueprints
from app.cliente.cliente_routes import cliente_bp
from app.fornecedor.fornecedor_routes import fornecedor_bp

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
        if username == 'admin' and password == 'admin':
            session['usuario'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('cliente.listar_clientes'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html')


# Rota para página inicial especial
@app.route('/inicio')
@login_required
def inicio():
    return render_template('index.html')

# Rota para dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

@app.route('/')
def home():
    if 'usuario' in session:
        return redirect(url_for('cliente.listar_clientes'))
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
