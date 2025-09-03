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
    q = request.args.get('q', '').strip()
    page = request.args.get('pagina', type=int, default=1)
    per_page = 20
    
    query = Cliente.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(Cliente.nome.ilike(like),
                Cliente.email.ilike(like),
                Cliente.cpf_cnpj.ilike(like))
        )
    
    pag = query.order_by(Cliente.nome.asc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'cliente/lista.html',
        clientes=pag.items,   # só a lista!
        paginacao=pag,        # o objeto de paginação
        q=q
    )

# Cadastro
@cliente_bp.route('/cadastrar', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':
        try:
            cliente = Cliente()
            cliente.codigo = gerar_codigo_cliente()
            cliente.nome = request.form['nome']
            cpf_cnpj = request.form.get('cpf_cnpj', '')
            # Remove qualquer formatação (pontos, traços, barras)
            cpf_cnpj = ''.join(filter(str.isdigit, cpf_cnpj))
            cliente.cpf_cnpj = cpf_cnpj
            cliente.email = request.form.get('email')
            cliente.telefone = request.form.get('telefone')
            
            # Salvar campos de endereço separados (com try/except para compatibilidade)
            try:
                cliente.cep = request.form.get('cep', '')
                cliente.logradouro = request.form.get('logradouro', '')
                cliente.numero = request.form.get('numero', '')
                cliente.complemento = request.form.get('complemento', '')
                cliente.bairro = request.form.get('bairro', '')
                cliente.cidade = request.form.get('cidade', '')
                cliente.uf = request.form.get('uf', '')
            except AttributeError:
                # Se as colunas não existem, ignore
                pass
            
            # Construir endereço completo para compatibilidade
            endereco_partes = []
            logradouro = request.form.get('logradouro', '')
            numero = request.form.get('numero', '')
            complemento = request.form.get('complemento', '')
            bairro = request.form.get('bairro', '')
            cidade = request.form.get('cidade', '')
            uf = request.form.get('uf', '')
            cep = request.form.get('cep', '')
            
            if logradouro:
                endereco_partes.append(logradouro)
            if numero:
                endereco_partes.append(f"nº {numero}")
            if complemento:
                endereco_partes.append(complemento)
            if bairro:
                endereco_partes.append(f"Bairro: {bairro}")
            if cidade:
                endereco_partes.append(cidade)
            if uf:
                endereco_partes.append(uf)
            if cep:
                endereco_partes.append(f"CEP: {cep}")
            
            cliente.endereco = ', '.join(endereco_partes) if endereco_partes else ''
            cliente.pais = request.form.get('pais', 'Brasil')  # Corrigido: país padrão Brasil
            cliente.ativo = True  # Corrigido: sempre ativo por padrão

            db.session.add(cliente)
            db.session.commit()
            flash('Cliente cadastrado com sucesso!', 'success')
            return redirect(url_for('cliente.listar_clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar cliente: {e}', 'danger')
    
    return render_template('cliente/cadastro.html')

# Edição
@cliente_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            cliente.nome = request.form['nome']
            cpf_cnpj = request.form.get('cpf_cnpj', '')
            cpf_cnpj = ''.join(filter(str.isdigit, cpf_cnpj))
            cliente.cpf_cnpj = cpf_cnpj
            cliente.email = request.form.get('email')
            cliente.telefone = request.form.get('telefone')
            
            # Salvar campos de endereço separados (com try/except para compatibilidade)
            try:
                cliente.cep = request.form.get('cep', '')
                cliente.logradouro = request.form.get('logradouro', '')
                cliente.numero = request.form.get('numero', '')
                cliente.complemento = request.form.get('complemento', '')
                cliente.bairro = request.form.get('bairro', '')
                cliente.cidade = request.form.get('cidade', '')
                cliente.uf = request.form.get('uf', '')
            except AttributeError:
                # Se as colunas não existem, ignore
                pass
            
            # Construir endereço completo para compatibilidade
            endereco_partes = []
            logradouro = request.form.get('logradouro', '')
            numero = request.form.get('numero', '')
            complemento = request.form.get('complemento', '')
            bairro = request.form.get('bairro', '')
            cidade = request.form.get('cidade', '')
            uf = request.form.get('uf', '')
            cep = request.form.get('cep', '')
            
            if logradouro:
                endereco_partes.append(logradouro)
            if numero:
                endereco_partes.append(f"nº {numero}")
            if complemento:
                endereco_partes.append(complemento)
            if bairro:
                endereco_partes.append(f"Bairro: {bairro}")
            if cidade:
                endereco_partes.append(cidade)
            if uf:
                endereco_partes.append(uf)
            if cep:
                endereco_partes.append(f"CEP: {cep}")
            
            cliente.endereco = ', '.join(endereco_partes) if endereco_partes else ''
            cliente.pais = request.form.get('pais', cliente.pais or 'Brasil')  # Corrigido: mantém país existente ou Brasil
            # Manter ativo como está (não alterar no edit)
            
            # Garante que o campo codigo exista
            if not hasattr(cliente, 'codigo') or not cliente.codigo:
                cliente.codigo = gerar_codigo_cliente()
            
            db.session.commit()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('cliente.listar_clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar cliente: {e}', 'danger')
    
    # Garante que o campo codigo exista ao renderizar o template
    if not hasattr(cliente, 'codigo') or not cliente.codigo:
        cliente.codigo = gerar_codigo_cliente()
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

# Detalhamento
@cliente_bp.route('/detalhar/<int:id>')
def detalhar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('cliente/detalhar.html', cliente=cliente)

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
            'codigo': c.codigo,
            'nome': c.nome,
            'cpf_cnpj': c.cpf_cnpj or '',
            'telefone': c.telefone or '',
            'email': c.email or '',
            'endereco': c.endereco or ''
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
