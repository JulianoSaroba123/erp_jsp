from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from extensoes import db
from .os_model import OrdemServico
from .os_calculos import CalculadoraOS
from app.produto.produto_model import Produto
from app.servico.servico_model import Servico
from app.financeiro.financeiro_model import LancamentoFinanceiro
from datetime import datetime
from sqlalchemy.orm import joinedload
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file, abort, make_response
from extensoes import db
from .os_model import OrdemServico, OrdemServicoItem
from .arquivo_model import OSArquivo
from .os_calculos import CalculadoraOS
from .upload_utils import UploadManager, allowed_file
from .simple_pdf_generator import SimplePDFGenerator
from app.cliente.cliente_model import Cliente
from app.produto.produto_model import Produto
from app.servico.servico_model import Servico
from app.condicoes_pagamento.condicoes_pag_model import OSParcela
from datetime import datetime, date
import os
import tempfile


# Blueprint precisa ser definido após os imports

os_bp = Blueprint('os', __name__, url_prefix='/os')

# === NOVA ORDEM DE SERVIÇO (endpoint: os.nova_os) ===
@os_bp.route('/nova', methods=['GET', 'POST'], endpoint='nova_os')
def nova_os():
    """Exibe formulário e cria nova ordem de serviço (básico)"""
    if request.method == 'POST':
        try:
            dados_form = request.form.to_dict()
            # Validação mínima
            if not dados_form.get('cliente_id'):
                flash('Cliente é obrigatório', 'error')
                return redirect(url_for('os.nova_os'))
            if not dados_form.get('data_emissao'):
                flash('Data de emissão é obrigatória', 'error')
                return redirect(url_for('os.nova_os'))
            # Gerar código automático
            ultima_os = OrdemServico.query.order_by(OrdemServico.id.desc()).first()
            if ultima_os and ultima_os.codigo and ultima_os.codigo.startswith('OS'):
                try:
                    proximo_num = int(ultima_os.codigo[2:]) + 1
                    codigo = f'OS{proximo_num:04d}'
                except Exception:
                    codigo = 'OS0001'
            else:
                codigo = 'OS0001'

            ordem = OrdemServico(
                codigo=codigo,
                cliente_id=dados_form.get('cliente_id'),
                status=dados_form.get('status', 'Aberta'),
                prioridade=dados_form.get('prioridade', 'Normal'),
                tipo_servico=dados_form.get('tipo_servico', ''),
                solicitante=dados_form.get('solicitante'),
                contato=dados_form.get('contato'),
                data_emissao=datetime.strptime(dados_form.get('data_emissao'), '%Y-%m-%d').date() if dados_form.get('data_emissao') else None,
                previsao_conclusao=datetime.strptime(dados_form.get('previsao_conclusao'), '%Y-%m-%d').date() if dados_form.get('previsao_conclusao') else None,
                tecnico_responsavel=dados_form.get('tecnico_responsavel'),
                equipamento_nome=dados_form.get('equipamento_nome'),
                equipamento_marca=dados_form.get('equipamento_marca'),
                equipamento_modelo=dados_form.get('equipamento_modelo'),
                equipamento_numero_serie=dados_form.get('equipamento_numero_serie'),
                equipamento_acessorios=dados_form.get('equipamento_acessorios'),
                problema_descrito=dados_form.get('problema_descrito'),
                descricao_servico_realizado=dados_form.get('descricao_servico_realizado'),
                hora_inicio=datetime.strptime(dados_form.get('hora_inicio'), '%H:%M').time() if dados_form.get('hora_inicio') else None,
                hora_termino=datetime.strptime(dados_form.get('hora_termino'), '%H:%M').time() if dados_form.get('hora_termino') else None,
                km_inicial=float(dados_form.get('km_inicial')) if dados_form.get('km_inicial') else None,
                km_final=float(dados_form.get('km_final')) if dados_form.get('km_final') else None,
                condicoes_pagamento=dados_form.get('condicoes_pagamento', 'À vista'),
                outras_informacoes=dados_form.get('outras_informacoes'),
                ativo=True
            )
            db.session.add(ordem)
            db.session.commit()
            flash('Ordem de serviço criada com sucesso!', 'success')
            return redirect(url_for('os.listar_os'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar ordem de serviço: {str(e)}', 'error')
            import traceback
            print('ERRO AO CRIAR OS:', traceback.format_exc())
            return redirect(url_for('os.nova_os'))
    # GET: exibe o formulário (ajuste o template conforme seu projeto)
    from app.cliente.cliente_model import Cliente
    servicos = Servico.query.filter_by(ativo=True).all() if hasattr(Servico, 'ativo') else Servico.query.all()
    produtos = Produto.query.filter_by(ativo=True).all() if hasattr(Produto, 'ativo') else Produto.query.all()
    clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
    # Gerar código automático (exemplo simples)
    ultima_os = OrdemServico.query.order_by(OrdemServico.id.desc()).first()
    if ultima_os and ultima_os.codigo and ultima_os.codigo.startswith('OS'):
        try:
            proximo_num = int(ultima_os.codigo[2:]) + 1
            codigo_gerado = f'OS{proximo_num:04d}'
        except Exception:
            codigo_gerado = 'OS0001'
    else:
        codigo_gerado = 'OS0001'
    return render_template('ordem_servico/cadastro_new.html', servicos=servicos, produtos=produtos, clientes=clientes, codigo_gerado=codigo_gerado, ordem_servico=None)

# === LISTAGEM DE ORDENS DE SERVIÇO (endpoint: os.listar_os) ===

@os_bp.route('/', endpoint='listar_os')
def listar_os():
    """Lista todas as ordens de serviço (página principal do módulo OS)"""
    try:
        # 1) Filtrar apenas ordens ativas
        ordens = OrdemServico.query.filter_by(ativo=True).order_by(OrdemServico.id.desc()).all()
        print("DEBUG /os -> total ordens ativas:", len(ordens))

        # 2) Contadores robustos
        total_os = len(ordens)
        norm = lambda s: (s or '').strip()
        os_abertas    = sum(1 for o in ordens if norm(o.status) == 'Aberta')
        os_andamento  = sum(1 for o in ordens if norm(o.status) == 'Em Andamento')
        os_concluidas = sum(1 for o in ordens if norm(o.status) == 'Concluída')

        valor_total = 0.0
        for o in ordens:
            try: valor_total += float(o.valor_total or 0)
            except: pass
        valor_medio = (valor_total / total_os) if total_os else 0.0

        return render_template(
            'lista_os.html',
            ordens=ordens,
            total_os=total_os,
            os_abertas=os_abertas,
            os_andamento=os_andamento,
            os_concluidas=os_concluidas,
            valor_total=valor_total,
            valor_medio=valor_medio
        )
    except Exception as e:
        from flask import flash
        import traceback
        print("ERRO listar_os:", e)
        print(traceback.format_exc())
        flash(f'Erro ao carregar lista de OS: {e}', 'error')
        return render_template('lista_os.html',
            ordens=[], total_os=0, os_abertas=0, os_andamento=0,
            os_concluidas=0, valor_total=0.0, valor_medio=0.0)

# === ROTA DE DEBUG RÁPIDO ===
@os_bp.route('/_debug')
def os_debug():
    try:
        rows = OrdemServico.query.order_by(OrdemServico.id.desc()).all()
        payload = []
        for o in rows:
            payload.append({
                "id": o.id,
                "codigo": getattr(o, "codigo", None),
                "status": getattr(o, "status", None),
                "ativo": getattr(o, "ativo", None),
                "cliente_id": getattr(o, "cliente_id", None),
                "valor_total": float(getattr(o, "valor_total", 0) or 0),
            })
        return {"count": len(payload), "items": payload}, 200
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }, 500

# === DEBUG OS14 ===
@os_bp.route('/_debug/14')
def debug_os_14():
    try:
        os = OrdemServico.query.get(14)
        if not os:
            return {"error": "OS 14 não encontrada"}, 404
            
        debug_info = {
            "id": os.id,
            "codigo": os.codigo,
            "cliente": os.cliente.nome if os.cliente else None,
            "status": os.status,
            "valor_total": float(os.valor_total or 0),
            "valor_servicos": float(os.valor_servicos or 0),
            "valor_produtos": float(os.valor_produtos or 0),
            "total_horas": float(os.total_horas or 0),
            "hora_inicio": str(os.hora_inicio) if os.hora_inicio else None,
            "hora_termino": str(os.hora_termino) if os.hora_termino else None,
            "itens": [],
            "servicos": [],
            "produtos": []
        }
        
        # Calcular horas manualmente para debug
        if os.hora_inicio and os.hora_termino:
            inicio_str = os.hora_inicio.strftime('%H:%M')
            termino_str = os.hora_termino.strftime('%H:%M')
            inicio_parts = inicio_str.split(':')
            termino_parts = termino_str.split(':')
            inicio_minutos = (int(inicio_parts[0]) * 60) + int(inicio_parts[1])
            termino_minutos = (int(termino_parts[0]) * 60) + int(termino_parts[1])
            diff_minutos = termino_minutos - inicio_minutos
            horas_calculadas = diff_minutos / 60.0 if diff_minutos > 0 else 0
            debug_info["horas_calculadas"] = horas_calculadas
        
        # Verificar itens
        if hasattr(os, 'itens') and os.itens:
            for item in os.itens:
                debug_info["itens"].append({
                    "tipo": getattr(item, 'tipo_item', 'N/A'),
                    "descricao": getattr(item, 'descricao', 'N/A'),
                    "quantidade": float(getattr(item, 'quantidade', 0) or 0),
                    "valor_unitario": float(getattr(item, 'valor_unitario', 0) or 0),
                    "valor_total": float(getattr(item, 'valor_total', 0) or 0)
                })
        
        # Verificar serviços se existirem
        if hasattr(os, 'servicos'):
            for servico in os.servicos:
                debug_info["servicos"].append({
                    "nome": servico.nome,
                    "horas": float(servico.horas or 0),
                    "valor_por_hora": float(servico.valor_por_hora or 0),
                    "valor_total": float(servico.valor_total or 0)
                })
        
        # Verificar produtos se existirem
        if hasattr(os, 'produtos'):
            for produto in os.produtos:
                debug_info["produtos"].append({
                    "nome": produto.nome,
                    "quantidade": int(produto.quantidade or 0),
                    "valor_unitario": float(produto.valor_unitario or 0),
                    "valor_total": float(produto.valor_total or 0)
                })
                
        return debug_info, 200
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }, 500


