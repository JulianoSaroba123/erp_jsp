
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime, date, timedelta
from app.extensoes import db
from .financeiro_model import LancamentoFinanceiro
from . import financeiro_bp

@financeiro_bp.app_template_filter('moeda')
def moeda_br(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"

@financeiro_bp.route('/dashboard')
def dashboard():
    # Período padrão: mês atual
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)
    fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Buscar lançamentos do período
    lancamentos = LancamentoFinanceiro.query.filter(
        LancamentoFinanceiro.data >= inicio_mes,
        LancamentoFinanceiro.data <= fim_mes
    ).all()
    
    # Calcular totais
    receitas = sum(x.valor for x in lancamentos if x.is_receita())
    despesas = sum(x.valor for x in lancamentos if x.is_despesa())
    saldo = receitas - despesas
    
    # Valores para DRE (simplificado)
    rec_dre = receitas
    des_dre = despesas
    lucro = rec_dre - des_dre
    
    # Valores fictícios para demonstração
    pe_reais = saldo * 0.1  # 10% do saldo como exemplo
    base_hora = 50.0  # valor base por hora
    valor_hora = base_hora + (lucro / 160) if lucro > 0 else base_hora  # 160h/mês
    
    return render_template('financeiro/dashboard.html',
                         periodo=[inicio_mes, fim_mes],
                         receitas=receitas,
                         despesas=despesas,
                         saldo=saldo,
                         pe_reais=pe_reais,
                         rec_dre=rec_dre,
                         des_dre=des_dre,
                         lucro=lucro,
                         valor_hora=valor_hora,
                         base_hora=base_hora)

@financeiro_bp.route('/')
def listar():
    tipo = request.args.get('tipo')      # Receita/Despesa/None
    status = request.args.get('status')  # Pago/Pendente/Atrasado/None
    de = request.args.get('de')          # YYYY-MM-DD
    ate = request.args.get('ate')        # YYYY-MM-DD

    q = LancamentoFinanceiro.query
    if tipo: q = q.filter(LancamentoFinanceiro.tipo == tipo)
    if status: q = q.filter(LancamentoFinanceiro.status == status)
    if de: q = q.filter(LancamentoFinanceiro.data >= de)
    if ate: q = q.filter(LancamentoFinanceiro.data <= ate)

    registros = q.order_by(LancamentoFinanceiro.data.desc(), LancamentoFinanceiro.id.desc()).all()

    total_receitas = sum(x.valor for x in registros if x.is_receita())
    total_despesas = sum(x.valor for x in registros if x.is_despesa())
    saldo = total_receitas - total_despesas

    return render_template('financeiro/lista_financeiro.html',
                           registros=registros,
                           total_receitas=total_receitas,
                           total_despesas=total_despesas,
                           saldo=saldo,
                           filtros={'tipo': tipo, 'status': status, 'de': de, 'ate': ate})

@financeiro_bp.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        dados = request.form
        try:
            lanc = LancamentoFinanceiro(
                tipo=dados.get('tipo'),
                categoria=dados.get('categoria'),
                descricao=dados.get('descricao'),
                valor=float(dados.get('valor') or 0),
                data=datetime.strptime(dados.get('data'), '%Y-%m-%d').date() if dados.get('data') else datetime.utcnow().date(),
                forma_pagamento=dados.get('forma_pagamento'),
                status=dados.get('status') or 'Pendente',
                observacoes=dados.get('observacoes')
            )
            db.session.add(lanc)
            db.session.commit()
            flash('Lançamento salvo!', 'success')
            return redirect(url_for('financeiro.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar: {e}', 'danger')

    return render_template('financeiro/cadastro_financeiro.html')

@financeiro_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    lanc = LancamentoFinanceiro.query.get_or_404(id)
    db.session.delete(lanc)
    db.session.commit()
    flash('Lançamento excluído!', 'success')
    return redirect(url_for('financeiro.listar'))

