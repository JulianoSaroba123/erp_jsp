from flask import Blueprint, render_template, request, redirect, url_for
from .fornecedor_model import Fornecedor
from app.extensoes import db

fornecedor_bp = Blueprint(
    'fornecedor',
    __name__,
    url_prefix='/fornecedores',
    template_folder='templates'
)

# Gerador de código automático
def gerar_codigo_fornecedor():
    ultimo = Fornecedor.query.order_by(Fornecedor.id.desc()).first()
    if not ultimo or not ultimo.codigo or not ultimo.codigo.startswith("FOR"):
        return "FOR0001"
    try:
        numero = int(ultimo.codigo[3:]) + 1
    except Exception:
        numero = 1
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
        fornecedor.nome = request.form['nome']
        fornecedor.cnpj = request.form.get('cnpj')
        fornecedor.telefone = request.form.get('telefone')
        fornecedor.cep = request.form.get('cep')
        fornecedor.cidade = request.form.get('cidade')
        fornecedor.endereco = request.form.get('endereco')

        db.session.add(fornecedor)
        db.session.commit()
        return redirect(url_for('fornecedor.listar_fornecedores'))
    return render_template('fornecedor/cadastro.html')

@fornecedor_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    if request.method == 'POST':
        fornecedor.nome = request.form['nome']
        fornecedor.cnpj = request.form.get('cnpj')
        fornecedor.telefone = request.form.get('telefone')
        fornecedor.cep = request.form.get('cep')
        fornecedor.cidade = request.form.get('cidade')
        fornecedor.endereco = request.form.get('endereco')
        db.session.commit()
        return redirect(url_for('fornecedor.listar_fornecedores'))
    return render_template('fornecedor/cadastro.html', fornecedor=fornecedor)

@fornecedor_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    return redirect(url_for('fornecedor.listar_fornecedores'))
