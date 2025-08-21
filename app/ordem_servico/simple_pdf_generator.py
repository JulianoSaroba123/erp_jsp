"""
Gerador de PDF Simples usando HTML + CSS
Muito mais fácil de manter e atualizar
"""

try:
    from weasyprint import HTML, CSS
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

try:
    import pdfkit
    HAS_PDFKIT = True
except ImportError:
    HAS_PDFKIT = False

from flask import render_template
import tempfile
import os
import io

class SimplePDFGenerator:
    def __init__(self):
        self.use_weasyprint = HAS_WEASYPRINT
        
        if HAS_PDFKIT and not HAS_WEASYPRINT:
            # Configurações do wkhtmltopdf como fallback
            self.options = {
                'page-size': 'A4',
                'margin-top': '1cm',
                'margin-right': '1cm',
                'margin-bottom': '1cm',
                'margin-left': '1cm',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None,
                'print-media-type': None
            }
    
    def generate_pdf(self, os, output_path=None):
        """
        Gera PDF usando template HTML
        Muito mais simples que a versão anterior!
        """
        try:
            # Preparar dados para o template
            context = self._prepare_context(os)
            
            # Renderizar HTML
            html_content = render_template('pdf_template.html', **context)
            
            if self.use_weasyprint and HAS_WEASYPRINT:
                return self._generate_with_weasyprint(html_content, output_path)
            elif HAS_PDFKIT:
                return self._generate_with_pdfkit(html_content, output_path)
            else:
                return self._generate_fallback(html_content, output_path)
                
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
            return self._generate_fallback_old(os, output_path)
    
    def _generate_with_weasyprint(self, html_content, output_path):
        """Gera PDF usando WeasyPrint (recomendado)"""
        try:
            html_doc = HTML(string=html_content)
            
            if output_path:
                html_doc.write_pdf(output_path)
                return output_path
            else:
                pdf_bytes = html_doc.write_pdf()
                return pdf_bytes
        except Exception as e:
            print(f"Erro no WeasyPrint: {e}")
            raise
    
    def _generate_with_pdfkit(self, html_content, output_path):
        """Gera PDF usando pdfkit (fallback)"""
        if output_path:
            pdfkit.from_string(html_content, output_path, options=self.options)
            return output_path
        else:
            pdf_bytes = pdfkit.from_string(html_content, False, options=self.options)
            return pdf_bytes
    
    def _generate_fallback(self, html_content, output_path):
        """Fallback: retorna HTML quando PDF não está disponível"""
        print("⚠️  Bibliotecas de PDF não disponíveis, retornando HTML")
        if output_path:
            html_path = output_path.replace('.pdf', '.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return html_path
        else:
            return html_content.encode('utf-8')
    
    def _generate_fallback_old(self, os, output_path):
        """Fallback final: usar gerador antigo"""
        try:
            # from .pdf_generator import OSPDFGenerator
            # old_generator = OSPDFGenerator()
            # if hasattr(old_generator, 'generate_pdf_bytes'):
            #     return old_generator.generate_pdf_bytes(os)
            # else:
            #     return old_generator.generate_pdf(os, output_path)
            return b"PDF antigo indisponivel - usando apenas HTML template"
        except Exception as e2:
            print(f"Erro no fallback antigo também: {e2}")
            return b"Erro ao gerar PDF"
    
    def _prepare_context(self, os):
        """Prepara os dados para o template"""
        context = {
            'os': os,
            'servicos_dados': [],
            'produtos_dados': [],
            'total_servicos': 0,
            'total_produtos': 0,
            'valor_total': 0,
            'horas_reais_calculadas': 0
        }
        
        # Calcular horas reais se há horários
        if hasattr(os, 'hora_inicio') and hasattr(os, 'hora_termino') and os.hora_inicio and os.hora_termino:
            try:
                inicio_str = os.hora_inicio.strftime('%H:%M')
                termino_str = os.hora_termino.strftime('%H:%M')
                inicio_parts = inicio_str.split(':')
                termino_parts = termino_str.split(':')
                inicio_minutos = (int(inicio_parts[0]) * 60) + int(inicio_parts[1])
                termino_minutos = (int(termino_parts[0]) * 60) + int(termino_parts[1])
                diff_minutos = termino_minutos - inicio_minutos
                if diff_minutos > 0:
                    context['horas_reais_calculadas'] = diff_minutos / 60.0
                print(f"DEBUG HORAS: {inicio_str} até {termino_str} = {context['horas_reais_calculadas']:.2f}h")
            except Exception as e:
                print(f"Erro no cálculo de horas: {e}")
        
        # Processar itens da OS se existirem
        if hasattr(os, 'itens') and os.itens:
            for item in os.itens:
                if hasattr(item, 'tipo_item'):
                    if item.tipo_item == 'servico':
                        servico_data = {
                            'nome': item.descricao or '',
                            'quantidade': float(item.quantidade or 0),
                            'valor_total': float(item.valor_total or 0)
                        }
                        context['servicos_dados'].append(servico_data)
                        context['total_servicos'] += servico_data['valor_total']
                    
                    elif item.tipo_item == 'produto':
                        produto_data = {
                            'nome': item.descricao or '',
                            'quantidade': int(item.quantidade or 0),
                            'valor_unitario': float(item.valor_unitario or 0),
                            'valor_total': float(item.valor_total or 0)
                        }
                        context['produtos_dados'].append(produto_data)
                        context['total_produtos'] += produto_data['valor_total']
        
        # CORREÇÃO: Garantir que total_servicos seja o valor correto da OS
        # Se não há itens detalhados, usar valores diretos da OS
        if not context['servicos_dados'] and hasattr(os, 'valor_servicos') and os.valor_servicos:
            context['total_servicos'] = float(os.valor_servicos)
        
        if not context['produtos_dados'] and hasattr(os, 'valor_produtos') and os.valor_produtos:
            context['total_produtos'] = float(os.valor_produtos)
        
        # SEMPRE usar o valor_total da OS como valor final
        # Isso corrige o problema onde estava aparecendo apenas valor de serviços
        if hasattr(os, 'valor_total') and os.valor_total:
            context['valor_total'] = float(os.valor_total)
        else:
            # Fallback: calcular apenas se não há valor_total definido
            context['valor_total'] = context['total_servicos'] + context['total_produtos']
        
        # CORREÇÃO FINAL: SEMPRE usar os valores diretamente da OS
        # Isso garante que o PDF sempre mostra os valores corretos
        if hasattr(os, 'valor_servicos') and os.valor_servicos is not None:
            context['total_servicos'] = float(os.valor_servicos)
        
        if hasattr(os, 'valor_produtos') and os.valor_produtos is not None:
            context['total_produtos'] = float(os.valor_produtos)
            
        if hasattr(os, 'valor_total') and os.valor_total is not None:
            context['valor_total'] = float(os.valor_total)
        
        # Debug: imprimir os valores para verificar
        print(f"=== DEBUG PDF DETALHADO - OS ID: {os.id} ===")
        print(f"OS.valor_total (original): {getattr(os, 'valor_total', 'N/A')}")
        print(f"OS.valor_servicos: {getattr(os, 'valor_servicos', 'N/A')}")
        print(f"OS.valor_produtos: {getattr(os, 'valor_produtos', 'N/A')}")
        print(f"OS.total_horas: {getattr(os, 'total_horas', 'N/A')}")
        print(f"Context total_servicos (calculado): {context['total_servicos']}")
        print(f"Context total_produtos (calculado): {context['total_produtos']}")
        print(f"Context valor_total (calculado): {context['total_servicos'] + context['total_produtos']}")
        print(f"Context valor_total (final): {context['valor_total']}")
        print(f"Número de itens detalhados: {len(getattr(os, 'itens', []))}")
        print(f"=== FIM DEBUG ===")
        
        return context

# Para compatibilidade com código existente
class OSPDFGenerator(SimplePDFGenerator):
    """Alias para manter compatibilidade"""
    pass