# ------- VISUALIZAR OS (GET) Mostra a OS formatada -------
@os_bp.route('/<int:id>/visualizar', methods=['GET'], endpoint='visualizar_os')
def visualizar_os(id):
    """Visualiza a ordem de serviço em formato de relatório"""
    try:
        # Buscar OS com relacionamentos
        ordem = OrdemServico.query.options(
            joinedload(OrdemServico.cliente),
            joinedload(OrdemServico.itens)
        ).get_or_404(id)
        
        # Preparar dados dos serviços
        servicos_dados = []
        if hasattr(ordem, 'itens') and ordem.itens:
            for item in ordem.itens:
                if hasattr(item, 'tipo_item') and item.tipo_item == 'servico':
                    servicos_dados.append({
                        'nome': item.descricao or '',
                        'quantidade': float(item.quantidade or 0),
                        'valor_unitario': float(item.valor_unitario or 0),
                        'valor_total': float(item.valor_total or 0)
                    })
        
        # Preparar dados dos produtos
        produtos_dados = []
        if hasattr(ordem, 'itens') and ordem.itens:
            for item in ordem.itens:
                if hasattr(item, 'tipo_item') and item.tipo_item == 'produto':
                    produtos_dados.append({
                        'nome': item.descricao or '',
                        'quantidade': int(item.quantidade or 0),
                        'valor_unitario': float(item.valor_unitario or 0),
                        'valor_total': float(item.valor_total or 0)
                    })
        
        # Se não há itens detalhados, usar dados JSON salvos
        if not servicos_dados and ordem.servicos_dados:
            try:
                servicos_dados = json.loads(ordem.servicos_dados)
                # Garantir que cada serviço tenha valor_unitario
                for s in servicos_dados:
                    if 'valor_unitario' not in s:
                        quantidade = float(s.get('quantidade', 1) or 1)
                        valor_total = float(s.get('valor_total', 0) or 0)
                        s['valor_unitario'] = valor_total / quantidade if quantidade > 0 else 0
            except:
                servicos_dados = []
                
        if not produtos_dados and ordem.produtos_dados:
            try:
                produtos_dados = json.loads(ordem.produtos_dados)
                # Garantir que cada produto tenha valor_unitario
                for p in produtos_dados:
                    if 'valor_unitario' not in p:
                        quantidade = float(p.get('quantidade', 1) or 1)
                        valor_total = float(p.get('valor_total', 0) or 0)
                        p['valor_unitario'] = valor_total / quantidade if quantidade > 0 else 0
            except:
                produtos_dados = []
        
        # Preparar dados das parcelas
        parcelas = []
        if hasattr(ordem, 'parcelas_json') and ordem.parcelas_json:
            try:
                parcelas = json.loads(ordem.parcelas_json)
            except:
                parcelas = []
        
        # Calcular totais
        total_servicos = float(ordem.valor_servicos or 0)
        total_produtos = float(ordem.valor_produtos or 0)
        valor_total = float(ordem.valor_total or 0)
        
        return render_template(
            'os_visualizar.html',
            os=ordem,
            servicos_dados=servicos_dados,
            produtos_dados=produtos_dados,
            parcelas=parcelas,
            total_servicos=total_servicos,
            total_produtos=total_produtos,
            valor_total=valor_total
        )
        
    except Exception as e:
        flash(f'Erro ao visualizar OS: {e}', 'error')
        return redirect(url_for('os.listar_os'))

