from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.produto.produto_model import Produto
from app.fornecedor.fornecedor_model import Fornecedor   # 👈 IMPORTA ISSO
from app.extensoes import db

produto_bp = Blueprint('produto', __name__, url_prefix='/produtos', template_folder='templates')

def gerar_codigo_produto():
    ultimo = Produto.query.order_by(Produto.id.desc()).first()
    if not ultimo or not ultimo.codigo.startswith("PRD"):
        return "PRD0001"
    try:
        numero = int(ultimo.codigo[3:]) + 1
    except ValueError:
        numero = 1
    return f"PRD{numero:04}"

@produto_bp.route('/')
def listar_produtos():
    produtos = Produto.query.filter_by(ativo=True).all()
    return render_template('produto/lista.html', produtos=produtos)

# app/produto/produto_routes.py

@produto_bp.route('/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        produto = Produto()
        produto.codigo = gerar_codigo_produto()
        produto.nome = request.form['nome']
        produto.descricao = request.form.get('descricao')
        produto.categoria = request.form.get('categoria')
        produto.marca = request.form.get('marca')

        # 👇 higieniza e transforma '' em None
        produto.modelo = (request.form.get('modelo') or '').strip() or None
        produto.numero_serie = (request.form.get('numero_serie') or '').strip() or None

        fornecedor_id = request.form.get('fornecedor_id')
        produto.fornecedor_id = int(fornecedor_id) if fornecedor_id else None

        produto.unidade = request.form.get('unidade', 'UN')
        produto.estoque_atual = float(request.form.get('estoque_atual', 0))
        produto.estoque_minimo = float(request.form.get('estoque_minimo', 0))
        produto.preco_custo = float(request.form.get('preco_custo', 0))
        produto.markup_percentual = float(request.form.get('markup_percentual', 0))
        produto.codigo_barras = request.form.get('codigo_barras')
        produto.ncm = request.form.get('ncm')
        produto.peso = float(request.form.get('peso', 0)) if request.form.get('peso') else None

        produto.calcular_preco_venda()
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('produto.listar_produtos'))

    fornecedores = Fornecedor.query.order_by(Fornecedor.nome).all()
    return render_template('produto/cadastro.html',
                           codigo_gerado=gerar_codigo_produto(),
                           fornecedores=fornecedores)


@produto_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form.get('descricao')
        produto.categoria = request.form.get('categoria')
        produto.marca = request.form.get('marca')

        # 👇 mesmo tratamento aqui
        produto.modelo = (request.form.get('modelo') or '').strip() or None
        produto.numero_serie = (request.form.get('numero_serie') or '').strip() or None

        fornecedor_id = request.form.get('fornecedor_id')
        produto.fornecedor_id = int(fornecedor_id) if fornecedor_id else None

        produto.unidade = request.form.get('unidade', 'UN')
        produto.estoque_atual = float(request.form.get('estoque_atual', 0))
        produto.estoque_minimo = float(request.form.get('estoque_minimo', 0))
        produto.preco_custo = float(request.form.get('preco_custo', 0))
        produto.markup_percentual = float(request.form.get('markup_percentual', 0))
        produto.codigo_barras = request.form.get('codigo_barras')
        produto.ncm = request.form.get('ncm')
        produto.peso = float(request.form.get('peso', 0)) if request.form.get('peso') else None

        produto.calcular_preco_venda()
        db.session.commit()
        return redirect(url_for('produto.listar_produtos'))

    fornecedores = Fornecedor.query.order_by(Fornecedor.nome).all()
    return render_template('produto/cadastro.html',
                           produto=produto,
                           fornecedores=fornecedores)



@produto_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    produto.ativo = False
    db.session.commit()
    return redirect(url_for('produto.listar_produtos'))
