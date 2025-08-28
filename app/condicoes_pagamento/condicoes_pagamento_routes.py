from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensoes import db
from app.condicoes_pagamento.condicoes_pagamento_model import CondicaoPagamento

condicoes_pagamento_bp = Blueprint('condicoes_pagamento', __name__)

# Listar condições de pagamento
@condicoes_pagamento_bp.route('/condicoes_pagamento/lista')
def listar_condicoes_pagamento():
	condicoes = CondicaoPagamento.query.order_by(CondicaoPagamento.id.desc()).all()
	return render_template('condicoes_pagamento/lista.html', condicoes=condicoes)

# Cadastrar nova condição
@condicoes_pagamento_bp.route('/condicoes_pagamento/novo', methods=['GET', 'POST'])
def nova_condicao_pagamento():
	if request.method == 'POST':
		condicao = CondicaoPagamento(
			descricao=request.form['descricao'],
			tipo=request.form['tipo'],
			parcelas=request.form.get('parcelas', 1),
			desconto=request.form.get('desconto', 0.0),
			juros=request.form.get('juros', 0.0),
			observacoes=request.form.get('observacoes', '')
		)
		db.session.add(condicao)
		db.session.commit()
		flash('Condição de pagamento cadastrada com sucesso!', 'success')
		return redirect(url_for('condicoes_pagamento.listar_condicoes_pagamento'))
	return render_template('condicoes_pagamento/cadastro.html')

# Editar condição
@condicoes_pagamento_bp.route('/condicoes_pagamento/editar/<int:id>', methods=['GET', 'POST'])
def editar_condicao_pagamento(id):
	condicao = CondicaoPagamento.query.get_or_404(id)
	if request.method == 'POST':
		condicao.descricao = request.form['descricao']
		condicao.tipo = request.form['tipo']
		condicao.parcelas = request.form.get('parcelas', 1)
		condicao.desconto = request.form.get('desconto', 0.0)
		condicao.juros = request.form.get('juros', 0.0)
		condicao.observacoes = request.form.get('observacoes', '')
		db.session.commit()
		flash('Condição de pagamento atualizada!', 'success')
		return redirect(url_for('condicoes_pagamento.listar_condicoes_pagamento'))
	return render_template('condicoes_pagamento/cadastro.html', condicao=condicao)

# Excluir condição
@condicoes_pagamento_bp.route('/condicoes_pagamento/excluir/<int:id>', methods=['POST'])
def excluir_condicao_pagamento(id):
	condicao = CondicaoPagamento.query.get_or_404(id)
	db.session.delete(condicao)
	db.session.commit()
	flash('Condição de pagamento excluída!', 'success')
	return redirect(url_for('condicoes_pagamento.listar_condicoes_pagamento'))
