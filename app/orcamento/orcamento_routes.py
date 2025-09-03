from flask import Blueprint, render_template, request, redirect, url_for
from app.extensoes import db
from app.orcamento.orcamento_model import Orcamento
from app.cliente.cliente_model import Cliente
from app.configuracoes.condicoes_pagamento.condicoes_pagamento_model import CondicaoPagamento
from datetime import datetime

orcamento_bp = Blueprint('orcamento', __name__, template_folder='templates')

@orcamento_bp.route('/orcamento/lista')
def listar_orcamentos():
    orcamentos = Orcamento.query.order_by(Orcamento.data.desc()).all()
    return render_template('orcamento/lista.html', orcamentos=orcamentos)

@orcamento_bp.route('/orcamento/novo')
def novo_orcamento():
    clientes = Cliente.query.all()
    condicoes = CondicaoPagamento.query.all()
    return render_template(
        'orcamento/cadastro.html',
        clientes=clientes,
        condicoes=condicoes,
        data_hoje=datetime.today().date()
    )

@orcamento_bp.route('/orcamento/salvar', methods=['POST'])
def salvar_orcamento():
    codigo = gerar_codigo_orcamento()
    novo = Orcamento(
        codigo=codigo,
        cliente_id=request.form['cliente_id'],
        data=datetime.strptime(request.form['data'], '%Y-%m-%d'),
        validade=request.form['validade'],
        condicao_pagamento_id=request.form['condicao_pagamento_id'],
        valor_total=request.form['valor_total'],
        status=request.form['status']
    )
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('orcamento.novo_orcamento'))



from flask import Blueprint, render_template, request, redirect, url_for
from app.extensoes import db
from app.orcamento.orcamento_model import Orcamento
from app.cliente.cliente_model import Cliente
from app.configuracoes.condicoes_pagamento.condicoes_pagamento_model import CondicaoPagamento
from datetime import datetime

orcamento_bp = Blueprint('orcamento', __name__, template_folder='templates')

@orcamento_bp.route('/orcamento/lista')
def listar_orcamentos():
    orcamentos = Orcamento.query.order_by(Orcamento.data.desc()).all()
    return render_template('orcamento/lista.html', orcamentos=orcamentos)

@orcamento_bp.route('/orcamento/novo')
def novo_orcamento():
    clientes = Cliente.query.all()
    condicoes = CondicaoPagamento.query.all()
    return render_template(
        'orcamento/cadastro.html',
        clientes=clientes,
        condicoes=condicoes,
        data_hoje=datetime.today().date()
    )

@orcamento_bp.route('/orcamento/salvar', methods=['POST'])
def salvar_orcamento():
    codigo = gerar_codigo_orcamento()
    novo = Orcamento(
        codigo=codigo,
        cliente_id=request.form['cliente_id'],
        data=datetime.strptime(request.form['data'], '%Y-%m-%d'),
        validade=request.form['validade'],
        condicao_pagamento_id=request.form['condicao_pagamento_id'],
        valor_total=request.form['valor_total'],
        status=request.form['status']
    )
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('orcamento.novo_orcamento'))

def gerar_codigo_orcamento():
    ultimo = Orcamento.query.order_by(Orcamento.id.desc()).first()
    numero = 1 if not ultimo else ultimo.id + 1
    return f"ORC{str(numero).zfill(4)}"

# Rota para editar orçamento
@orcamento_bp.route('/orcamento/<int:id>/editar', methods=['GET', 'POST'])
def editar_orcamento(id):
    orcamento = Orcamento.query.get_or_404(id)
    clientes = Cliente.query.all()
    condicoes = CondicaoPagamento.query.all()
    if request.method == 'POST':
        orcamento.cliente_id = request.form['cliente_id']
        orcamento.data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        orcamento.validade = request.form['validade']
        orcamento.condicao_pagamento_id = request.form['condicao_pagamento_id']
        orcamento.valor_total = request.form['valor_total']
        orcamento.status = request.form['status']
        db.session.commit()
        return redirect(url_for('orcamento.listar_orcamentos'))
    return render_template('orcamento/cadastro.html', orcamento=orcamento, clientes=clientes, condicoes=condicoes, data_hoje=orcamento.data)

# Rota para excluir orçamento
@orcamento_bp.route('/orcamento/<int:id>/excluir', methods=['GET', 'POST'])
def excluir_orcamento(id):
    orcamento = Orcamento.query.get_or_404(id)
    db.session.delete(orcamento)
    db.session.commit()
    return redirect(url_for('orcamento.listar_orcamentos'))


# Rota para visualizar orçamento
@orcamento_bp.route('/orcamento/<int:id>')
def visualizar_orcamento(id):
    orcamento = Orcamento.query.get_or_404(id)
    return render_template('orcamento/visualizar.html', orcamento=orcamento)
