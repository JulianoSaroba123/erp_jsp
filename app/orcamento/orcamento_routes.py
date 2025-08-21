from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from extensoes import db
from .orcamento_model import Orcamento
from datetime import datetime
import os

orcamento_bp = Blueprint('orcamento', __name__, url_prefix='/orcamento')

@orcamento_bp.route('/')
def lista_orcamentos():
    orcamentos = Orcamento.query.order_by(Orcamento.data_emissao.desc()).all()
    return render_template('orcamento/lista_orcamentos.html', orcamentos=orcamentos)

@orcamento_bp.route('/novo', methods=['GET', 'POST'])
def novo_orcamento():
    if request.method == 'POST':
        # Coleta dados do formulário (igual OS)
        dados = request.form.to_dict()
        orcamento = Orcamento(
            codigo=dados.get('codigo'),
            cliente_id=dados.get('cliente_id'),
            status='Aguardando',
            data_emissao=datetime.today(),
            validade=dados.get('validade'),
            valor_total=dados.get('valor_total', 0),
            servicos_dados=dados.get('servicos_json'),
            produtos_dados=dados.get('produtos_json'),
            observacoes=dados.get('observacoes'),
        )
        db.session.add(orcamento)
        db.session.commit()
        flash('Orçamento criado com sucesso!', 'success')
        return redirect(url_for('orcamento.lista_orcamentos'))
    return render_template('orcamento/cadastro_orcamento.html')

@orcamento_bp.route('/<int:id>/pdf')
def gerar_pdf_orcamento(id):
    # Aqui será implementada a geração do PDF conforme modelo
    orcamento = Orcamento.query.get_or_404(id)
    # ... gerar PDF e salvar em orcamento.pdf_path ...
    # Exemplo: return send_file(orcamento.pdf_path)
    flash('Função de geração de PDF ainda não implementada.', 'info')
    return redirect(url_for('orcamento.lista_orcamentos'))

@orcamento_bp.route('/<int:id>/aprovar', methods=['POST'])
def aprovar_orcamento(id):
    orcamento = Orcamento.query.get_or_404(id)
    orcamento.status = 'Aprovado'
    db.session.commit()
    flash('Orçamento aprovado! Você pode gerar uma Ordem de Serviço.', 'success')
    return redirect(url_for('orcamento.lista_orcamentos'))

@orcamento_bp.route('/<int:id>/gerar-os', methods=['POST'])
def gerar_os(id):
    orcamento = Orcamento.query.get_or_404(id)
    # Aqui será implementada a lógica para criar uma OS a partir do orçamento
    flash('Função de gerar OS a partir do orçamento ainda não implementada.', 'info')
    return redirect(url_for('orcamento.lista_orcamentos'))
