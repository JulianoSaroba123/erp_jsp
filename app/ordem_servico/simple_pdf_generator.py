"""
Gerador de PDF Simples usando HTML + CSS
Muito mais fácil de manter e atualizar
"""

try:
    from weasyprint import HTML, CSS
    HAS_WEASYPRINT = True
    print("✅ WeasyPrint disponível")
except ImportError as e:
    print(f"❌ WeasyPrint não disponível: {e}")
    HAS_WEASYPRINT = False
except Exception as e:
    print(f"❌ Erro ao carregar WeasyPrint: {e}")
    HAS_WEASYPRINT = False

try:
    import pdfkit
    HAS_PDFKIT = True
    print("✅ PDFKit disponível")
except ImportError as e:
    print(f"❌ PDFKit não disponível: {e}")
    HAS_PDFKIT = False
except Exception as e:
    print(f"❌ Erro ao carregar PDFKit: {e}")
    HAS_PDFKIT = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    HAS_REPORTLAB = True
    print("✅ ReportLab disponível")
except ImportError as e:
    print(f"❌ ReportLab não disponível: {e}")
    HAS_REPORTLAB = False
except Exception as e:
    print(f"❌ Erro ao carregar ReportLab: {e}")
    HAS_REPORTLAB = False

from flask import render_template
import tempfile
import os
import io
from datetime import datetime
import json

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
        print(f"▶️ Iniciando geração de PDF para OS: {os.codigo}")
        print(f"▶️ Status bibliotecas: WeasyPrint={HAS_WEASYPRINT}, ReportLab={HAS_REPORTLAB}, PDFKit={HAS_PDFKIT}")
        try:
            # Preparar dados para o template
            context = self._prepare_context(os)
            
            # PRIMEIRO: Tentar com reportlab (mais confiável)
            print("🔍 Tentando gerar PDF com reportlab...")
            return self._generate_with_reportlab(os, output_path)
            
        except Exception as e:
            print(f"❌ Erro no reportlab: {e}")
            
            try:
                # SEGUNDO: Tentar com WeasyPrint usando o template relatorio_cliente_print.html
                print("🔍 Tentando fallback com WeasyPrint...")
                context = self._prepare_context(os)
                html_content = render_template('relatorio_cliente_print.html', **context)
                if self.use_weasyprint and HAS_WEASYPRINT:
                    return self._generate_with_weasyprint(html_content, output_path)
                else:
                    print("WeasyPrint não disponível")
                    raise Exception("WeasyPrint não disponível")
                    
            except Exception as e2:
                print(f"❌ Erro no WeasyPrint também: {e2}")
                return self._generate_fallback_simple(os, output_path)
    
    def _generate_with_weasyprint(self, html_content, output_path):
        """Gera PDF usando WeasyPrint (recomendado)"""
        try:
            print("🔍 Tentando gerar PDF com WeasyPrint...")
            html_doc = HTML(string=html_content)
            
            if output_path:
                html_doc.write_pdf(output_path)
                print(f"✅ PDF salvo em: {output_path}")
                return output_path
            else:
                pdf_bytes = html_doc.write_pdf()
                print(f"✅ PDF gerado: {len(pdf_bytes)} bytes")
                
                # Verificar se é PDF válido
                if pdf_bytes.startswith(b'%PDF'):
                    print("✅ PDF válido!")
                else:
                    print(f"❌ PDF inválido - primeiros bytes: {pdf_bytes[:20]}")
                    raise Exception("PDF gerado é inválido")
                    
                return pdf_bytes
        except Exception as e:
            print(f"❌ Erro no WeasyPrint: {e}")
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
    
    def _generate_with_reportlab(self, os, output_path):
        """Gera PDF usando reportlab (fallback confiável)"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import mm
            from io import BytesIO
            
            print("📄 Gerando PDF com reportlab...")
            
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4
            
            # Configurações
            margin = 20 * mm
            y_pos = height - margin
            line_height = 15
            
            # Cabeçalho
            p.setFont("Helvetica-Bold", 16)
            p.drawString(margin, y_pos, "JSP ELÉTRICA")
            y_pos -= 20
            
            p.setFont("Helvetica", 12)
            p.drawString(margin, y_pos, "Juliano Saroba Pereira - Eletricista")
            y_pos -= 15
            p.drawString(margin, y_pos, "Telefone: (15) 99999-9999")
            y_pos -= 30
            
            # Título da OS
            p.setFont("Helvetica-Bold", 14)
            p.drawString(margin, y_pos, f"ORDEM DE SERVIÇO Nº {os.codigo}")
            y_pos -= 30
            
            # Dados básicos
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin, y_pos, "DADOS BÁSICOS")
            y_pos -= 20
            
            p.setFont("Helvetica", 10)
            y_pos = self._add_field(p, margin, y_pos, "Código:", os.codigo)
            y_pos = self._add_field(p, margin, y_pos, "Data Emissão:", 
                                   os.data_emissao.strftime('%d/%m/%Y') if os.data_emissao else 'N/A')
            y_pos = self._add_field(p, margin, y_pos, "Status:", os.status or 'N/A')
            y_pos = self._add_field(p, margin, y_pos, "Prioridade:", os.prioridade or 'N/A')
            y_pos -= 15
            
            # Dados do cliente
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin, y_pos, "DADOS DO CLIENTE")
            y_pos -= 20
            
            p.setFont("Helvetica", 10)
            y_pos = self._add_field(p, margin, y_pos, "Cliente:", 
                                   os.cliente.nome if os.cliente else 'N/A')
            y_pos = self._add_field(p, margin, y_pos, "Solicitante:", os.solicitante or 'N/A')
            y_pos = self._add_field(p, margin, y_pos, "Contato:", os.contato or 'N/A')
            y_pos -= 15
            
            # Equipamento
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin, y_pos, "EQUIPAMENTO")
            y_pos -= 20
            
            p.setFont("Helvetica", 10)
            y_pos = self._add_field(p, margin, y_pos, "Nome:", os.equipamento_nome or 'N/A')
            y_pos = self._add_field(p, margin, y_pos, "Marca:", os.equipamento_marca or 'N/A')
            y_pos = self._add_field(p, margin, y_pos, "Modelo:", os.equipamento_modelo or 'N/A')
            y_pos -= 15
            
            # Descrição do problema
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin, y_pos, "DESCRIÇÃO DO PROBLEMA")
            y_pos -= 20
            
            p.setFont("Helvetica", 10)
            problema = os.problema_descrito or 'Nenhuma descrição informada.'
            y_pos = self._add_text_block(p, margin, y_pos, problema, width - 2*margin)
            y_pos -= 15
            
            # Serviço realizado
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin, y_pos, "SERVIÇO REALIZADO")
            y_pos -= 20
            
            p.setFont("Helvetica", 10)
            servico = os.descricao_servico_realizado or 'Nenhuma descrição informada.'
            y_pos = self._add_text_block(p, margin, y_pos, servico, width - 2*margin)
            y_pos -= 15
            
            # Dados de execução
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin, y_pos, "DADOS DE EXECUÇÃO")
            y_pos -= 20
            
            p.setFont("Helvetica", 10)
            y_pos = self._add_field(p, margin, y_pos, "Técnico:", os.tecnico_responsavel or 'N/A')
            y_pos = self._add_field(p, margin, y_pos, "Hora Início:", 
                                   os.hora_inicio.strftime('%H:%M') if os.hora_inicio else 'N/A')
            y_pos = self._add_field(p, margin, y_pos, "Hora Término:", 
                                   os.hora_termino.strftime('%H:%M') if os.hora_termino else 'N/A')
            y_pos = self._add_field(p, margin, y_pos, "Total Horas:", str(os.total_horas or 'N/A'))
            y_pos -= 15
            
            # Valores
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin, y_pos, "VALORES")
            y_pos -= 20
            
            p.setFont("Helvetica", 10)
            y_pos = self._add_field(p, margin, y_pos, "Mão de Obra:", f"R$ {os.valor_mao_obra or 0:.2f}")
            y_pos = self._add_field(p, margin, y_pos, "Produtos:", f"R$ {os.valor_produtos or 0:.2f}")
            y_pos = self._add_field(p, margin, y_pos, "Serviços:", f"R$ {os.valor_servicos or 0:.2f}")
            y_pos = self._add_field(p, margin, y_pos, "Deslocamento:", f"R$ {os.valor_deslocamento or 0:.2f}")
            
            # Total destacado
            p.setFont("Helvetica-Bold", 12)
            y_pos = self._add_field(p, margin, y_pos, "TOTAL:", f"R$ {os.valor_total or 0:.2f}")
            y_pos -= 15
            
            # Pagamento
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin, y_pos, "PAGAMENTO")
            y_pos -= 20
            
            p.setFont("Helvetica", 10)
            y_pos = self._add_field(p, margin, y_pos, "Forma:", os.forma_pagamento or 'N/A')
            y_pos = self._add_field(p, margin, y_pos, "Condições:", os.condicoes_pagamento or 'N/A')
            y_pos -= 30
            
            # Assinaturas
            p.setFont("Helvetica-Bold", 10)
            p.drawString(margin, y_pos, "Técnico: ________________________")
            p.drawString(width/2, y_pos, "Cliente: ________________________")
            y_pos -= 20
            
            p.setFont("Helvetica", 8)
            p.drawString(margin, y_pos, os.tecnico_responsavel or 'Juliano Saroba Pereira')
            p.drawString(width/2, y_pos, os.cliente.nome if os.cliente else '')
            
            p.save()
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            print(f"✅ PDF gerado com reportlab: {len(pdf_bytes)} bytes")
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(pdf_bytes)
                return output_path
            else:
                return pdf_bytes
                
        except Exception as e:
            print(f"❌ Erro no reportlab: {e}")
            raise
    
    def _add_field(self, canvas, x, y, label, value):
        """Adiciona um campo label: valor"""
        canvas.drawString(x, y, f"{label} {value}")
        return y - 15
    
    def _add_text_block(self, canvas, x, y, text, max_width):
        """Adiciona um bloco de texto com quebra de linha"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if canvas.stringWidth(test_line, "Helvetica", 10) < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            canvas.drawString(x, y, line)
            y -= 15
        
        return y
    
    def _generate_fallback_simple(self, os, output_path):
        """Fallback super simples"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from io import BytesIO
            
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            
            p.drawString(100, 750, f"JSP ELÉTRICA - OS {os.codigo}")
            p.drawString(100, 720, f"Cliente: {os.cliente.nome if os.cliente else 'N/A'}")
            p.drawString(100, 690, f"Data: {os.data_emissao.strftime('%d/%m/%Y') if os.data_emissao else 'N/A'}")
            p.drawString(100, 660, f"Total: R$ {os.valor_total or 0:.2f}")
            p.drawString(100, 600, f"PDF gerado em modo simplificado")
            
            p.save()
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(pdf_bytes)
                return output_path
            else:
                return pdf_bytes
                
        except Exception as e:
            print(f"❌ Erro no fallback simples: {e}")
            return b"Erro ao gerar PDF"
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
        """Prepara os dados para o template relatorio_cliente_print.html"""
        context = {
            'os': os,
            'servicos_realizados': [],
            'produtos_utilizados': [],
            'parcelas_salvas': [],
            'total_servicos': 0,
            'total_produtos': 0,
            'valor_total': 0,
            'data_geracao': datetime.now()
        }
        
        # Processar dados de serviços do JSON para formato esperado pelo template
        total_servicos_calculado = 0
        if hasattr(os, 'servicos_dados') and os.servicos_dados:
            try:
                servicos_json = json.loads(os.servicos_dados) if isinstance(os.servicos_dados, str) else os.servicos_dados
                for servico in servicos_json:
                    valor_total_servico = float(servico.get('valor_total', 0))
                    # Adaptar para o formato esperado pelo template (nome, qtd_horas, valor)
                    context['servicos_realizados'].append({
                        'nome': servico.get('nome', ''),
                        'qtd_horas': float(servico.get('quantidade', 0)),
                        'valor': valor_total_servico / max(float(servico.get('quantidade', 1)), 1),  # valor unitário
                        'valor_total': valor_total_servico
                    })
                    total_servicos_calculado += valor_total_servico
            except Exception as e:
                print(f"Erro ao processar servicos_dados: {e}")
        
        # Processar dados de produtos do JSON para formato esperado pelo template
        total_produtos_calculado = 0
        if hasattr(os, 'produtos_dados') and os.produtos_dados:
            try:
                produtos_json = json.loads(os.produtos_dados) if isinstance(os.produtos_dados, str) else os.produtos_dados
                for produto in produtos_json:
                    valor_total_produto = float(produto.get('valor_total', 0))
                    # Adaptar para o formato esperado pelo template
                    context['produtos_utilizados'].append({
                        'nome': produto.get('nome', ''),
                        'quantidade': int(produto.get('quantidade', 0)),
                        'valor_unitario': float(produto.get('valor_unitario', 0)),
                        'valor_total': valor_total_produto
                    })
                    total_produtos_calculado += valor_total_produto
            except Exception as e:
                print(f"Erro ao processar produtos_dados: {e}")
        
        # Processar parcelas do JSON se existir
        if hasattr(os, 'parcelas_json') and os.parcelas_json:
            try:
                parcelas_json = json.loads(os.parcelas_json) if isinstance(os.parcelas_json, str) else os.parcelas_json
                if isinstance(parcelas_json, list):
                    for parcela in parcelas_json:
                        context['parcelas_salvas'].append({
                            'vencimento': parcela.get('vencimento', ''),
                            'valor': float(parcela.get('valor', 0)),
                            'situacao': parcela.get('situacao', 'Em aberto')
                        })
            except Exception as e:
                print(f"Erro ao processar parcelas_json: {e}")
        
        # Usar os totais calculados corretamente da soma dos itens
        context['total_servicos'] = total_servicos_calculado
        context['total_produtos'] = total_produtos_calculado
        
        # Calcular o valor total correto
        valor_deslocamento = float(os.valor_deslocamento or 0) if hasattr(os, 'valor_deslocamento') else 0
        context['valor_total'] = total_servicos_calculado + total_produtos_calculado + valor_deslocamento
        
        # Debug
        print(f"=== DEBUG PDF RELATORIO_CLIENTE_PRINT - OS {os.codigo} ===")
        print(f"Servicos realizados: {len(context['servicos_realizados'])}")
        print(f"Produtos utilizados: {len(context['produtos_utilizados'])}")
        print(f"Parcelas: {len(context['parcelas_salvas'])}")
        print(f"Valor total: R$ {context['valor_total']}")
        print(f"=== FIM DEBUG ===")
        
        return context

# Para compatibilidade com código existente
class OSPDFGenerator(SimplePDFGenerator):
    """Alias para manter compatibilidade"""
    pass