# ------- EDITAR OS (GET) Mostra o formulário com os dados da OS -------
@os_bp.route('/<int:id>/editar', methods=['GET'], endpoint='editar_os')
def editar_os(id):
    # Limpar mensagens flash antigas
    from flask import session
    if '_flashes' in session:
        session.pop('_flashes', None)
    
    ordem = OrdemServico.query.get_or_404(id)
    servicos_salvos = json.loads(ordem.servicos_dados) if ordem.servicos_dados else []
    produtos_salvos = json.loads(ordem.produtos_dados) if ordem.produtos_dados else []
    parcelas_salvas = json.loads(ordem.parcelas_json) if getattr(ordem, 'parcelas_json', None) else []
    servicos = Servico.query.filter_by(ativo=True).all() if hasattr(Servico,'ativo') else Servico.query.all()
    produtos = Produto.query.filter_by(ativo=True).all() if hasattr(Produto,'ativo') else Produto.query.all()
    try:
        clientes = Cliente.query.filter_by(ativo=True).all()
    except:
        clientes = Cliente.query.all()
    return render_template(
        'ordem_servico/cadastro_new.html',
        ordem_servico=ordem,
        clientes=clientes,
        servicos=servicos,
        produtos=produtos,
        codigo_gerado=ordem.codigo,
        servicos_salvos=servicos_salvos,
        produtos_salvos=produtos_salvos,
        parcelas_salvas=parcelas_salvas
    )

# ------- EDITAR OS (POST) atualização dos dados da OS -------
@os_bp.route('/<int:id>/editar', methods=['POST'])
def atualizar_os(id):
    try:
        ordem = OrdemServico.query.get_or_404(id)
        dados = request.form.to_dict()
        
        # Para edição, se não vier cliente_id, manter o existente
        if not dados.get('cliente_id') and ordem.cliente_id:
            dados['cliente_id'] = str(ordem.cliente_id)
        
        # Validar
        is_valid, erros = CalculadoraOS.validar_dados_os(dados)
        if not is_valid:
            for erro in erros:
                flash(erro, 'error')
            return redirect(url_for('os.editar_os', id=id))

        # JSONs
        servicos_data = json.loads(dados.get('servicos_json','[]') or '[]')
        produtos_data = json.loads(dados.get('produtos_json','[]') or '[]')
        parcelas_data = json.loads(dados.get('parcelas_json','[]') or '[]')

        # DEBUG: Log dos valores antes e depois dos cálculos
        print(f"=== DEBUG EDIÇÃO OS {id} ===")
        print(f"Valores ANTES da atualização:")
        print(f"  valor_servicos: {ordem.valor_servicos}")
        print(f"  valor_produtos: {ordem.valor_produtos}")
        print(f"  valor_total: {ordem.valor_total}")
        print(f"Dados recebidos do form:")
        print(f"  servicos_data: {servicos_data}")
        print(f"  produtos_data: {produtos_data}")

        calculos = CalculadoraOS.calcular_todos_valores(dados, servicos_data, produtos_data)
        
        print(f"Valores CALCULADOS:")
        print(f"  valor_servicos: {calculos['valor_servicos']}")
        print(f"  valor_produtos: {calculos['valor_produtos']}")
        print(f"  valor_total: {calculos['valor_total']}")
        print(f"=== FIM DEBUG ===")

        # Campos básicos
        ordem.cliente_id = dados.get('cliente_id')
        ordem.status = dados.get('status','Aberta')
        if dados.get('data_emissao'):
            ordem.data_emissao = datetime.strptime(dados['data_emissao'],'%Y-%m-%d').date()
        ordem.previsao_conclusao = datetime.strptime(dados['previsao_conclusao'],'%Y-%m-%d').date() if dados.get('previsao_conclusao') else None
        ordem.tecnico_responsavel = dados.get('tecnico_responsavel')

        # Equipamento
        ordem.equipamento_nome = dados.get('equipamento_nome')
        ordem.equipamento_marca = dados.get('equipamento_marca')
        ordem.equipamento_modelo = dados.get('equipamento_modelo')
        ordem.equipamento_numero_serie = dados.get('equipamento_numero_serie')
        ordem.equipamento_acessorios = dados.get('equipamento_acessorios')

        # Descrição
        ordem.problema_descrito = dados.get('problema_descrito')
        ordem.descricao_servico_realizado = dados.get('descricao_servico_realizado')

        # Horários
        ordem.hora_inicio = datetime.strptime(dados['hora_inicio'],'%H:%M').time() if dados.get('hora_inicio') else None
        ordem.hora_termino = datetime.strptime(dados['hora_termino'],'%H:%M').time() if dados.get('hora_termino') else None
        ordem.total_horas = calculos['total_horas']

        # KM / valores
        ordem.km_inicial = float(dados.get('km_inicial')) if dados.get('km_inicial') else None
        ordem.km_final = float(dados.get('km_final')) if dados.get('km_final') else None
        ordem.km_total = calculos['km_total']
        ordem.valor_deslocamento = calculos['valor_deslocamento']
        # Valores calculados - SEMPRE RECALCULAR
        ordem.valor_servicos = calculos['valor_servicos']
        ordem.valor_produtos = calculos['valor_produtos']
        ordem.valor_total = calculos['valor_total']

        # Pagamento - ATUALIZAR AUTOMATICAMENTE
        ordem.forma_pagamento = dados.get('forma_pagamento', 'À Vista')
        ordem.condicoes_pagamento = dados.get('condicoes_pagamento','À vista')
        # Atualizar data_vencimento se fornecida
        if dados.get('data_vencimento'):
            ordem.data_vencimento = datetime.strptime(dados['data_vencimento'],'%Y-%m-%d').date()
        ordem.parcelas_json = json.dumps(parcelas_data) if parcelas_data else None

        # Salva JSONs
        ordem.servicos_dados = json.dumps(servicos_data) if servicos_data else None
        ordem.produtos_dados = json.dumps(produtos_data) if produtos_data else None

        # *** FORÇA RECÁLCULO AUTOMÁTICO SEMPRE ***
        print(f"[FORÇA RECÁLCULO] Executando recálculo automático para OS {ordem.codigo}")
        ordem.recalcular_valores()
        print(f"[APÓS RECÁLCULO] OS {ordem.codigo}: Serviços={ordem.valor_servicos}, Total={ordem.valor_total}")

        # --- NOVO: Criar lançamentos financeiros se status for Concluída e forma_pagamento for de pagamento imediato ---
        status_atual = ordem.status
        forma_pag = (ordem.forma_pagamento or '').lower()
        pode_lancar = status_atual == 'Concluída' and forma_pag in ['pago', 'à vista', 'a vista', 'dinheiro', 'pix', 'cartão', 'cartao']
        if pode_lancar:
            from app.financeiro.financeiro_model import LancamentoFinanceiro
            lancamentos_existentes = LancamentoFinanceiro.query.filter(
                LancamentoFinanceiro.descricao.like(f'%{ordem.codigo}%'),
                ~LancamentoFinanceiro.status.in_(['Cancelado', 'Excluído'])
            ).count()
            if lancamentos_existentes == 0:
                try:
                    criar_lancamentos_financeiros(ordem)
                    # Marcar novos lançamentos como pagos
                    novos_lancamentos = LancamentoFinanceiro.query.filter(
                        LancamentoFinanceiro.descricao.like(f'%{ordem.codigo}%'),
                        LancamentoFinanceiro.status == 'Pendente'
                    ).all()
                    for lancamento in novos_lancamentos:
                        lancamento.status = 'Pago'
                except Exception as e:
                    print(f"DEBUG: Erro ao criar lançamentos financeiros em atualizar_os: {str(e)}")
                    flash(f'Erro ao criar lançamentos financeiros: {str(e)}', 'error')
        db.session.commit()
        flash(f'Ordem de Serviço {ordem.codigo} atualizada com sucesso!', 'success')
        return redirect(url_for('os.editar_os', id=ordem.id))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar ordem de serviço: {e}', 'error')
        return redirect(url_for('os.editar_os', id=id))



