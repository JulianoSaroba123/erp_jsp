from flask import Blueprint, render_template, request, jsonify, make_response
from extensoes import db
from app.ordem_servico.os_model import OrdemServico
from app.cliente.cliente_model import Cliente
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import joinedload
import json
import csv
import io

# Blueprint para relatórios
relatorio_bp = Blueprint('relatorio', __name__, 
                        url_prefix='/relatorios', 
                        template_folder='templates')

@relatorio_bp.route('/ordens-servico/<int:os_id>/export-pdf')
def export_os_individual_pdf(os_id):
    """
    Exporta um PDF de uma Ordem de Serviço individual no padrão visual ERP_JSP.
    Segue as diretrizes do README: código limpo, modular, comentado, seguro e com nomes descritivos.
    """
    try:
        # O gerador de PDF padronizado JSP não está disponível (pdf_generator.py não existe)
        return jsonify({'erro': 'Função de exportação PDF não implementada: pdf_generator.py não encontrado.'}), 501
    except Exception as e:
        print(f"Erro na exportação PDF individual: {str(e)}")
        return jsonify({'erro': str(e)}), 500
# relatorios/relatorio_routes.py

from flask import Blueprint, render_template, request, jsonify, make_response
from extensoes import db
from app.ordem_servico.os_model import OrdemServico
from app.cliente.cliente_model import Cliente
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import joinedload
import json
import csv
import io

# Blueprint para relatórios
relatorio_bp = Blueprint('relatorio', __name__, 
                        url_prefix='/relatorios', 
                        template_folder='templates')

@relatorio_bp.route('/')
def index_relatorios():
    """Página principal de relatórios"""
    return render_template('relatorios/index.html')

@relatorio_bp.route('/ordens-servico')
def relatorio_os():
    """Relatório de Ordens de Serviço"""
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim') 
        status = request.args.get('status')
        cliente_id = request.args.get('cliente_id')
        tecnico = request.args.get('tecnico')
        
        # Query base
        query = OrdemServico.query.options(joinedload(OrdemServico.cliente))
        
        # Aplicar filtros
        if data_inicio:
            query = query.filter(OrdemServico.data_emissao >= datetime.strptime(data_inicio, '%Y-%m-%d').date())
        
        if data_fim:
            query = query.filter(OrdemServico.data_emissao <= datetime.strptime(data_fim, '%Y-%m-%d').date())
            
        if status and status != 'todos':
            query = query.filter(OrdemServico.status == status)
            
        if cliente_id and cliente_id != 'todos':
            query = query.filter(OrdemServico.cliente_id == int(cliente_id))
            
        if tecnico:
            query = query.filter(OrdemServico.tecnico_responsavel.like(f'%{tecnico}%'))
        
        # Filtro por ativo
        query = query.filter((OrdemServico.ativo == True) | (OrdemServico.ativo.is_(None)))
        
        # Executar query
        ordens = query.order_by(OrdemServico.data_emissao.desc()).all()
        
        # Estatísticas
        total_os = len(ordens)
        valor_total = sum([float(os.valor_total) if os.valor_total else 0.0 for os in ordens])
        valor_medio = valor_total / total_os if total_os > 0 else 0.0
        
        # Estatísticas por status
        stats_status = {}
        for os in ordens:
            status = os.status or 'Sem Status'
            if status not in stats_status:
                stats_status[status] = {'count': 0, 'valor': 0.0}
            stats_status[status]['count'] += 1
            stats_status[status]['valor'] += float(os.valor_total) if os.valor_total else 0.0
        
        # Buscar clientes para o filtro
        clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
        
        return render_template('relatorios/ordens_servico.html',
                             ordens=ordens,
                             total_os=total_os,
                             valor_total=valor_total,
                             valor_medio=valor_medio,
                             stats_status=stats_status,
                             clientes=clientes,
                             filtros={
                                 'data_inicio': data_inicio,
                                 'data_fim': data_fim,
                                 'status': status,
                                 'cliente_id': cliente_id,
                                 'tecnico': tecnico
                             })
    
    except Exception as e:
        print(f"Erro no relatório de OS: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return render_template('relatorios/ordens_servico.html',
                             ordens=[],
                             total_os=0,
                             valor_total=0.0,
                             valor_medio=0.0,
                             stats_status={},
                             clientes=[],
                             filtros={})

