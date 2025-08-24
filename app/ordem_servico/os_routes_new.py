from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file, abort, make_response
from extensoes import db
from .os_model import OrdemServico
from .os_calculos import CalculadoraOS
from produto.produto_model import Produto
from servico.servico_model import Servico
from financeiro.financeiro_model import LancamentoFinanceiro
from cliente.cliente_model import Cliente
from datetime import datetime, date
import json

# Blueprint
os_bp = Blueprint('os', __name__, url_prefix='/os')

# === LISTAR ORDENS DE SERVIÇO ===
@os_bp.route('/', methods=['GET'])
def listar_os():
    """Lista todas as ordens de serviço"""
    try:
        ordens = OrdemServico.query.filter_by(ativo=True).order_by(OrdemServico.id.desc()).all()
        return render_template('ordem_servico/listar.html', ordens=ordens)
    except Exception as e:
        flash(f'Erro ao carregar ordens de serviço: {str(e)}', 'error')
        return render_template('ordem_servico/listar.html', ordens=[])

# === NOVA ORDEM DE SERVIÇO ===
@os_bp.route('/nova', methods=['GET', 'POST'])
def nova_os():
    """Criar nova ordem de serviço"""
    if request.method == 'GET':
        clientes = Cliente.query.filter_by(ativo=True).all()
        servicos = Servico.query.filter_by(ativo=True).all()
        produtos = Produto.query.filter_by(ativo=True).all()
        return render_template('ordem_servico/cadastro_new.html', 
                             clientes=clientes, servicos=servicos, produtos=produtos)
    
    try:
        dados = request.form.to_dict()
        
        # Gerar código automático
        ultima_os = OrdemServico.query.order_by(OrdemServico.id.desc()).first()
        if ultima_os and ultima_os.codigo:
            num = int(ultima_os.codigo.replace('OS', '')) + 1
        else:
            num = 1
        codigo = f'OS{num:04d}'
        
        # Criar nova ordem
        ordem = OrdemServico()
        ordem.codigo = codigo
        ordem.cliente_id = dados.get('cliente_id')
        ordem.data_emissao = datetime.strptime(dados.get('data_emissao'), '%Y-%m-%d').date() if dados.get('data_emissao') else date.today()
        ordem.tipo_servico = dados.get('tipo_servico')
        ordem.prioridade = dados.get('prioridade', 'Normal')
        ordem.status = dados.get('status', 'Aberta')
        ordem.tecnico_responsavel = dados.get('tecnico_responsavel')
        ordem.supervisor = dados.get('supervisor')
        
        # Equipamento
        ordem.equipamento_nome = dados.get('equipamento_nome')
        ordem.equipamento_marca = dados.get('equipamento_marca')
        ordem.equipamento_modelo = dados.get('equipamento_modelo')
        ordem.equipamento_numero_serie = dados.get('equipamento_numero_serie')
        ordem.equipamento_acessorios = dados.get('equipamento_acessorios')
        ordem.equipamento_problema = dados.get('equipamento_problema')
        ordem.local_instalacao = dados.get('local_instalacao')
        
        # Horários
        if dados.get('hora_inicio'):
            ordem.hora_inicio = datetime.strptime(dados.get('hora_inicio'), '%H:%M').time()
        if dados.get('hora_termino'):
            ordem.hora_termino = datetime.strptime(dados.get('hora_termino'), '%H:%M').time()
        ordem.total_horas = float(dados.get('total_horas', 0))
        
        # Descrições
        ordem.problema_descrito = dados.get('problema_descrito')
        ordem.descricao_problema = dados.get('descricao_problema')
        ordem.descricao_servico_realizado = dados.get('descricao_servico_realizado')
        ordem.solucao_aplicada = dados.get('solucao_aplicada')
        
        # Deslocamento
        ordem.km_inicial = float(dados.get('km_inicial', 0))
        ordem.km_final = float(dados.get('km_final', 0))
        ordem.km_total = float(dados.get('km_total', 0))
        ordem.valor_deslocamento = float(dados.get('valor_deslocamento', 0))
        
        # Valores
        ordem.valor_mao_obra = float(dados.get('valor_mao_obra', 0))
        ordem.valor_produtos = float(dados.get('valor_produtos', 0))
        ordem.valor_servicos = float(dados.get('valor_servicos', 0))
        ordem.valor_descontos = float(dados.get('valor_descontos', 0))
        ordem.valor_total = float(dados.get('valor_total', 0))
        
        # Pagamento
        ordem.forma_pagamento = dados.get('forma_pagamento', 'À Vista')
        ordem.condicoes_pagamento = dados.get('condicoes_pagamento')
        
        # Observações
        ordem.observacoes_tecnico = dados.get('observacoes_tecnico')
        ordem.observacoes_cliente = dados.get('observacoes_cliente')
        ordem.observacoes_internas = dados.get('observacoes_internas')
        ordem.outras_informacoes = dados.get('outras_informacoes')
        
        # JSON dados
        ordem.servicos_dados = dados.get('servicos_dados')
        ordem.produtos_dados = dados.get('produtos_dados')
        ordem.parcelas_json = dados.get('parcelas_json')
        
        db.session.add(ordem)
        db.session.commit()
        
        flash(f'Ordem de serviço {codigo} criada com sucesso!', 'success')
        return redirect(url_for('os.visualizar_os', id=ordem.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao criar ordem de serviço: {str(e)}', 'error')
        clientes = Cliente.query.filter_by(ativo=True).all()
        servicos = Servico.query.filter_by(ativo=True).all()
        produtos = Produto.query.filter_by(ativo=True).all()
        return render_template('ordem_servico/cadastro_new.html', 
                             clientes=clientes, servicos=servicos, produtos=produtos)

# === VISUALIZAR ORDEM DE SERVIÇO ===
@os_bp.route('/<int:id>')
def visualizar_os(id):
    """Visualizar ordem de serviço"""
    try:
        ordem = OrdemServico.query.get_or_404(id)
        
        # Parsear dados JSON
        servicos = []
        produtos = []
        parcelas = []
        
        if ordem.servicos_dados:
            try:
                servicos = json.loads(ordem.servicos_dados)
            except:
                pass
                
        if ordem.produtos_dados:
            try:
                produtos = json.loads(ordem.produtos_dados)
            except:
                pass
                
        if ordem.parcelas_json:
            try:
                parcelas = json.loads(ordem.parcelas_json)
            except:
                pass
        
        return render_template('os_visualizar.html', 
                             os=ordem, servicos=servicos, produtos=produtos, parcelas=parcelas)
    except Exception as e:
        flash(f'Erro ao carregar ordem de serviço: {str(e)}', 'error')
        return redirect(url_for('os.listar_os'))

# === EDITAR ORDEM DE SERVIÇO ===
@os_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_os(id):
    """Editar ordem de serviço"""
    ordem = OrdemServico.query.get_or_404(id)
    
    if request.method == 'GET':
        clientes = Cliente.query.filter_by(ativo=True).all()
        servicos = Servico.query.filter_by(ativo=True).all()
        produtos = Produto.query.filter_by(ativo=True).all()
        return render_template('ordem_servico/cadastro_new.html', 
                             ordem_servico=ordem, clientes=clientes, servicos=servicos, produtos=produtos)
    
    try:
        dados = request.form.to_dict()
        
        # Atualizar campos básicos
        ordem.cliente_id = dados.get('cliente_id')
        if dados.get('data_emissao'):
            ordem.data_emissao = datetime.strptime(dados.get('data_emissao'), '%Y-%m-%d').date()
        
        ordem.tipo_servico = dados.get('tipo_servico')
        ordem.prioridade = dados.get('prioridade', 'Normal')
        ordem.status = dados.get('status', 'Aberta')
        ordem.tecnico_responsavel = dados.get('tecnico_responsavel')
        ordem.supervisor = dados.get('supervisor')
        
        # Equipamento
        ordem.equipamento_nome = dados.get('equipamento_nome')
        ordem.equipamento_marca = dados.get('equipamento_marca')
        ordem.equipamento_modelo = dados.get('equipamento_modelo')
        ordem.equipamento_numero_serie = dados.get('equipamento_numero_serie')
        ordem.equipamento_acessorios = dados.get('equipamento_acessorios')
        ordem.equipamento_problema = dados.get('equipamento_problema')
        ordem.local_instalacao = dados.get('local_instalacao')
        
        # Horários
        if dados.get('hora_inicio'):
            ordem.hora_inicio = datetime.strptime(dados.get('hora_inicio'), '%H:%M').time()
        if dados.get('hora_termino'):
            ordem.hora_termino = datetime.strptime(dados.get('hora_termino'), '%H:%M').time()
        ordem.total_horas = float(dados.get('total_horas', 0))
        
        # Descrições
        ordem.problema_descrito = dados.get('problema_descrito')
        ordem.descricao_problema = dados.get('descricao_problema')
        ordem.descricao_servico_realizado = dados.get('descricao_servico_realizado')
        ordem.solucao_aplicada = dados.get('solucao_aplicada')
        
        # Deslocamento
        ordem.km_inicial = float(dados.get('km_inicial', 0))
        ordem.km_final = float(dados.get('km_final', 0))
        ordem.km_total = float(dados.get('km_total', 0))
        ordem.valor_deslocamento = float(dados.get('valor_deslocamento', 0))
        
        # Valores
        ordem.valor_mao_obra = float(dados.get('valor_mao_obra', 0))
        ordem.valor_produtos = float(dados.get('valor_produtos', 0))
        ordem.valor_servicos = float(dados.get('valor_servicos', 0))
        ordem.valor_descontos = float(dados.get('valor_descontos', 0))
        ordem.valor_total = float(dados.get('valor_total', 0))
        
        # Pagamento
        ordem.forma_pagamento = dados.get('forma_pagamento', 'À Vista')
        ordem.condicoes_pagamento = dados.get('condicoes_pagamento')
        
        # Observações
        ordem.observacoes_tecnico = dados.get('observacoes_tecnico')
        ordem.observacoes_cliente = dados.get('observacoes_cliente')
        ordem.observacoes_internas = dados.get('observacoes_internas')
        ordem.outras_informacoes = dados.get('outras_informacoes')
        
        # JSON dados
        ordem.servicos_dados = dados.get('servicos_dados')
        ordem.produtos_dados = dados.get('produtos_dados')
        ordem.parcelas_json = dados.get('parcelas_json')
        
        db.session.commit()
        
        flash(f'Ordem de serviço {ordem.codigo} atualizada com sucesso!', 'success')
        return redirect(url_for('os.visualizar_os', id=ordem.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar ordem de serviço: {str(e)}', 'error')
        clientes = Cliente.query.filter_by(ativo=True).all()
        servicos = Servico.query.filter_by(ativo=True).all()
        produtos = Produto.query.filter_by(ativo=True).all()
        return render_template('ordem_servico/cadastro_new.html', 
                             ordem_servico=ordem, clientes=clientes, servicos=servicos, produtos=produtos)

# === ALTERAR STATUS ===
@os_bp.route('/alterar_status/<int:id>', methods=['POST'])
def alterar_status(id):
    """Alterar status da ordem de serviço e integrar com financeiro"""
    try:
        ordem = OrdemServico.query.get_or_404(id)
        novo_status = request.json.get('status')
        
        if not novo_status:
            return jsonify({'success': False, 'message': 'Status não informado'}), 400
        
        status_anterior = ordem.status
        ordem.status = novo_status
        
        # Se está marcando como concluída, verificar se deve criar lançamentos financeiros
        if novo_status == 'Concluída' and status_anterior != 'Concluída':
            # Verificar se a forma de pagamento indica pagamento efetivado
            forma_pag = (ordem.forma_pagamento or '').lower()
            pode_lancar = forma_pag in ['pago', 'à vista', 'a vista', 'dinheiro', 'pix', 'cartão', 'cartao']
            
            print(f"DEBUG: OS {ordem.codigo} - Status: {novo_status}")
            print(f"DEBUG: Forma de pagamento: '{ordem.forma_pagamento}' - Pode lançar: {pode_lancar}")
            
            if pode_lancar and ordem.valor_total and ordem.valor_total > 0:
                # Verificar se já existem lançamentos ativos
                lancamentos_existentes = LancamentoFinanceiro.query.filter(
                    LancamentoFinanceiro.descricao.like(f'%{ordem.codigo}%'),
                    ~LancamentoFinanceiro.status.in_(['Cancelado', 'Excluído'])
                ).count()
                
                if lancamentos_existentes == 0:
                    # Criar lançamento financeiro
                    lancamento = LancamentoFinanceiro()
                    lancamento.tipo = 'Receita'
                    lancamento.categoria = 'Serviços'
                    lancamento.descricao = f'Serviços OS {ordem.codigo} - {ordem.cliente.nome if ordem.cliente else "Cliente"}'
                    lancamento.valor = ordem.valor_total
                    lancamento.data_vencimento = date.today()
                    lancamento.status = 'Pago'  # Marca como pago pois forma_pagamento indica pagamento
                    lancamento.observacoes = f'Lançamento automático - OS concluída com pagamento'
                    
                    db.session.add(lancamento)
                    print(f"DEBUG: Lançamento criado para OS {ordem.codigo}: R$ {ordem.valor_total}")
                else:
                    print(f"DEBUG: Já existem {lancamentos_existentes} lançamentos para OS {ordem.codigo}")
            else:
                print(f"DEBUG: Não criando lançamentos. Forma de pagamento '{ordem.forma_pagamento}' não indica pagamento efetivado.")
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Status alterado para {novo_status}',
            'status': novo_status
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# === DELETAR ORDEM DE SERVIÇO ===
@os_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_os(id):
    """Soft delete da ordem de serviço e cancelar lançamentos financeiros"""
    try:
        ordem = OrdemServico.query.get_or_404(id)
        
        # Cancelar lançamentos financeiros relacionados
        lancamentos = LancamentoFinanceiro.query.filter(
            LancamentoFinanceiro.descricao.like(f'%{ordem.codigo}%'),
            ~LancamentoFinanceiro.status.in_(['Cancelado', 'Excluído'])
        ).all()
        
        for lancamento in lancamentos:
            lancamento.status = 'Cancelado'
            lancamento.observacoes = f"{lancamento.observacoes or ''}\nCancelado - OS excluída em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        # Soft delete da OS
        ordem.ativo = False
        
        db.session.commit()
        
        flash(f'Ordem de serviço {ordem.codigo} excluída com sucesso!', 'success')
        return redirect(url_for('os.listar_os'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir ordem de serviço: {str(e)}', 'error')
        return redirect(url_for('os.visualizar_os', id=id))

# === GERAR PDF ===
@os_bp.route('/pdf/<int:id>')
def gerar_pdf(id):
    """Gerar PDF da ordem de serviço"""
    try:
        ordem = OrdemServico.query.get_or_404(id)
        
        # Parsear dados JSON
        servicos = []
        produtos = []
        parcelas = []
        
        if ordem.servicos_dados:
            try:
                servicos = json.loads(ordem.servicos_dados)
            except:
                pass
                
        if ordem.produtos_dados:
            try:
                produtos = json.loads(ordem.produtos_dados)
            except:
                pass
                
        if ordem.parcelas_json:
            try:
                parcelas = json.loads(ordem.parcelas_json)
            except:
                pass
        
        # Renderizar HTML para PDF
        html_content = render_template('pdf_template.html', 
                                     os=ordem, servicos=servicos, produtos=produtos, parcelas=parcelas)
        
        # Gerar PDF usando WeasyPrint
        import weasyprint
        pdf = weasyprint.HTML(string=html_content).write_pdf()
        
        # Retornar PDF
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename="OS_{ordem.codigo}.pdf"'
        
        return response
        
    except Exception as e:
        flash(f'Erro ao gerar PDF: {str(e)}', 'error')
        return redirect(url_for('os.visualizar_os', id=id))

# === TESTE FORMA DE PAGAMENTO ===
@os_bp.route('/teste-forma-pagamento')
def teste_forma_pagamento():
    """Rota de teste para verificar lógica de forma de pagamento"""
    try:
        resultado = []
        resultado.append("=== TESTE FORMA DE PAGAMENTO ===")
        resultado.append("")
        
        # Testar diferentes formas de pagamento
        formas_teste = [
            'Pago', 'pago', 'PAGO',
            'À vista', 'A vista', 'a vista',
            'Dinheiro', 'PIX', 'Cartão',
            'Parcelado', 'Pendente', 'A prazo',
            '', None
        ]
        
        resultado.append("Formas de pagamento que GERAM lançamentos:")
        for forma in formas_teste:
            forma_lower = (forma or '').lower()
            pode_lancar = forma_lower in ['pago', 'à vista', 'a vista', 'dinheiro', 'pix', 'cartão', 'cartao']
            if pode_lancar:
                resultado.append(f"  ✅ '{forma}' → Gera lançamento")
        
        resultado.append("")
        resultado.append("Formas de pagamento que NÃO geram lançamentos:")
        for forma in formas_teste:
            forma_lower = (forma or '').lower()
            pode_lancar = forma_lower in ['pago', 'à vista', 'a vista', 'dinheiro', 'pix', 'cartão', 'cartao']
            if not pode_lancar:
                resultado.append(f"  ❌ '{forma}' → Não gera lançamento")
        
        resultado.append("")
        resultado.append("=== ORDENS DE SERVIÇO NO SISTEMA ===")
        
        # Verificar OS existentes
        ordens = OrdemServico.query.filter(
            OrdemServico.ativo == True if hasattr(OrdemServico, 'ativo') else True
        ).all()
        
        for os in ordens:
            forma_pag = (os.forma_pagamento or '').lower()
            pode_lancar = forma_pag in ['pago', 'à vista', 'a vista', 'dinheiro', 'pix', 'cartão', 'cartao']
            
            lancamentos_ativos = LancamentoFinanceiro.query.filter(
                LancamentoFinanceiro.descricao.like(f'%{os.codigo}%'),
                ~LancamentoFinanceiro.status.in_(['Cancelado', 'Excluído'])
            ).count()
            
            resultado.append(f"")
            resultado.append(f"OS {os.codigo}:")
            resultado.append(f"  Status: {os.status}")
            resultado.append(f"  Forma Pagamento: '{os.forma_pagamento}'")
            resultado.append(f"  Pode gerar lançamento: {'✅ Sim' if pode_lancar else '❌ Não'}")
            resultado.append(f"  Lançamentos ativos: {lancamentos_ativos}")
        
        resultado.append("")
        resultado.append("=== REGRA DE NEGÓCIO ===")
        resultado.append("Para gerar lançamentos financeiros:")
        resultado.append("1. ✅ Status = 'Concluída' (serviço executado)")
        resultado.append("2. ✅ Forma pagamento indica pagamento efetivado")
        resultado.append("   - Aceitos: 'pago', 'à vista', 'dinheiro', 'pix', 'cartão'")
        resultado.append("   - Rejeitados: 'parcelado', 'pendente', 'a prazo', etc.")
        
        return "<br>".join(resultado)
        
    except Exception as e:
        import traceback
        return f"❌ Erro: {str(e)}<br><pre>{traceback.format_exc()}</pre>"
