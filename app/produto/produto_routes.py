from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.produto.produto_model import Produto  
from extensoes import db

produto_bp = Blueprint('produto', __name__, url_prefix='/produtos', template_folder='templates')

@produto_bp.route('/api/busca', methods=['GET'])
def api_busca_produtos():
    """API para autocomplete de produtos (Select2)"""
    termo = request.args.get('q', '').strip()
    query = Produto.query.filter(Produto.ativo == True)
    if termo:
        query = query.filter(Produto.nome.ilike(f'%{termo}%'))
    produtos = query.order_by(Produto.nome).limit(20).all()
    return jsonify([
        {
            'id': p.id,
            'nome': p.nome,
            'preco_venda': p.preco_venda,
            'descricao': p.descricao or ''
        } for p in produtos
    ])

produto_bp = Blueprint('produto', __name__, url_prefix='/produtos', template_folder='templates')

def gerar_codigo_produto():
    ultimo = Produto.query.order_by(Produto.id.desc()).first()
    if not ultimo or not ultimo.codigo.startswith("PRD"):
        return "PRD0001"
    numero = int(ultimo.codigo[3:]) + 1
    return f"PRD{numero:04}"

@produto_bp.route('/')
def listar_produtos():
    produtos = Produto.query.filter_by(ativo=True).all()
    return render_template('produto/lista.html', produtos=produtos)

@produto_bp.route('/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        produto = Produto()
        produto.codigo = gerar_codigo_produto()
        produto.nome = request.form['nome']
        produto.descricao = request.form.get('descricao')
        produto.categoria = request.form.get('categoria')
        produto.marca = request.form.get('marca')
        produto.unidade = request.form.get('unidade', 'UN')
        
        # Controle de estoque
        produto.estoque_atual = float(request.form.get('estoque_atual', 0))
        produto.estoque_minimo = float(request.form.get('estoque_minimo', 0))
        
        # Preços e markup
        produto.preco_custo = float(request.form.get('preco_custo', 0))
        produto.markup_percentual = float(request.form.get('markup_percentual', 0))
        
        # Dados complementares
        produto.codigo_barras = request.form.get('codigo_barras')
        produto.ncm = request.form.get('ncm')
        produto.peso = float(request.form.get('peso', 0)) if request.form.get('peso') else None
        
        # Calcula preço de venda
        produto.calcular_preco_venda()
        
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('produto.listar_produtos'))
    
    codigo_gerado = gerar_codigo_produto()
    return render_template('produto/cadastro.html', codigo_gerado=codigo_gerado)

@produto_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form.get('descricao')
        produto.categoria = request.form.get('categoria')
        produto.marca = request.form.get('marca')
        produto.unidade = request.form.get('unidade', 'UN')
        
        # Controle de estoque
        produto.estoque_atual = float(request.form.get('estoque_atual', 0))
        produto.estoque_minimo = float(request.form.get('estoque_minimo', 0))
        
        # Preços e markup
        produto.preco_custo = float(request.form.get('preco_custo', 0))
        produto.markup_percentual = float(request.form.get('markup_percentual', 0))
        
        # Dados complementares
        produto.codigo_barras = request.form.get('codigo_barras')
        produto.ncm = request.form.get('ncm')
        produto.peso = float(request.form.get('peso', 0)) if request.form.get('peso') else None
        
        # Calcula preço de venda
        produto.calcular_preco_venda()
        
        db.session.commit()
        return redirect(url_for('produto.listar_produtos'))
    
    return render_template('produto/cadastro.html', produto=produto, codigo_gerado=produto.codigo)

@produto_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    # Não remove fisicamente, apenas marca como inativo
    produto.ativo = False
    db.session.commit()
    return redirect(url_for('produto.listar_produtos'))

# API para cálculo de markup em tempo real
@produto_bp.route('/api/calcular-markup', methods=['POST'])
def calcular_markup_api():
    try:
        data = request.get_json()
        preco_custo = float(data.get('preco_custo', 0))
        markup_percentual = float(data.get('markup_percentual', 0))
        
        if preco_custo and markup_percentual:
            preco_venda = preco_custo * (1 + (markup_percentual / 100))
            markup_valor = preco_custo * (markup_percentual / 100)
            margem_lucro = ((preco_venda - preco_custo) / preco_venda) * 100 if preco_venda > 0 else 0
            
            return jsonify({
                'success': True,
                'preco_venda': round(preco_venda, 2),
                'markup_valor': round(markup_valor, 2),
                'margem_lucro': round(margem_lucro, 2)
            })
        else:
            return jsonify({
                'success': True,
                'preco_venda': preco_custo,
                'markup_valor': 0,
                'margem_lucro': 0
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
