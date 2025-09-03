from weasyprint import HTML
import tempfile

def test_simple_weasyprint():
    """Teste básico do WeasyPrint"""
    try:
        print("🔍 Testando WeasyPrint...")
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Teste</title>
        </head>
        <body>
            <h1>Teste WeasyPrint</h1>
            <p>Este é um teste simples.</p>
        </body>
        </html>
        """
        
        # Gerar PDF
        html_doc = HTML(string=html_content)
        pdf_bytes = html_doc.write_pdf()
        
        # Salvar em arquivo
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_bytes)
            temp_path = temp_file.name
            
        print(f"✅ PDF gerado: {temp_path}")
        print(f"📊 Tamanho: {len(pdf_bytes)} bytes")
        
        # Verificar se é PDF válido
        if pdf_bytes.startswith(b'%PDF'):
            print("✅ PDF válido!")
        else:
            print(f"❌ PDF inválido - primeiros bytes: {pdf_bytes[:20]}")
            
        return temp_path
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_simple_weasyprint()