@relatorio_bp.route('/ordens-servico/export')
def export_os_csv():
    """Exportar relatório de OS para CSV"""
    try:
        # Mesmos filtros do relatório
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim') 
        status = request.args.get('status')
        cliente_id = request.args.get('cliente_id')
        tecnico = request.args.get('tecnico')
        
        # Query base (mesma do relatório)
        query = OrdemServico.query.options(joinedload(OrdemServico.cliente))
        
        if data_inicio:
            query = query.filter(OrdemServico.data_emissao >= datetime.strptime(data_inicio, '%Y-%m-%d').date())
        if data_fim:
            query = query.filter(OrdemServico.data_emissao <= datetime.strptime(data_fim, '%Y-%m-%d').date())
        if status and status != 'todos':
            query = query.filter(OrdemServico.status == status)
        if cliente_id and cliente_id != 'todos':
            query = query.filter(OrdemServico.cliente_id == int(cliente_id))
        if tecnico:
            query = query.filter(OrdemServico.tecnico_responsavel.like(f'%{tecnico}%'))
        
        query = query.filter((OrdemServico.ativo == True) | (OrdemServico.ativo.is_(None)))
        ordens = query.order_by(OrdemServico.data_emissao.desc()).all()
        
        # Criar CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho
        writer.writerow([
            'Código', 'Cliente', 'Data Emissão', 'Status', 'Técnico',
            'Valor Serviços', 'Valor Produtos', 'Valor Total', 'Descrição Problema'
        ])
        
        # Dados
        for os in ordens:
            writer.writerow([
                os.codigo,
                os.cliente.nome if os.cliente else f'Cliente ID {os.cliente_id}',
                os.data_emissao.strftime('%d/%m/%Y') if os.data_emissao else '',
                os.status or '',
                os.tecnico_responsavel or '',
                f'R$ {os.valor_servicos:.2f}' if os.valor_servicos else 'R$ 0,00',
                f'R$ {os.valor_produtos:.2f}' if os.valor_produtos else 'R$ 0,00',
                f'R$ {os.valor_total:.2f}' if os.valor_total else 'R$ 0,00',
                os.descricao_problema or ''
            ])
        
        # Preparar resposta
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=relatorio_os_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
        
    except Exception as e:
        print(f"Erro na exportação: {str(e)}")
        return jsonify({'erro': str(e)}), 500

@relatorio_bp.route('/dashboard')
def dashboard():
    """Dashboard com resumo geral"""
    try:
        # Período padrão: últimos 30 dias
        data_fim = date.today()
        data_inicio = data_fim - timedelta(days=30)
        
        # OS no período
        ordens_periodo = OrdemServico.query.filter(
            and_(
                OrdemServico.data_emissao >= data_inicio,
                OrdemServico.data_emissao <= data_fim,
                or_(OrdemServico.ativo == True, OrdemServico.ativo.is_(None))
            )
        ).all()
        
        # Estatísticas gerais
        total_os = len(ordens_periodo)
        valor_total = sum([float(os.valor_total) if os.valor_total else 0.0 for os in ordens_periodo])
        
        # OS por status
        stats_status = {}
        for os in ordens_periodo:
            status = os.status or 'Sem Status'
            stats_status[status] = stats_status.get(status, 0) + 1
        
        # OS por cliente (top 5)
        stats_cliente = {}
        for os in ordens_periodo:
            cliente_nome = os.cliente.nome if os.cliente else f'Cliente ID {os.cliente_id}'
            if cliente_nome not in stats_cliente:
                stats_cliente[cliente_nome] = {'count': 0, 'valor': 0.0}
            stats_cliente[cliente_nome]['count'] += 1
            stats_cliente[cliente_nome]['valor'] += float(os.valor_total) if os.valor_total else 0.0
        
        # Ordenar por valor
        top_clientes = sorted(stats_cliente.items(), key=lambda x: x[1]['valor'], reverse=True)[:5]
        
        return render_template('relatorios/dashboard.html',
                             total_os=total_os,
                             valor_total=valor_total,
                             stats_status=stats_status,
                             top_clientes=top_clientes,
                             data_inicio=data_inicio,
                             data_fim=data_fim)
    
    except Exception as e:
        print(f"Erro no dashboard: {str(e)}")
        return render_template('relatorios/dashboard.html',
                             total_os=0,
                             valor_total=0.0,
                             stats_status={},
                             top_clientes=[],
                             data_inicio=date.today(),
                             data_fim=date.today())
