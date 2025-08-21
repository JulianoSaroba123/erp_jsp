from flask import Blueprint, render_template
from app.ordem_servico.simple_pdf_generator import SimplePDFGenerator
from app.ordem_servico.os_model import OrdemServico
from sqlalchemy.orm import joinedload

# Blueprint para testes
test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/debug-template/<int:os_id>')
def debug_template(os_id):
    """Debug completo dos valores passados para o template"""
    try:
        # Buscar OS
        os = OrdemServico.query.options(
            joinedload(OrdemServico.cliente),
            joinedload(OrdemServico.itens),
            joinedload(OrdemServico.arquivos)
        ).get_or_404(os_id)
        
        # Preparar contexto
        pdf_generator = SimplePDFGenerator()
        context = pdf_generator._prepare_context(os)
        
        # Renderizar template de debug
        debug_html = f"""
        <h1>Debug Template - OS {os_id}</h1>
        
        <h2>Valores no Context:</h2>
        <ul>
            <li>total_servicos: {context.get('total_servicos', 'N/A')}</li>
            <li>total_produtos: {context.get('total_produtos', 'N/A')}</li>
            <li>valor_total: {context.get('valor_total', 'N/A')}</li>
            <li>servicos_dados: {len(context.get('servicos_dados', []))} itens</li>
            <li>produtos_dados: {len(context.get('produtos_dados', []))} itens</li>
        </ul>
        
        <h2>Valores diretos da OS:</h2>
        <ul>
            <li>os.valor_total: {getattr(os, 'valor_total', 'N/A')}</li>
            <li>os.valor_servicos: {getattr(os, 'valor_servicos', 'N/A')}</li>
            <li>os.valor_produtos: {getattr(os, 'valor_produtos', 'N/A')}</li>
            <li>os.total_horas: {getattr(os, 'total_horas', 'N/A')}</li>
        </ul>
        
        <h2>Template renderizado:</h2>
        <p>No template, o valor será: R$ {context.get('valor_total', 0):.2f}</p>
        
        <h3>Links:</h3>
        <p><a href="/test/pdf-preview/{os_id}">Ver PDF Preview</a></p>
        <p><a href="/test/compare-values/{os_id}">Comparar Valores</a></p>
        """
        
        return debug_html
        
    except Exception as e:
        return f"Erro: {e}"
    """Comparar valores diretos do banco vs processados pelo PDF"""
    try:
        # Buscar OS
        os = OrdemServico.query.options(
            joinedload(OrdemServico.cliente),
            joinedload(OrdemServico.itens),
            joinedload(OrdemServico.arquivos)
        ).get_or_404(os_id)
        
        # Valores diretos do banco
        valores_banco = {
            'valor_total': float(getattr(os, 'valor_total', 0) or 0),
            'valor_servicos': float(getattr(os, 'valor_servicos', 0) or 0),
            'valor_produtos': float(getattr(os, 'valor_produtos', 0) or 0),
            'total_horas': float(getattr(os, 'total_horas', 0) or 0)
        }
        
        # Valores processados pelo gerador PDF
        pdf_generator = SimplePDFGenerator()
        context = pdf_generator._prepare_context(os)
        valores_pdf = {
            'valor_total': context.get('valor_total', 0),
            'total_servicos': context.get('total_servicos', 0),
            'total_produtos': context.get('total_produtos', 0)
        }
        
        # Montar resultado
        resultado = f"""
        <h1>Comparação de Valores - OS {os_id}</h1>
        
        <h2>Valores diretos do banco:</h2>
        <ul>
            <li>Valor Total: R$ {valores_banco['valor_total']:.2f}</li>
            <li>Valor Serviços: R$ {valores_banco['valor_servicos']:.2f}</li>
            <li>Valor Produtos: R$ {valores_banco['valor_produtos']:.2f}</li>
            <li>Total Horas: {valores_banco['total_horas']:.2f}</li>
        </ul>
        
        <h2>Valores processados para PDF:</h2>
        <ul>
            <li>Valor Total: R$ {valores_pdf['valor_total']:.2f}</li>
            <li>Total Serviços: R$ {valores_pdf['total_servicos']:.2f}</li>
            <li>Total Produtos: R$ {valores_pdf['total_produtos']:.2f}</li>
        </ul>
        
        <h2>Diferenças:</h2>
        <ul>
            <li>Valor Total: {'✅ OK' if abs(valores_banco['valor_total'] - valores_pdf['valor_total']) < 0.01 else f'❌ Diferença: {valores_banco["valor_total"] - valores_pdf["valor_total"]:.2f}'}</li>
            <li>Serviços: {'✅ OK' if abs(valores_banco['valor_servicos'] - valores_pdf['total_servicos']) < 0.01 else f'❌ Diferença: {valores_banco["valor_servicos"] - valores_pdf["total_servicos"]:.2f}'}</li>
            <li>Produtos: {'✅ OK' if abs(valores_banco['valor_produtos'] - valores_pdf['total_produtos']) < 0.01 else f'❌ Diferença: {valores_banco["valor_produtos"] - valores_pdf["total_produtos"]:.2f}'}</li>
        </ul>
        
        <p><a href="/test/pdf-preview/{os_id}">Ver PDF Preview</a></p>
        """
        
        return resultado
        
    except Exception as e:
        return f"Erro: {e}"

@test_bp.route('/pdf-preview/<int:os_id>')
def pdf_preview(os_id):
    """Visualizar HTML do PDF antes de converter"""
    try:
        # Buscar OS com dados atualizados
        os = OrdemServico.query.options(
            joinedload(OrdemServico.cliente),
            joinedload(OrdemServico.itens),
            joinedload(OrdemServico.arquivos)
        ).get_or_404(os_id)
        
        # Forçar refresh dos dados
        from extensoes import db
        db.session.refresh(os)
        
        # Preparar contexto
        pdf_generator = SimplePDFGenerator()
        context = pdf_generator._prepare_context(os)
        
        # Debug dos valores no contexto
        print(f"=== DEBUG PDF CONTEXT OS {os_id} ===")
        print(f"OS valor_total: {getattr(os, 'valor_total', 'N/A')}")
        print(f"Context valor_total: {context.get('valor_total', 'N/A')}")
        print(f"Context total_servicos: {context.get('total_servicos', 'N/A')}")
        print(f"Context total_produtos: {context.get('total_produtos', 'N/A')}")
        
        # Renderizar template
        return render_template('pdf_template.html', **context)
        
    except Exception as e:
        return f"Erro: {e}"

@test_bp.route('/pdf-simple/<int:os_id>')
def pdf_simple(os_id):
    """Testar geração de PDF simples"""
    try:
        # Buscar OS
        os = OrdemServico.query.options(
            joinedload(OrdemServico.cliente),
            joinedload(OrdemServico.itens),
            joinedload(OrdemServico.arquivos)
        ).get_or_404(os_id)
        
        # Gerar PDF
        pdf_generator = SimplePDFGenerator()
        pdf_bytes = pdf_generator.generate_pdf(os)
        
        from flask import make_response
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename="OS_{os.codigo}_simples.pdf"'
        
        return response
        
    except Exception as e:
        return f"Erro: {e}"
