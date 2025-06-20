from flask import Flask, render_template, request, redirect, send_file, session, url_for
from models import db
from models.cliente_model import Cliente
from models.produto_model import Produto
from models.servico_model import Servico
from models.fornecedor_model import Fornecedor
from models.os_model import OrdemServico
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# -------------------------------
# FUNÇÃO PARA GERAR CÓDIGO AUTOMÁTICO
# -------------------------------
def gerar_codigo(model, prefixo='JSP', inicio=1):
    """
    Gera código sequencial automático com prefixo.
    Exemplo: CLT00001, PRD00001, etc.
    """
    ultimo = model.query.order_by(model.id.desc()).first()
    if ultimo and ultimo.codigo and ultimo.codigo.startswith(prefixo):
        try:
            num = int(ultimo.codigo.replace(prefixo, ''))
        except Exception:
            num = inicio
        novo_num = num + 1
    else:
        novo_num = inicio
    return f"{prefixo}{novo_num:05d}"

# -------------------------------
# CONFIGURAÇÃO DO APP FLASK
# -------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave-secreta-jsp'

db.init_app(app)

with app.app_context():
    db.create_all()

# -------------------------------
# MIDDLEWARE DE PROTEÇÃO DE ROTAS
# -------------------------------
@app.before_request
def proteger_rotas():
    rotas_livres = ['login']
    if 'usuario' not in session and request.endpoint not in rotas_livres:
        return redirect(url_for('login'))

# -------------------------------
# LOGIN / LOGOUT
# -------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'admin' and senha == '123':
            session['usuario'] = usuario
            return redirect('/')
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/login')