@relatorio_bp.route('/ordens-servico/export-pdf')
def export_os_pdf():
    """Exportar relatório de OS para PDF com layout do modelo fornecido"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm, cm
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        import os

        # Filtros
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        status = request.args.get('status')
        cliente_id = request.args.get('cliente_id')
        tecnico = request.args.get('tecnico')

        # Query base (mesma do relatório)
        query = OrdemServico.query.options(joinedload(OrdemServico.cliente))
        if data_inicio:
            query = query.filter(OrdemServico.data_emissao >= datetime.strptime(data_inicio, '%Y-%m-%d').date())
        if data_fim:
            query = query.filter(OrdemServico.data_emissao <= datetime.strptime(data_fim, '%Y-%m-%d').date())
        if status and status != 'todos':
            query = query.filter(OrdemServico.status == status)
        if cliente_id and cliente_id != 'todos':
            query = query.filter(OrdemServico.cliente_id == int(cliente_id))
        if tecnico:
            query = query.filter(OrdemServico.tecnico_responsavel.like(f'%{tecnico}%'))
        query = query.filter((OrdemServico.ativo == True) | (OrdemServico.ativo.is_(None)))
        ordens = query.order_by(OrdemServico.data_emissao.desc()).all()

        # PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']
        styleH.alignment = TA_CENTER
        styleTitle = ParagraphStyle('title', parent=styleH, fontSize=16, alignment=TA_CENTER, spaceAfter=10)
        styleSection = ParagraphStyle('section', parent=styleN, fontSize=11, spaceAfter=6, spaceBefore=6, leftIndent=0)

        story = []

        # Cabeçalho com logo e título
        logo_path = os.path.join('static', 'logo.png')
        if os.path.exists(logo_path):
            story.append(Image(logo_path, width=60, height=60))
        story.append(Paragraph("<b>RELATÓRIO DE ORDENS DE SERVIÇO</b>", styleTitle))
        story.append(Spacer(1, 6))

        # Filtros usados
        filtros = []
        if data_inicio:
            filtros.append(f"<b>Data início:</b> {data_inicio}")
        if data_fim:
            filtros.append(f"<b>Data fim:</b> {data_fim}")
        if status and status != 'todos':
            filtros.append(f"<b>Status:</b> {status}")
        if cliente_id and cliente_id != 'todos':
            filtros.append(f"<b>Cliente ID:</b> {cliente_id}")
        if tecnico:
            filtros.append(f"<b>Técnico:</b> {tecnico}")
        if filtros:
            story.append(Paragraph(' | '.join(filtros), styleSection))
            story.append(Spacer(1, 6))

        # Tabela de OS
        data = [[
            'Código', 'Cliente', 'Data Emissão', 'Status', 'Técnico',
            'Valor Serviços', 'Valor Produtos', 'Valor Total', 'Descrição Problema']]
        for os in ordens:
            data.append([
                os.codigo,
                os.cliente.nome if os.cliente else f'Cliente ID {os.cliente_id}',
                os.data_emissao.strftime('%d/%m/%Y') if os.data_emissao else '',
                os.status or '',
                os.tecnico_responsavel or '',
                f'R$ {os.valor_servicos:.2f}' if os.valor_servicos else 'R$ 0,00',
                f'R$ {os.valor_produtos:.2f}' if os.valor_produtos else 'R$ 0,00',
                f'R$ {os.valor_total:.2f}' if os.valor_total else 'R$ 0,00',
                os.descricao_problema or ''
            ])

        table = Table(data, repeatRows=1, colWidths=[40, 90, 55, 45, 60, 55, 55, 55, 120])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e6e6e6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#222')),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#888')),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

        # Rodapé com data/hora e totalizadores
        total_servicos = sum([float(os.valor_servicos) if os.valor_servicos else 0.0 for os in ordens])
        total_produtos = sum([float(os.valor_produtos) if os.valor_produtos else 0.0 for os in ordens])
        total_geral = sum([float(os.valor_total) if os.valor_total else 0.0 for os in ordens])
        story.append(Paragraph(f"<b>Total Serviços:</b> R$ {total_servicos:.2f} &nbsp;&nbsp; <b>Total Produtos:</b> R$ {total_produtos:.2f} &nbsp;&nbsp; <b>Total Geral:</b> R$ {total_geral:.2f}", styleSection))
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"<font size=8>Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</font>", styles['Normal']))

        doc.build(story)
        buffer.seek(0)
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=relatorio_os_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        return response
    except Exception as e:
        print(f"Erro na exportação PDF: {str(e)}")
        return jsonify({'erro': str(e)}), 500