# === ROTAS DE DEBUG PARA BANCO DE DADOS ===
@os_bp.route('/debug/db')
def debug_db():
    """Testa conexão com o banco (SELECT 1)"""
    try:
        result = db.session.execute('SELECT 1').scalar()
        return {'success': True, 'result': result}, 200
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500

# === APIS PARA JS EM lista_os.html ===
@os_bp.route('/api/estatisticas')
def api_estatisticas():
    """API para estatísticas de OS (status, valores, etc)"""
    try:
        status = request.args.get('status')
        prioridade = request.args.get('prioridade')
        q = request.args.get('q')
        query = OrdemServico.query
        if status:
            query = query.filter(OrdemServico.status == status)
        if prioridade:
            query = query.filter(OrdemServico.prioridade == prioridade)
        if q:
            q_like = f"%{q}%"
            query = query.filter(
                (OrdemServico.codigo.ilike(q_like)) |
                (OrdemServico.status.ilike(q_like))
            )
        ordens = query.all()
        total_os = len(ordens)
        os_abertas = sum(1 for o in ordens if (o.status or '').strip() == 'Aberta')
        os_andamento = sum(1 for o in ordens if (o.status or '').strip() == 'Em Andamento')
        os_concluidas = sum(1 for o in ordens if (o.status or '').strip() == 'Concluída')
        valor_total = 0.0
        for o in ordens:
            try:
                valor_total += float(o.valor_total or 0)
            except Exception:
                pass
        valor_medio = (valor_total / total_os) if total_os else 0.0
        return jsonify({
            'success': True,
            'total_os': total_os,
            'os_abertas': os_abertas,
            'os_andamento': os_andamento,
            'os_concluidas': os_concluidas,
            'valor_total': valor_total,
            'valor_medio': valor_medio
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@os_bp.route('/api/lista')
def api_lista():
    """API para listar ordens de serviço (com filtros)"""
    try:
        status = request.args.get('status')
        prioridade = request.args.get('prioridade')
        q = request.args.get('q')
        query = OrdemServico.query
        if status:
            query = query.filter(OrdemServico.status == status)
        if prioridade:
            query = query.filter(OrdemServico.prioridade == prioridade)
        if q:
            q_like = f"%{q}%"
            query = query.filter(
                (OrdemServico.codigo.ilike(q_like)) |
                (OrdemServico.status.ilike(q_like))
            )
        ordens = query.order_by(OrdemServico.id.desc()).all()
        lista = []
        for o in ordens:
            lista.append({
                'id': o.id,
                'codigo': o.codigo,
                'status': o.status,
                'prioridade': getattr(o, 'prioridade', None),
                'valor_total': float(o.valor_total or 0),
                'cliente_id': o.cliente_id
            })
        return jsonify({'success': True, 'ordens': lista})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



@os_bp.route('/<int:id>/imprimir')
def imprimir_os(id):
    """Visualizar/Imprimir ordem de serviço"""
    try:
        ordem = OrdemServico.query.get_or_404(id)
        
        # Processar dados salvos para exibição
        servicos_salvos = []
        produtos_salvos = []
        parcelas_salvas = []
        
        try:
            if ordem.servicos_dados:
                servicos_salvos = json.loads(ordem.servicos_dados)
            if ordem.produtos_dados:
                produtos_salvos = json.loads(ordem.produtos_dados)
            if ordem.parcelas_json:
                parcelas_salvas = json.loads(ordem.parcelas_json)
        except (json.JSONDecodeError, TypeError):
            pass
        
        return render_template('imprimir_os.html',
                             ordem_servico=ordem,
                             servicos=servicos_salvos,
                             produtos=produtos_salvos,
                             parcelas=parcelas_salvas)
    
    except Exception as e:
        flash(f'Erro ao carregar ordem de serviço: {str(e)}', 'error')
        return redirect(url_for('.listar_os'))

@os_bp.route('/<int:id>/deletar', methods=['POST'], endpoint='deletar_os')
def deletar_os(id):
    """Deletar ordem de serviço (soft delete) e cancelar lançamentos financeiros"""
    try:
        print(f"DEBUG: Tentando excluir OS com ID: {id}")
        ordem = OrdemServico.query.get_or_404(id)
        print(f"DEBUG: OS encontrada: {ordem.codigo}")
        
        # Verificar se já está inativa
        if hasattr(ordem, 'ativo') and ordem.ativo == False:
            flash(f'Ordem de Serviço {ordem.codigo} já foi excluída!', 'warning')
            return redirect(url_for('os.listar_os'))
        
        # Cancelar lançamentos financeiros relacionados
        try:
            lancamentos = LancamentoFinanceiro.query.filter(
                LancamentoFinanceiro.descricao.like(f'%{ordem.codigo}%'),
                ~LancamentoFinanceiro.status.in_(['Cancelado', 'Excluído'])
            ).all()
            
            for lancamento in lancamentos:
                lancamento.status = 'Cancelado'
                lancamento.observacoes = (lancamento.observacoes or '') + f' [CANCELADO em {datetime.now().strftime("%d/%m/%Y %H:%M")} - OS excluída]'
            
            print(f"DEBUG: {len(lancamentos)} lançamentos cancelados para OS {ordem.codigo}")
            
        except Exception as e:
            print(f"DEBUG: Erro ao cancelar lançamentos: {e}")
        
        # Soft delete - marcar como inativo
        if hasattr(ordem, 'ativo'):
            ordem.ativo = False
        else:
            # Se não tem campo ativo, fazer delete real
            db.session.delete(ordem)
        
        db.session.commit()
        print(f"DEBUG: OS {ordem.codigo} excluída com sucesso")
        
        flash(f'Ordem de Serviço {ordem.codigo} excluída com sucesso!', 'success')
        return redirect(url_for('os.listar_os'))
    
    except Exception as e:
        print(f"DEBUG: Erro ao excluir OS: {str(e)}")
        db.session.rollback()
        flash(f'Erro ao excluir ordem de serviço: {str(e)}', 'error')
        return redirect(url_for('os.listar_os'))

@os_bp.route('/<int:id>/alterar-status', methods=['POST'], endpoint='alterar_status')
def alterar_status(id):
    """Alterar status da ordem de serviço e gerar lançamentos financeiros se concluída"""
    try:
        novo_status = request.form.get('status')
        ordem = OrdemServico.query.get_or_404(id)
        status_anterior = ordem.status
        
        print(f"DEBUG: Alterando status da OS {ordem.codigo} de '{status_anterior}' para '{novo_status}'")
        
        ordem.status = novo_status
        
        # Se marcou como concluída, verificar se pode criar lançamentos financeiros
        if novo_status == 'Concluída' and status_anterior != 'Concluída':
            print(f"DEBUG: OS {ordem.codigo} marcada como concluída")
            
            # Verificar se a forma de pagamento permite lançamento financeiro
            forma_pag = (ordem.forma_pagamento or '').lower()
            pode_lancar = forma_pag in ['pago', 'à vista', 'a vista', 'dinheiro', 'pix', 'cartão', 'cartao']
            
            print(f"DEBUG: Forma de pagamento: '{ordem.forma_pagamento}' - Pode lançar: {pode_lancar}")
            
            if pode_lancar:
                print(f"DEBUG: Criando lançamentos financeiros para OS {ordem.codigo}")
                try:
                    # Primeiro, verificar se existem lançamentos cancelados para reativar
                    lancamentos_cancelados = LancamentoFinanceiro.query.filter(
                        LancamentoFinanceiro.descricao.like(f'%{ordem.codigo}%'),
                        LancamentoFinanceiro.status.in_(['Cancelado', 'Excluído'])
                    ).all()
                    
                    if lancamentos_cancelados:
                        print(f"DEBUG: Reativando {len(lancamentos_cancelados)} lançamentos cancelados")
                        for lancamento in lancamentos_cancelados:
                            lancamento.status = 'Pago'  # Marca como pago pois forma_pagamento indica pagamento
                            lancamento.observacoes = (lancamento.observacoes or '') + f' [REATIVADO e PAGO em {datetime.now().strftime("%d/%m/%Y %H:%M")} - OS concluída e paga]'
                        print(f"DEBUG: Lançamentos reativados e marcados como pagos!")
                    else:
                        # Se não há lançamentos cancelados, criar novos
                        criar_lancamentos_financeiros(ordem)
                        # Marcar novos lançamentos como pagos
                        novos_lancamentos = LancamentoFinanceiro.query.filter(
                            LancamentoFinanceiro.descricao.like(f'%{ordem.codigo}%'),
                            LancamentoFinanceiro.status == 'Pendente'
                        ).all()
                        for lancamento in novos_lancamentos:
                            lancamento.status = 'Pago'
                        print(f"DEBUG: Novos lançamentos criados e marcados como pagos!")
                        
                except Exception as e:
                    print(f"DEBUG: Erro ao criar/reativar lançamentos: {str(e)}")
                    raise e
            else:
                print(f"DEBUG: Não criando lançamentos. Forma de pagamento '{ordem.forma_pagamento}' não indica pagamento efetivado.")
                flash(f'OS {ordem.codigo} concluída. Para registrar no financeiro, defina a forma de pagamento como "Pago".', 'info')
        else:
            print(f"DEBUG: Não criando lançamentos. Status: {novo_status}, Anterior: {status_anterior}")
        
        db.session.commit()
        flash(f'Status da OS {ordem.codigo} alterado para {novo_status}!', 'success')
        
    except Exception as e:
        print(f"DEBUG: Erro ao alterar status: {str(e)}")
        db.session.rollback()
        flash(f'Erro ao alterar status: {str(e)}', 'error')
    
    return redirect(url_for('os.listar_os'))

def criar_lancamentos_financeiros(ordem):
    """Criar lançamentos financeiros baseados nas parcelas da OS"""
    try:
        print(f"DEBUG: Iniciando criação de lançamentos financeiros para OS {ordem.codigo}")
        
        # Verificar se já existem lançamentos ATIVOS para esta OS
        # Exclui lançamentos com status 'Cancelado' ou 'Excluído'
        lancamentos_existentes = LancamentoFinanceiro.query.filter(
            LancamentoFinanceiro.descricao.like(f'%{ordem.codigo}%'),
            ~LancamentoFinanceiro.status.in_(['Cancelado', 'Excluído'])
        ).count()
        
        print(f"DEBUG: Lançamentos ativos encontrados: {lancamentos_existentes}")
        
        if lancamentos_existentes > 0:
            print(f"DEBUG: Já existem {lancamentos_existentes} lançamentos ativos para esta OS, pulando criação")
            return
        
        # Buscar parcelas da OS
        parcelas = []
        if ordem.parcelas_json:
            try:
                parcelas = json.loads(ordem.parcelas_json)
                print(f"DEBUG: Parcelas JSON parseadas: {len(parcelas)} parcelas")
            except Exception as e:
                print(f"DEBUG: Erro ao parsear parcelas JSON: {e}")
                parcelas = []
        else:
            print(f"DEBUG: Sem parcelas JSON na OS")
        
        if parcelas and len(parcelas) > 0:
            print(f"DEBUG: Processando {len(parcelas)} parcelas")
            # Parcelado - criar um lançamento para cada parcela
            for i, parcela in enumerate(parcelas):
                data_vencimento = parcela.get('data_vencimento') or parcela.get('vencimento')
                valor = float(parcela.get('valor', 0))
                
                print(f"DEBUG: Parcela {i+1}: R$ {valor} - Data: {data_vencimento}")
                
                # Converter data se necessário
                if isinstance(data_vencimento, str):
                    if '-' in data_vencimento:
                        data_vencimento = datetime.strptime(data_vencimento.split('T')[0], '%Y-%m-%d').date()
                    else:
                        data_vencimento = datetime.today().date()
                elif not data_vencimento:
                    data_vencimento = datetime.today().date()
                
                lancamento = LancamentoFinanceiro(
                    tipo='Receita',
                    categoria='Serviços',
                    descricao=f'OS {ordem.codigo} - Parcela {i+1}/{len(parcelas)} - {ordem.cliente.nome if ordem.cliente else "Cliente"}',
                    valor=valor,
                    data=data_vencimento,
                    status='Pendente',
                    observacoes=f'Gerado automaticamente da OS {ordem.codigo}'
                )
                db.session.add(lancamento)
                print(f"DEBUG: Adicionado lançamento parcela {i+1}: R$ {valor:.2f} para {data_vencimento}")
        else:
            print(f"DEBUG: Criando lançamento à vista")
            # À vista - criar um lançamento único
            valor_total = float(ordem.valor_total or 0)
            data_vencimento = ordem.data_vencimento or datetime.today().date()
            
            print(f"DEBUG: Valor total: R$ {valor_total}, Data: {data_vencimento}")
            
            lancamento = LancamentoFinanceiro(
                tipo='Receita',
                categoria='Serviços',
                descricao=f'OS {ordem.codigo} - À Vista - {ordem.cliente.nome if ordem.cliente else "Cliente"}',
                valor=valor_total,
                data=data_vencimento,
                status='Pendente',
                observacoes=f'Gerado automaticamente da OS {ordem.codigo}'
            )
            db.session.add(lancamento)
            print(f"DEBUG: Adicionado lançamento à vista: R$ {valor_total:.2f} para {data_vencimento}")
        
        # Não fazer commit aqui, deixar para a função que chama
        print(f"DEBUG: Lançamentos financeiros preparados para OS {ordem.codigo}")
        
    except Exception as e:
        print(f"DEBUG: Erro ao criar lançamentos financeiros: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise e

# APIs para AJAX
@os_bp.route('/api/calcular', methods=['POST'])
def api_calcular():
    """API para calcular valores em tempo real"""
    try:
        dados = request.get_json()
        
        # Extrair dados dos arrays
        servicos_data = dados.get('servicos', [])
        produtos_data = dados.get('produtos', [])
        dados_form = dados.get('form_data', {})
        
        # Calcular valores
        calculos = CalculadoraOS.calcular_todos_valores(
            dados_form, 
            servicos_data, 
            produtos_data
        )
        
        return jsonify({
            'success': True,
            'calculos': calculos
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@os_bp.route('/teste-financeiro-os14')
def teste_financeiro_os14():
    """Rota de teste para verificar integração financeira da OS0014"""
    try:
        # Buscar OS0014
        os = OrdemServico.query.filter_by(codigo='OS0014').first()
        if not os:
            return f"❌ OS0014 não encontrada!"
        
        resultado = []
        resultado.append(f"✅ OS encontrada: {os.codigo}")
        resultado.append(f"Status: {os.status}")
        resultado.append(f"Valor: R$ {os.valor_total}")
        resultado.append(f"Cliente: {os.cliente.nome if os.cliente else 'N/A'}")
        
        # Verificar lançamentos existentes
        lancamentos = LancamentoFinanceiro.query.filter(
            LancamentoFinanceiro.descricao.like(f'%{os.codigo}%')
        ).all()
        
        resultado.append(f"\n📊 Lançamentos existentes: {len(lancamentos)}")
        for lanc in lancamentos:
            resultado.append(f"- {lanc.descricao}: R$ {lanc.valor:.2f}")
        
        # Se não tem lançamentos, criar agora
        if len(lancamentos) == 0:
            resultado.append(f"\n🔧 Criando lançamentos...")
            
            # Criar lançamento à vista
            valor_total = float(os.valor_total or 0)
            lancamento = LancamentoFinanceiro(
                tipo='Receita',
                categoria='Serviços',
                descricao=f'{os.codigo} - À Vista - {os.cliente.nome if os.cliente else "Cliente"}',
                valor=valor_total,
                data=datetime.today().date(),
                status='Pendente',
                observacoes=f'Gerado automaticamente da {os.codigo}'
            )
            db.session.add(lancamento)
            db.session.commit()
            
            resultado.append(f"✅ Lançamento criado: R$ {valor_total:.2f}")
        
        return "<br>".join(resultado)
        
    except Exception as e:
        import traceback
        return f"❌ Erro: {str(e)}<br><pre>{traceback.format_exc()}</pre>"

@os_bp.route('/teste-valores-servicos-os14')
def teste_valores_servicos_os14():
    """Rota de teste para verificar valores dos serviços da OS0014"""
    try:
        # Buscar OS0014
        os = OrdemServico.query.filter_by(codigo='OS0014').first()
        if not os:
            return f"❌ OS0014 não encontrada!"
        
        resultado = []
        resultado.append(f"=== VALORES DA OS {os.codigo} ===")
        resultado.append(f"Valor Total: R$ {os.valor_total or 0}")
        resultado.append(f"Valor Serviços: R$ {os.valor_servicos or 0}")
        resultado.append(f"Total Horas: {os.total_horas or 0}h")
        
        # Calcular valor por hora
        if os.total_horas and os.total_horas > 0:
            valor_por_hora = (os.valor_servicos or 0) / os.total_horas
            resultado.append(f"Valor por Hora: R$ {valor_por_hora:.2f}")
        else:
            resultado.append(f"Valor por Hora: Não calculável (sem horas)")
        
        # Verificar relacionamento com serviço
        if os.servico:
            resultado.append(f"\nServiço Relacionado: {os.servico.nome}")
            resultado.append(f"Valor do Serviço no Cadastro: R$ {os.servico.valor}")
        else:
            resultado.append(f"\nNenhum serviço relacionado")
        
        # Verificar dados JSON
        if os.servicos_dados:
            resultado.append(f"\nDados JSON dos Serviços:")
            try:
                import json
                servicos = json.loads(os.servicos_dados)
                for i, s in enumerate(servicos):
                    resultado.append(f"  Serviço {i+1}: {s}")
            except Exception as e:
                resultado.append(f"  Erro ao parsear JSON: {e}")
        else:
            resultado.append(f"\nSem dados JSON de serviços")
        
        resultado.append(f"\n=== SIMULAÇÃO TEMPLATE ===")
        
        # Simular cálculo do template
        horas = os.total_horas or 0
        valor_servicos = os.valor_servicos or 0
        
        if horas > 0:
            valor_unitario = valor_servicos / horas
            resultado.append(f"Template mostrará: R$ {valor_unitario:.2f} por hora")
        elif os.servico:
            resultado.append(f"Template mostrará: R$ {os.servico.valor:.2f} (valor do cadastro)")
        else:
            resultado.append(f"Template mostrará: R$ 0.00")
        
        return "<br>".join(resultado)
        
    except Exception as e:
        import traceback
        return f"❌ Erro: {str(e)}<br><pre>{traceback.format_exc()}</pre>"
    """Rota de teste para simular mudança de status da OS0014"""
    try:
        # Buscar OS0014
        os = OrdemServico.query.filter_by(codigo='OS0014').first()
        if not os:
            return f"❌ OS0014 não encontrada!"
        
        resultado = []
        resultado.append(f"✅ OS encontrada: {os.codigo}")
        resultado.append(f"Status atual: {os.status}")
        
        # Primeiro mudar para Em Andamento
        if os.status == 'Concluída':
            os.status = 'Em Andamento'
            db.session.commit()
            resultado.append(f"⚠️ Status alterado para: {os.status}")
        
        # Agora simular mudança para Concluída
        status_anterior = os.status
        os.status = 'Concluída'
        
        resultado.append(f"\n🔄 Simulando mudança de '{status_anterior}' para 'Concluída'")
        
        # Chamar função criar_lancamentos_financeiros
        try:
            criar_lancamentos_financeiros(os)
            resultado.append(f"✅ Função criar_lancamentos_financeiros executada")
        except Exception as e:
            resultado.append(f"❌ Erro na função: {str(e)}")
            import traceback
            resultado.append(f"<pre>{traceback.format_exc()}</pre>")
        
        db.session.commit()
        resultado.append(f"💾 Status salvo: {os.status}")
        
        # Verificar lançamentos após
        lancamentos = LancamentoFinanceiro.query.filter(
            LancamentoFinanceiro.descricao.like(f'%{os.codigo}%')
        ).all()
        
        resultado.append(f"\n📊 Lançamentos após teste: {len(lancamentos)}")
        for lanc in lancamentos:
            resultado.append(f"- {lanc.descricao}: R$ {lanc.valor:.2f}")
        
        return "<br>".join(resultado)
        
    except Exception as e:
        import traceback
        return f"❌ Erro: {str(e)}<br><pre>{traceback.format_exc()}</pre>"






# === RELATÓRIO HTML JSP ===
@os_bp.route('/<int:os_id>/relatorio')
def relatorio_os(os_id):
    """Visualiza o relatório da OS em HTML (padrão JSP)"""
    ordem = OrdemServico.query.options(
        joinedload(OrdemServico.cliente),
        joinedload(OrdemServico.itens)
    ).get_or_404(os_id)

    servicos_dados = []
    produtos_dados = []
    parcelas = []
    try:
        if ordem.servicos_dados:
            servicos_dados = json.loads(ordem.servicos_dados)
        if ordem.produtos_dados:
            produtos_dados = json.loads(ordem.produtos_dados)
        if ordem.parcelas_json:
            parcelas = json.loads(ordem.parcelas_json)

    except Exception:
        pass




# ===== ROTAS PARA GERENCIAMENTO DE ARQUIVOS =====


@os_bp.route('/<int:os_id>/upload', methods=['POST'])
def upload_arquivo(os_id):
    """Upload de arquivo para uma OS"""
    try:
        # Verificar se a OS existe
        os = OrdemServico.query.get_or_404(os_id)
        
        # Verificar se há arquivo no request
        if 'arquivo' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo foi enviado'
            }), 400
        
        file = request.files['arquivo']
        categoria = request.form.get('categoria', 'documento')
        descricao = request.form.get('descricao', '')
        
        # Validar arquivo
        upload_manager = UploadManager()
        errors = upload_manager.validate_file(file)
        
        if errors:
            return jsonify({
                'success': False,
                'error': '; '.join(errors)
            }, 400)
        
        # Salvar arquivo localmente
        resultado = upload_manager.save_file_local(file, os_id, categoria)
        
        if not resultado['success']:
            return jsonify({
                'success': False,
                'error': resultado['error']
            }, 500)
        
        # Criar registro no banco
        arquivo = OSArquivo(
            ordem_servico_id=os_id,
            nome_original=file.filename,
            nome_arquivo=resultado['nome_arquivo'],
            tipo_arquivo=resultado['tipo_arquivo'],
            tamanho=resultado['tamanho'],
            categoria=categoria,
            descricao=descricao,
            caminho_local=resultado['caminho_local'],
            url_publica=resultado['url_relativa'],
            usuario_upload='Sistema'  # TODO: Implementar autenticação
        )
        
        db.session.add(arquivo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Arquivo enviado com sucesso',
            'arquivo': arquivo.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@os_bp.route('/arquivo/<int:arquivo_id>')
def visualizar_arquivo(arquivo_id):
    """Visualizar arquivo"""
    try:
        arquivo = OSArquivo.query.get_or_404(arquivo_id)
        
        # Verificar se arquivo existe fisicamente
        if arquivo.caminho_local and os.path.exists(arquivo.caminho_local):
            return send_file(
                arquivo.caminho_local,
                as_attachment=False,
                download_name=arquivo.nome_original
            )
        elif arquivo.url_s3:
            # Redirecionar para URL do S3
            return redirect(arquivo.url_s3)
        else:
            abort(404, "Arquivo não encontrado")
    
    except Exception as e:
        abort(500, f"Erro ao acessar arquivo: {str(e)}")

@os_bp.route('/arquivo/<int:arquivo_id>/download')
def download_arquivo(arquivo_id):
    """Download de arquivo"""
    try:
        arquivo = OSArquivo.query.get_or_404(arquivo_id)
        
        # Verificar se arquivo existe fisicamente
        if arquivo.caminho_local and os.path.exists(arquivo.caminho_local):
            return send_file(
                arquivo.caminho_local,
                as_attachment=True,
                download_name=arquivo.nome_original
            )
        elif arquivo.url_s3:
            # Redirecionar para URL do S3
            return redirect(arquivo.url_s3)
        else:
            abort(404, "Arquivo não encontrado")
    
    except Exception as e:
        abort(500, f"Erro ao baixar arquivo: {str(e)}")

@os_bp.route('/arquivo/<int:arquivo_id>/excluir', methods=['POST'])
def excluir_arquivo(arquivo_id):
    """Excluir arquivo"""
    try:
        arquivo = OSArquivo.query.get_or_404(arquivo_id)
        os_id = arquivo.ordem_servico_id
        
        # Remover arquivo físico
        upload_manager = UploadManager()
        if arquivo.caminho_local:
            upload_manager.delete_file_local(arquivo.caminho_local)
        
        # Marcar como inativo no banco (soft delete)
        arquivo.ativo = False
        db.session.commit()
        
        flash('Arquivo excluído com sucesso', 'success')
        
        # Se for requisição AJAX
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Arquivo excluído com sucesso'
            })
        
        return redirect(url_for('os.gerenciar_arquivos', os_id=os_id))
    
    except Exception as e:
        db.session.rollback()
        
        if request.is_json:
            return jsonify({
                'success': False,
                'error': str(e)
            }, 500)
        
        flash(f'Erro ao excluir arquivo: {str(e)}', 'error')
        return redirect(url_for('os.gerenciar_arquivos', os_id=arquivo.ordem_servico_id))

@os_bp.route('/<int:os_id>/arquivos/api')
def api_arquivos(os_id):
    """API para listar arquivos de uma OS (para AJAX)"""
    try:
        arquivos = OSArquivo.query.filter_by(
            ordem_servico_id=os_id,
            ativo=True
        ).order_by(OSArquivo.data_upload.desc()).all()
        
        return jsonify({
            'success': True,
            'arquivos': [arquivo.to_dict() for arquivo in arquivos]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ===== ROTAS PARA GERAÇÃO DE PDF =====

@os_bp.route('/<int:os_id>/pdf')
def gerar_pdf(os_id):
    """Gera PDF da ordem de serviço com template JSP ELÉTRICA"""
    try:
        print(f"=== GERANDO PDF PARA OS ID: {os_id} ===")
        
        # Buscar OS com relacionamentos
        os = OrdemServico.query.options(
            joinedload(OrdemServico.cliente),
            joinedload(OrdemServico.itens),
            joinedload(OrdemServico.arquivos)
        ).get_or_404(os_id)
        
        print(f"OS encontrada: {os.codigo}")
        print(f"Cliente: {os.cliente.nome if os.cliente else 'Sem cliente'}")
        print(f"Itens: {len(os.itens) if os.itens else 0}")
        
        # Gerar PDF com template JSP completo
        print("Importando SimplePDFGenerator...")
        
        print("Criando instância do gerador...")
        pdf_generator = SimplePDFGenerator()
        
        print("Gerando PDF com template JSP...")
        pdf_bytes = pdf_generator.generate_pdf(os)
        
        print(f"PDF gerado com sucesso! Tamanho: {len(pdf_bytes)} bytes")
        
        # Criar resposta com PDF
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename="OS_{os.codigo}_JSP_ELETRICA.pdf"'
        
        print("Retornando PDF...")
        return response
    
    except Exception as e:
        print(f"ERRO ao gerar PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Em caso de erro, tentar PDF simples como fallback
        try:
            print("Tentando PDF simples como fallback...")
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from io import BytesIO
            
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            
            # Cabeçalho de erro
            p.drawString(100, 750, f"JSP ELÉTRICA - Ordem de Serviço {os.codigo}")
            p.drawString(100, 720, f"ERRO: Não foi possível gerar o template completo")
            p.drawString(100, 690, f"Cliente: {os.cliente.nome if os.cliente else 'N/A'}")
            p.drawString(100, 660, f"Data: {os.data_emissao.strftime('%d/%m/%Y') if os.data_emissao else 'N/A'}")
            p.drawString(100, 630, f"Erro: {str(e)}")
            
            p.save()
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            response = make_response(pdf_bytes)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'inline; filename="OS_{os.codigo}_ERROR.pdf"'
            
            return response
            
        except Exception as fallback_error:
            print(f"ERRO no fallback: {str(fallback_error)}")
            flash(f'Erro ao gerar PDF: {str(e)}', 'error')
            return redirect(url_for('os.listar_os'))

@os_bp.route('/<int:os_id>/pdf/download')
def download_pdf(os_id):
    """Download do PDF da ordem de serviço"""
    try:
        # Buscar OS com relacionamentos
        os = OrdemServico.query.options(
            joinedload(OrdemServico.cliente),
            joinedload(OrdemServico.itens),
            joinedload(OrdemServico.arquivos)
        ).get_or_404(os_id)
        
        # Gerar PDF
        pdf_generator = SimplePDFGenerator()
        pdf_bytes = pdf_generator.generate_pdf(os)
        
        # Criar resposta para download
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="Ordem_de_servico_{os.codigo}_{os.cliente.nome if os.cliente else "sem_cliente"}.pdf"'
        
        return response
    
    except Exception as e:
        flash(f'Erro ao baixar PDF: {str(e)}', 'error')
        return redirect(url_for('os.listar_os'))


@os_bp.route('/test-pdf-jsp')
def test_pdf_jsp():
    """Rota para testar o PDF com template JSP"""
    try:
        # Teste de imports primeiro
        
        # Criar mock da OS para teste
        class MockCliente:
            def __init__(self):
                self.nome = "EMPRESA EXEMPLO LTDA"
                self.cpf_cnpj = "29.256.846/0001-59"
                self.telefone = "(11) 98765-4321"
                self.email = "contato@empresa.com.br"
                self.endereco = "RUA DAS FLORES, 123 - SÃO PAULO - SP"

        class MockItem:
            def __init__(self, descricao, quantidade, valor_unitario, valor_total, tipo_item):
                self.descricao = descricao
                self.quantidade = quantidade
                self.valor_unitario = valor_unitario
                self.valor_total = valor_total
                self.tipo_item = tipo_item

        class MockOS:
            def __init__(self):
                self.codigo = "OS-2024001"
                self.numero = "2024001"
                self.data_abertura = datetime.now()
                self.data_conclusao = datetime.now()
                self.status = "Concluída"
                
                # Cliente
                self.cliente = MockCliente()
                
                # Equipamento
                self.equipamento_nome = "Calandra 01"
                self.equipamento_marca = "Mirandópolis"
                self.equipamento_modelo = "CC440"
                self.equipamento_numero_serie = "123456789"
                self.equipamento_acessorios = "Rolos extras, Suporte"
                
                # Técnico
                self.responsavel_tecnico = "Carlos Santos - Técnico Eletrônico"
                self.problema_relatado = "Equipamento apresentando ruído excessivo"
                self.problema_encontrado = "Rolamentos desgastados"
                self.solucao = "Substituição dos rolamentos"
                self.observacoes = "Manutenção preventiva recomendada"
                self.tipo_servico = "Manutenção Preventiva"
                self.total_horas = 4.0
                self.tecnico_responsavel = "Carlos Santos"
                
                # Valores
                self.valor_servicos = 450.00
                self.valor_produtos = 280.00
                self.valor_mao_obra = 150.00
                self.valor_deslocamento = 50.00
                self.valor_descontos = 30.00
                self.valor_total = 900.00
                
                # Listas
                self.arquivos = []
                self.servicos = [
                    MockItem("Limpeza geral do equipamento", 1, 100.00, 100.00, "servico"),
                    MockItem("Substituição de rolamentos", 1, 200.00, 200.00, "servico")
                ]
                self.itens = [
                    MockItem("Rolamento SKF 6205", 2, 85.00, 170.00, "produto"),
                    MockItem("Filtro de ar", 1, 45.00, 45.00, "produto")
                ]

        # Criar mock e gerar PDF
        os_mock = MockOS()
        pdf_generator = SimplePDFGenerator()
        pdf_bytes = pdf_generator.generate_pdf(os_mock)
        
        # Retornar PDF
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=teste_jsp_template.pdf'
        
        return response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Erro ao gerar PDF de teste:<br><pre>{error_details}</pre>", 500

@os_bp.route('/teste-reativacao-lancamentos')
def teste_reativacao_lancamentos():
    """Rota de teste para verificar reativação de lançamentos financeiros"""
    try:
        resultado = []
        resultado.append("=== TESTE DE REATIVAÇÃO DE LANÇAMENTOS ===")
        
        # Verificar todas as OS
        ordens = OrdemServico.query.all()
        resultado.append(f"Total de ordens no sistema: {len(ordens)}")
        
        for os in ordens:
            if hasattr(os, 'ativo') and not os.ativo:
                continue  # Pular OS inativas
                
            # Verificar lançamentos da OS
            lancamentos_ativos = LancamentoFinanceiro.query.filter(
                LancamentoFinanceiro.descricao.like(f'%{os.codigo}%'),
                ~LancamentoFinanceiro.status.in_(['Cancelado', 'Excluído'])
            ).count()
            
            lancamentos_cancelados = LancamentoFinanceiro.query.filter(
                LancamentoFinanceiro.descricao.like(f'%{os.codigo}%'),
                LancamentoFinanceiro.status.in_(['Cancelado', 'Excluído'])
            ).count()
            
            if lancamentos_ativos > 0 or lancamentos_cancelados > 0:
                resultado.append(f"")
                resultado.append(f"OS {os.codigo} (Status: {os.status}):")
                resultado.append(f"  - Lançamentos ativos: {lancamentos_ativos}")
                resultado.append(f"  - Lançamentos cancelados: {lancamentos_cancelados}")
        
        resultado.append(f"")
        resultado.append("=== COMO TESTAR ===")
        resultado.append("1. Marque uma OS como 'Concluída' (cria lançamentos)")
        resultado.append("2. Exclua a OS (cancela lançamentos)")
        resultado.append("3. Marque a OS como 'Concluída' novamente (reativa lançamentos)")
        
        return "<br>".join(resultado)
        
    except Exception as e:
        import traceback
        return f"❌ Erro: {str(e)}<br><pre>{traceback.format_exc()}</pre>"

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
