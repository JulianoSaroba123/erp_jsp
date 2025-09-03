#!/usr/bin/env python
# Script para diagnóstico do PDF

import os
import sys

# Adicionar o diretório da aplicação ao path
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Teste de importações"""
    print("🔍 Testando importações...")
    
    try:
        from app.ordem_servico.simple_pdf_generator import SimplePDFGenerator
        print("✅ SimplePDFGenerator importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar SimplePDFGenerator: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        print("✅ reportlab importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar reportlab: {e}")
        return False
    
    try:
        import weasyprint
        print("✅ weasyprint importado com sucesso")
    except Exception as e:
        print(f"⚠️  weasyprint não disponível: {e}")
    
    return True

def test_pdf_generation():
    """Teste de geração de PDF"""
    print("\n🔍 Testando geração de PDF...")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from io import BytesIO
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        
        p.drawString(100, 750, "Teste de PDF")
        p.drawString(100, 720, "Este é um teste simples")
        
        p.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        print(f"✅ PDF gerado com sucesso: {len(pdf_bytes)} bytes")
        
        # Salvar para teste
        with open('test_diagnostic.pdf', 'wb') as f:
            f.write(pdf_bytes)
        
        print("✅ PDF salvo como test_diagnostic.pdf")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_context():
    """Teste do contexto Flask"""
    print("\n🔍 Testando contexto Flask...")
    
    try:
        from app.app import app
        print("✅ App Flask importado com sucesso")
        
        with app.app_context():
            print("✅ Contexto Flask criado com sucesso")
            
            # Testar modelo
            from app.ordem_servico.os_model import OrdemServico
            print("✅ Modelo OrdemServico importado")
            
            # Testar se existe OS no banco
            os_count = OrdemServico.query.count()
            print(f"✅ Ordens de serviço no banco: {os_count}")
            
            if os_count > 0:
                primeira_os = OrdemServico.query.first()
                print(f"✅ Primeira OS: {primeira_os.codigo}")
                return primeira_os
            else:
                print("⚠️  Nenhuma OS encontrada no banco")
                return None
        
    except Exception as e:
        print(f"❌ Erro no contexto Flask: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_pdf_with_os(os):
    """Teste de PDF com OS real"""
    print("\n🔍 Testando PDF com OS real...")
    
    try:
        from app.ordem_servico.simple_pdf_generator import SimplePDFGenerator
        
        generator = SimplePDFGenerator()
        pdf_bytes = generator.generate_pdf(os)
        
        print(f"✅ PDF da OS gerado: {len(pdf_bytes)} bytes")
        
        # Salvar para teste
        with open(f'test_os_{os.codigo}.pdf', 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF salvo como test_os_{os.codigo}.pdf")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF da OS: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 DIAGNÓSTICO DO SISTEMA PDF\n")
    
    # Teste 1: Importações
    if not test_imports():
        print("\n❌ Falha nas importações. Abortando.")
        return
    
    # Teste 2: PDF básico
    if not test_pdf_generation():
        print("\n❌ Falha na geração de PDF básico. Abortando.")
        return
    
    # Teste 3: Contexto Flask
    os = test_flask_context()
    if os is None:
        print("\n⚠️  Não foi possível obter OS para teste")
        return
    
    # Teste 4: PDF com OS
    test_pdf_with_os(os)
    
    print("\n✅ Diagnóstico concluído!")

if __name__ == "__main__":
    main()
