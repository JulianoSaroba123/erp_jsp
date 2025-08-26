# Endpoint de debug: listar todos os clientes em JSON (ativos e inativos)


from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .cliente_model import Cliente
from app.extensoes import db
from sqlalchemy import or_

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes', template_folder='templates')

def gerar_codigo_cliente():
    ultimo = Cliente.query.order_by(Cliente.id.desc()).first()
    if not ultimo or not ultimo.codigo.startswith("CLI"):
        return "CLI0001"
    numero = int(ultimo.codigo[3:]) + 1
    return f"CLI{numero:04}"

# Listagem com busca e paginação
@cliente_bp.route('/')
def listar_clientes():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '', type=str)
    query = Cliente.query
    if search:
        query = query.filter(or_(Cliente.nome.ilike(f'%{search}%'), Cliente.cpf_cnpj.ilike(f'%{search}%')))
    clientes = query.order_by(Cliente.nome).paginate(page=page, per_page=10)
    return render_template('cliente/lista.html', clientes=clientes, search=search)

# Cadastro
@cliente_bp.route('/cadastrar', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':
        try:
            cliente = Cliente()
            cliente.codigo = gerar_codigo_cliente()
            cliente.nome = request.form['nome']
            cliente.nome_fantasia = request.form.get('nome_fantasia')
            cliente.cpf_cnpj = request.form.get('cpf_cnpj', '')
            cliente.email = request.form.get('email')
            cliente.telefone = request.form.get('telefone')
            cliente.cep = request.form.get('cep')
            cliente.endereco = request.form.get('endereco')
            cliente.numero = request.form.get('numero')
            cliente.complemento = request.form.get('complemento')
            cliente.bairro = request.form.get('bairro')
            cliente.cidade = request.form.get('cidade')
            cliente.uf = request.form.get('uf')
            cliente.pais = request.form.get('pais', 'Brasil')
            cliente.inscricao_estadual = request.form.get('inscricao_estadual')
            cliente.inscricao_municipal = request.form.get('inscricao_municipal')
            cliente.observacoes = request.form.get('observacoes')
            cliente.ativo = True
            db.session.add(cliente)
            db.session.commit()
            flash('Cliente cadastrado com sucesso!', 'success')
            return redirect(url_for('cliente.listar_clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar cliente: {e}', 'danger')
    codigo_gerado = gerar_codigo_cliente()
    return render_template('cliente/cadastro.html', codigo_gerado=codigo_gerado, cliente=None)

# Edição
@cliente_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        try:
            cliente.nome = request.form['nome']
            cliente.nome_fantasia = request.form.get('nome_fantasia')
            cliente.cpf_cnpj = request.form.get('cpf_cnpj')
            cliente.email = request.form.get('email')
            cliente.telefone = request.form.get('telefone')
            cliente.cep = request.form.get('cep')
            cliente.endereco = request.form.get('endereco')
            cliente.numero = request.form.get('numero')
            cliente.complemento = request.form.get('complemento')
            cliente.bairro = request.form.get('bairro')
            cliente.cidade = request.form.get('cidade')
            cliente.uf = request.form.get('uf')
            cliente.pais = request.form.get('pais', 'Brasil')
            cliente.inscricao_estadual = request.form.get('inscricao_estadual')
            cliente.inscricao_municipal = request.form.get('inscricao_municipal')
            cliente.observacoes = request.form.get('observacoes')
            db.session.commit()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('cliente.listar_clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar cliente: {e}', 'danger')
    return render_template('cliente/cadastro.html', cliente=cliente, codigo_gerado=cliente.codigo)

# Exclusão
@cliente_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir cliente: {e}', 'danger')
    return redirect(url_for('cliente.listar_clientes'))

# API para busca/autocomplete
@cliente_bp.route('/api/busca', methods=['GET'])
def api_busca_clientes():
    termo = request.args.get('q', '').strip()
    query = Cliente.query
    if termo:
        query = query.filter(or_(Cliente.nome.ilike(f'%{termo}%'), Cliente.cpf_cnpj.ilike(f'%{termo}%')))
    clientes = query.filter(Cliente.ativo == True).order_by(Cliente.nome).limit(20).all()
    resultados = [
        {
            'id': c.id,
            'nome': c.nome,
            'cpf_cnpj': c.cpf_cnpj,
            'telefone': c.telefone,
            'email': c.email,
            'endereco': c.endereco
        }
        for c in clientes
    ]
    return jsonify(resultados)

# API RESTful básica (GET, POST, PUT, DELETE)
@cliente_bp.route('/api/', methods=['GET'])
def api_listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([
        {
            'id': c.id,
            'codigo': c.codigo,
            'nome': c.nome,
            'cpf_cnpj': c.cpf_cnpj,
            'email': c.email,
            'telefone': c.telefone
        } for c in clientes
    ])

@cliente_bp.route('/api/<int:id>', methods=['GET'])
def api_detalhar_cliente(id):
    c = Cliente.query.get_or_404(id)
    return jsonify({
        'id': c.id,
        'codigo': c.codigo,
        'nome': c.nome,
        'cpf_cnpj': c.cpf_cnpj,
        'email': c.email,
        'telefone': c.telefone
    })

@cliente_bp.route('/api/', methods=['POST'])
def api_criar_cliente():
    data = request.json
    cliente = Cliente(
        codigo=gerar_codigo_cliente(),
        nome=data.get('nome'),
        cpf_cnpj=data.get('cpf_cnpj'),
        email=data.get('email'),
        telefone=data.get('telefone'),
        ativo=True
    )
    db.session.add(cliente)
    db.session.commit()
    return jsonify({'id': cliente.id}), 201

@cliente_bp.route('/api/<int:id>', methods=['PUT'])
def api_editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.json
    cliente.nome = data.get('nome', cliente.nome)
    cliente.cpf_cnpj = data.get('cpf_cnpj', cliente.cpf_cnpj)
    cliente.email = data.get('email', cliente.email)
    cliente.telefone = data.get('telefone', cliente.telefone)
    db.session.commit()
    return jsonify({'msg': 'Cliente atualizado'})

@cliente_bp.route('/api/<int:id>', methods=['DELETE'])
def api_excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'msg': 'Cliente excluído'})
