# Endpoint de debug: listar todos os clientes em JSON (ativos e inativos)

# Endpoint de debug: listar todos os clientes em JSON (ativos e inativos)

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.cliente.cliente_model import Cliente  
from extensoes import db

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes', template_folder='templates')

# API para busca de clientes (autocomplete)
@cliente_bp.route('/api/busca', methods=['GET'])
def api_busca_clientes():
    termo = request.args.get('q', '').strip()
    
    if not termo:
        # Se não há termo, retornar todos os clientes ativos (para recarregamento)
        query = Cliente.query.filter(Cliente.ativo == True).order_by(Cliente.nome).limit(50)
    else:
        # Se há termo, buscar por nome ou CPF/CNPJ
        query = Cliente.query.filter(
            ((Cliente.nome.ilike(f'%{termo}%')) |
             (Cliente.cpf_cnpj.ilike(f'%{termo}%')))
            & (Cliente.ativo == True)
        ).order_by(Cliente.nome).limit(15)
    resultados = [
        {
            'id': c.id,
            'nome': c.nome,
            'cpf_cnpj': c.cpf_cnpj,
            'telefone': c.telefone,
            'email': c.email,
            'endereco': c.endereco
        }
        for c in query
    ]
    return jsonify(resultados)

def gerar_codigo_cliente():
    ultimo = Cliente.query.order_by(Cliente.id.desc()).first()
    if not ultimo or not ultimo.codigo.startswith("CLI"):
        return "CLI0001"
    numero = int(ultimo.codigo[3:]) + 1
    return f"CLI{numero:04}"

@cliente_bp.route('/')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('cliente/lista.html', clientes=clientes)

@cliente_bp.route('/cadastrar', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':
        cliente = Cliente()
        cliente.codigo = gerar_codigo_cliente()
        
        # Informações principais
        cliente.nome = request.form['nome']
        cliente.nome_fantasia = request.form.get('nome_fantasia')
        cliente.cpf_cnpj = request.form.get('cpf_cnpj', '')
        
        # Contato
        cliente.email = request.form.get('email')
        cliente.telefone = request.form.get('telefone')
        
        # Endereço
        cliente.cep = request.form.get('cep')
        cliente.endereco = request.form.get('endereco')
        cliente.numero = request.form.get('numero')
        cliente.complemento = request.form.get('complemento')
        cliente.bairro = request.form.get('bairro')
        cliente.cidade = request.form.get('cidade')
        cliente.uf = request.form.get('uf')  # Mudança: estado -> uf
        cliente.pais = request.form.get('pais', 'Brasil')
        
        # Informações fiscais
        cliente.inscricao_estadual = request.form.get('inscricao_estadual')
        cliente.inscricao_municipal = request.form.get('inscricao_municipal')
        
        # Observações
        cliente.observacoes = request.form.get('observacoes')
        # Sempre marcar como ativo ao cadastrar
        cliente.ativo = True
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('cliente.listar_clientes'))
    
    codigo_gerado = gerar_codigo_cliente()
    return render_template('cliente/cadastro.html', codigo_gerado=codigo_gerado)

@cliente_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        # Informações principais
        cliente.nome = request.form['nome']
        cliente.nome_fantasia = request.form.get('nome_fantasia')
        cliente.cpf_cnpj = request.form.get('cpf_cnpj')
        
        # Contato
        cliente.email = request.form.get('email')
        cliente.telefone = request.form.get('telefone')
        
        # Endereço
        cliente.cep = request.form.get('cep')
        cliente.endereco = request.form.get('endereco')
        cliente.numero = request.form.get('numero')
        cliente.complemento = request.form.get('complemento')
        cliente.bairro = request.form.get('bairro')
        cliente.cidade = request.form.get('cidade')
        cliente.uf = request.form.get('uf')  # Mudança: estado -> uf
        cliente.pais = request.form.get('pais', 'Brasil')
        
        # Informações fiscais
        cliente.inscricao_estadual = request.form.get('inscricao_estadual')
        cliente.inscricao_municipal = request.form.get('inscricao_municipal')
        
        # Observações
        cliente.observacoes = request.form.get('observacoes')
        
        db.session.commit()
        return redirect(url_for('cliente.listar_clientes'))
    
    return render_template('cliente/cadastro.html', cliente=cliente, codigo_gerado=cliente.codigo)

@cliente_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('cliente.listar_clientes'))

# Rota temporária para reativar todos os clientes via GET (para facilitar)
@cliente_bp.route('/reativar_todos', methods=['GET'])
def reativar_todos_clientes():
    Cliente.query.update({Cliente.ativo: True})
    db.session.commit()
    return 'Todos os clientes foram ativados! <a href="/clientes/">Voltar para lista de clientes</a>'
