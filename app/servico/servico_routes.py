from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.servico.servico_model import Servico
from app.extensoes import db

servico_bp = Blueprint('servico', __name__, url_prefix='/servicos', template_folder='templates')

@servico_bp.route('/api/busca', methods=['GET'])
def api_busca_servicos():
    """API para autocomplete de serviços (Select2)"""
    termo = request.args.get('q', '').strip()
    query = Servico.query.filter(Servico.ativo == True)
    if termo:
        query = query.filter(Servico.nome.ilike(f'%{termo}%'))
    servicos = query.order_by(Servico.nome).limit(20).all()
    return jsonify([
        {
            'id': s.id,
            'nome': s.nome,
            'valor': s.valor,
            'descricao': s.descricao or ''
        } for s in servicos
    ])

def gerar_codigo_servico():
    ultimo = Servico.query.order_by(Servico.id.desc()).first()
    if not ultimo or not ultimo.codigo.startswith("SRV"):
        return "SRV0001"
    numero = int(ultimo.codigo[3:]) + 1
    return f"SRV{numero:04d}"

@servico_bp.route('/')
def listar_servicos():
    servicos = Servico.query.filter_by(ativo=True).all()
    
    # Estatísticas
    total_servicos = len(servicos)
    valor_total = sum(servico.valor for servico in servicos)
    valor_medio = valor_total / total_servicos if total_servicos > 0 else 0
    
    return render_template('servico/lista.html', 
                         servicos=servicos,
                         total_servicos=total_servicos,
                         valor_total=valor_total,
                         valor_medio=valor_medio)

@servico_bp.route('/novo', methods=['GET', 'POST'])
def novo_servico():
    if request.method == 'POST':
        servico = Servico()
        servico.codigo = gerar_codigo_servico()
        servico.nome = request.form['nome']
        servico.descricao = request.form.get('descricao')
        servico.unidade = request.form.get('unidade', 'UN')
        servico.preco_custo = float(request.form.get('preco_custo', 0))
        servico.calcular_preco_venda(float(request.form.get('markup_percentual', 0)))
        db.session.add(servico)
        db.session.commit()
        return redirect(url_for('servico.listar_servicos'))
    return render_template('servico/cadastro.html')

@servico_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_servico(id):
    servico = Servico.query.get_or_404(id)
    if request.method == 'POST':
        servico.nome = request.form['nome']
        servico.descricao = request.form.get('descricao')
        servico.unidade = request.form.get('unidade', 'UN')
        servico.preco_custo = float(request.form.get('preco_custo', 0))
        servico.calcular_preco_venda(float(request.form.get('markup_percentual', 0)))
        db.session.commit()
        return redirect(url_for('servico.listar_servicos'))
    return render_template('servico/cadastro.html', servico=servico)

@servico_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    servico.ativo = False
    db.session.commit()
    return redirect(url_for('servico.listar_servicos'))