# -------------------------------
# CLIENTES
# -------------------------------
@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Código automático para cliente (CLT)
        codigo = gerar_codigo(Cliente, prefixo='CLT', inicio=1)
        cliente = Cliente(
            codigo=codigo,
            nome=request.form['nome'],
            cpf_cnpj=request.form['cpf_cnpj'],
            telefone=request.form['telefone'],
            email=request.form['email'],
            endereco=request.form['endereco'],
            numero=request.form['numero'],
            cep=request.form.get('cep', '')
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect('/')
    else:
        codigo_gerado = gerar_codigo(Cliente, prefixo='CLT', inicio=1)
        return render_template('cadastro_cliente.html', cliente=None, codigo_gerado=codigo_gerado)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.cpf_cnpj = request.form['cpf_cnpj']
        cliente.telefone = request.form['telefone']
        cliente.email = request.form['email']
        cliente.endereco = request.form['endereco']
        cliente.numero = request.form['numero']
        cliente.cep = request.form.get('cep', '')
        db.session.commit()
        return redirect('/')
    return render_template('cadastro_cliente.html', cliente=cliente, codigo_gerado=cliente.codigo)

@app.route('/excluir/<int:id>')
def excluir(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect('/')

# -------------------------------
# PRODUTOS
# -------------------------------
@app.route('/produtos')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('lista_produtos.html', produtos=produtos)

@app.route('/produto/novo', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        codigo = gerar_codigo(Produto, prefixo='PRD', inicio=1)
        produto = Produto(
            codigo=codigo,
            nome=request.form['nome'],
            codigo_barras=request.form.get('codigo_barras', ''),
            data=request.form.get('data', ''),
            fornecedor=request.form.get('fornecedor', ''),
            unidade=request.form.get('unidade', ''),
            classificacao=request.form.get('classificacao', ''),
            localizacao=request.form.get('localizacao', ''),
            situacao=request.form.get('situacao', ''),
            valor_venda=request.form.get('valor_venda', 0),
            valor_compra=request.form.get('valor_compra', 0),
            estoque=request.form.get('estoque', 0),
            lucro=request.form.get('lucro', 0),
            fabricante=request.form.get('fabricante', ''),
            numero_serie=request.form.get('numero_serie', '')
        )
        db.session.add(produto)
        db.session.commit()
        return redirect('/produtos')
    else:
        codigo_gerado = gerar_codigo(Produto, prefixo='PRD', inicio=1)
        return render_template('cadastro_produto.html', produto=None, codigo_gerado=codigo_gerado)

@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.codigo_barras = request.form.get('codigo_barras', '')
        produto.data = request.form.get('data', '')
        produto.fornecedor = request.form.get('fornecedor', '')
        produto.unidade = request.form.get('unidade', '')
        produto.classificacao = request.form.get('classificacao', '')
        produto.localizacao = request.form.get('localizacao', '')
        produto.situacao = request.form.get('situacao', '')
        produto.valor_venda = request.form.get('valor_venda', 0)
        produto.valor_compra = request.form.get('valor_compra', 0)
        produto.estoque = request.form.get('estoque', 0)
        produto.lucro = request.form.get('lucro', 0)
        produto.fabricante = request.form.get('fabricante', '')
        produto.numero_serie = request.form.get('numero_serie', '')
        db.session.commit()
        return redirect('/produtos')
    return render_template('cadastro_produto.html', produto=produto, codigo_gerado=produto.codigo)

@app.route('/produto/excluir/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect('/produtos')

# -------------------------------
# SERVIÇOS
# -------------------------------
@app.route('/servicos')
def listar_servicos():
    servicos = Servico.query.all()
    return render_template('lista_servicos.html', servicos=servicos)

@app.route('/servico/novo', methods=['GET', 'POST'])
def cadastrar_servico():
    if request.method == 'POST':
        codigo = gerar_codigo(Servico, prefixo='SRV', inicio=1)
        servico = Servico(
            codigo=codigo,
            nome=request.form['nome'],
            valor=request.form.get('valor', 0),
            unidade=request.form.get('unidade', ''),
            situacao=request.form.get('situacao', 'Ativo')
        )
        db.session.add(servico)
        db.session.commit()
        return redirect('/servicos')
    else:
        codigo_gerado = gerar_codigo(Servico, prefixo='SRV', inicio=1)
        return render_template('cadastro_servico.html', servico=None, codigo_gerado=codigo_gerado)

@app.route('/servico/editar/<int:id>', methods=['GET', 'POST'])
def editar_servico(id):
    servico = Servico.query.get_or_404(id)
    if request.method == 'POST':
        servico.nome = request.form['nome']
        servico.valor = request.form.get('valor', 0)
        servico.unidade = request.form.get('unidade', '')
        servico.situacao = request.form.get('situacao', 'Ativo')
        db.session.commit()
        return redirect('/servicos')
    return render_template('cadastro_servico.html', servico=servico, codigo_gerado=servico.codigo)

@app.route('/servico/excluir/<int:id>')
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    db.session.delete(servico)
    db.session.commit()
    return redirect('/servicos')

# -------------------------------
# FORNECEDORES
# -------------------------------
@app.route('/fornecedores')
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('lista_fornecedores.html', fornecedores=fornecedores)

@app.route('/fornecedor/novo', methods=['GET', 'POST'])
def cadastrar_fornecedor():
    if request.method == 'POST':
        codigo = gerar_codigo(Fornecedor, prefixo='FRN', inicio=1)
        fornecedor = Fornecedor(
            codigo=codigo,
            nome=request.form['nome'],
            cnpj=request.form['cnpj'],
            telefone=request.form['telefone'],
            cep=request.form['cep'],
            cidade=request.form['cidade'],
            endereco=request.form['endereco']
        )
        db.session.add(fornecedor)
        db.session.commit()
        return redirect('/fornecedores')
    else:
        codigo_gerado = gerar_codigo(Fornecedor, prefixo='FRN', inicio=1)
        return render_template('cadastro_fornecedor.html', fornecedor=None, codigo_gerado=codigo_gerado)

@app.route('/fornecedor/editar/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    if request.method == 'POST':
        fornecedor.nome = request.form['nome']
        fornecedor.cnpj = request.form['cnpj']
        fornecedor.telefone = request.form['telefone']
        fornecedor.cep = request.form['cep']
        fornecedor.cidade = request.form['cidade']
        fornecedor.endereco = request.form['endereco']
        db.session.commit()
        return redirect('/fornecedores')
    return render_template('cadastro_fornecedor.html', fornecedor=fornecedor, codigo_gerado=fornecedor.codigo)

@app.route('/fornecedor/excluir/<int:id>')
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    return redirect('/fornecedores')

# -------------------------------
# ORDEM DE SERVIÇO (simples)
# -------------------------------
@app.route('/ordens_servico')
def lista_ordens_servico():
    ordens = OrdemServico.query.all()
    return render_template('lista_ordens_servico.html', ordens=ordens)

@app.route('/ordem_servico/novo', methods=['GET', 'POST'])
def cadastrar_ordem_servico():
    if request.method == 'POST':
        codigo = gerar_codigo(OrdemServico, prefixo='OS', inicio=1)
        os = OrdemServico(
            codigo=codigo,
            # Adicione aqui os campos necessários!
            cliente_id=request.form.get('cliente_id'),
            descricao=request.form.get('descricao', ''),
            # ... outros campos da OS ...
        )
        db.session.add(os)
        db.session.commit()
        return redirect('/ordens_servico')
    else:
        codigo_gerado = gerar_codigo(OrdemServico, prefixo='OS', inicio=1)
        return render_template('cadastro_ordem_servico.html', os=None, codigo_gerado=codigo_gerado)

@app.route('/ordem_servico/editar/<int:id>', methods=['GET', 'POST'])
def editar_ordem_servico(id):
    os = OrdemServico.query.get_or_404(id)
    if request.method == 'POST':
        # Atualize os campos da OS conforme seu model!
        os.descricao = request.form.get('descricao', '')
        # ... outros campos ...
        db.session.commit()
        return redirect('/ordens_servico')
    return render_template('cadastro_ordem_servico.html', os=os, codigo_gerado=os.codigo)

@app.route('/ordem_servico/excluir/<int:id>')
def excluir_ordem_servico(id):
    os = OrdemServico.query.get_or_404(id)
    db.session.delete(os)
    db.session.commit()
    return redirect('/ordens_servico')

# -------------------------------
# INÍCIO DO APP
# -------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
