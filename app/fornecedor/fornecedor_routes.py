from flask import Blueprint, render_template, request, redirect, url_for
from app.fornecedor.fornecedor_model import Fornecedor
from extensoes import db

fornecedor_bp = Blueprint(
    'fornecedor',
    __name__,
    url_prefix='/fornecedores',
    template_folder='templates'
)

# Gerador de código automático
def gerar_codigo_fornecedor():
    ultimo = Fornecedor.query.order_by(Fornecedor.id.desc()).first()
    if not ultimo or not ultimo.codigo.startswith("FOR"):
        return "FOR0001"
    numero = int(ultimo.codigo[3:]) + 1
    return f"FOR{numero:04}"

@fornecedor_bp.route('/')
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedor/lista.html', fornecedores=fornecedores)

@fornecedor_bp.route('/cadastrar', methods=['GET', 'POST'])
def novo_fornecedor():
    if request.method == 'POST':
        fornecedor = Fornecedor()
        fornecedor.codigo = gerar_codigo_fornecedor()
        
        # Informações principais
        fornecedor.nome = request.form['nome']
        fornecedor.nome_fantasia = request.form.get('nome_fantasia')
        fornecedor.cpf_cnpj = request.form.get('cpf_cnpj', '')
        
        # Contato
        fornecedor.email = request.form.get('email')
        fornecedor.telefone = request.form.get('telefone')
        
        # Endereço
        fornecedor.cep = request.form.get('cep')
        fornecedor.endereco = request.form.get('endereco')
        fornecedor.numero = request.form.get('numero')
        fornecedor.complemento = request.form.get('complemento')
        fornecedor.bairro = request.form.get('bairro')
        fornecedor.cidade = request.form.get('cidade')
        fornecedor.uf = request.form.get('uf')
        fornecedor.pais = request.form.get('pais', 'Brasil')
        
        # Informações fiscais
        fornecedor.inscricao_estadual = request.form.get('inscricao_estadual')
        fornecedor.inscricao_municipal = request.form.get('inscricao_municipal')
        
        # Informações comerciais
        fornecedor.contato_comercial = request.form.get('contato_comercial')
        fornecedor.telefone_comercial = request.form.get('telefone_comercial')
        fornecedor.email_comercial = request.form.get('email_comercial')
        
        # Observações
        fornecedor.observacoes = request.form.get('observacoes')

        db.session.add(fornecedor)
        db.session.commit()

        return redirect(url_for('fornecedor.listar_fornecedores'))

    return render_template('fornecedor/cadastro.html')

@fornecedor_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)

    if request.method == 'POST':
        # Informações principais
        fornecedor.nome = request.form['nome']
        fornecedor.nome_fantasia = request.form.get('nome_fantasia')
        fornecedor.cpf_cnpj = request.form.get('cpf_cnpj')
        
        # Contato
        fornecedor.email = request.form.get('email')
        fornecedor.telefone = request.form.get('telefone')
        
        # Endereço
        fornecedor.cep = request.form.get('cep')
        fornecedor.endereco = request.form.get('endereco')
        fornecedor.numero = request.form.get('numero')
        fornecedor.complemento = request.form.get('complemento')
        fornecedor.bairro = request.form.get('bairro')
        fornecedor.cidade = request.form.get('cidade')
        fornecedor.uf = request.form.get('uf')
        fornecedor.pais = request.form.get('pais', 'Brasil')
        
        # Informações fiscais
        fornecedor.inscricao_estadual = request.form.get('inscricao_estadual')
        fornecedor.inscricao_municipal = request.form.get('inscricao_municipal')
        
        # Informações comerciais
        fornecedor.contato_comercial = request.form.get('contato_comercial')
        fornecedor.telefone_comercial = request.form.get('telefone_comercial')
        fornecedor.email_comercial = request.form.get('email_comercial')
        
        # Observações
        fornecedor.observacoes = request.form.get('observacoes')
        
        db.session.commit()
        return redirect(url_for('fornecedor.listar_fornecedores'))

    return render_template('fornecedor/cadastro.html', fornecedor=fornecedor)

@fornecedor_bp.route('/excluir/<int:id>')
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    return redirect(url_for('fornecedor.listar_fornecedores'))
