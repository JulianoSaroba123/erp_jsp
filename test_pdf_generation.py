import os
import sys
from flask import Flask
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
import tempfile

# Adicionando o diretório da aplicação ao path
sys.path.append(os.path.abspath('.'))

def test_pdf_generation():
    """Teste simples para verificar a geração de PDF"""
    
    # HTML básico para teste
    html_test = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Teste PDF</title>
        <style>
            body { font-family: Arial, sans-serif; }
            h1 { color: blue; }
        </style>
    </head>
    <body>
        <h1>Teste de Geração de PDF</h1>
        <p>Este é um teste simples para verificar se o WeasyPrint está funcionando corretamente.</p>
        <p>Data: 2025-09-02</p>
    </body>
    </html>
    """
    
    try:
        print("🔍 Testando geração de PDF com WeasyPrint...")
        
        # Gerar PDF a partir do HTML
        html_doc = HTML(string=html_test)
        pdf_bytes = html_doc.write_pdf()
        
        # Salvar o PDF em um arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_bytes)
            temp_pdf_path = temp_file.name
        
        print(f"✅ PDF gerado com sucesso!")
        print(f"📁 Arquivo salvo em: {temp_pdf_path}")
        print(f"📊 Tamanho do PDF: {len(pdf_bytes)} bytes")
        
        # Verificar se o arquivo é válido
        with open(temp_pdf_path, 'rb') as f:
            first_bytes = f.read(8)
            if first_bytes.startswith(b'%PDF'):
                print("✅ PDF válido - Header correto encontrado")
            else:
                print(f"❌ PDF inválido - Header incorreto: {first_bytes}")
        
        return temp_pdf_path
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {str(e)}")
        return None

def test_template_pdf():
    """Teste usando o template real da aplicação"""
    
    try:
        print("\n🔍 Testando com template da aplicação...")
        
        # Configurar o ambiente Jinja2
        template_dir = os.path.join(os.getcwd(), 'app', 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        
        # Dados fictícios para o template
        dados_teste = {
            'os': {
                'codigo': 'OS0001',
                'data_emissao': '2025-09-02',
                'cliente_nome': 'Empresa Teste Ltda',
                'solicitante': 'João Silva',
                'contato': '(15) 99999-9999',
                'tipo_servico': 'Instalação',
                'prioridade': 'Normal',
                'status': 'Concluída',
                'tecnico_responsavel': 'Juliano Saroba Pereira',
                'equipamento_nome': 'Quadro Elétrico Principal',
                'equipamento_marca': 'Schneider',
                'problema_descrito': 'Teste de instalação',
                'descricao_servico_realizado': 'Serviço realizado com sucesso',
                'valor_total': 1520.0,
                'forma_pagamento': 'À Vista'
            },
            'servicos': [
                {'nome': 'Instalação Elétrica', 'quantidade': 8.0, 'valor_total': 800.0}
            ],
            'produtos': [
                {'nome': 'Disjuntor 25A', 'quantidade': 2, 'valor_unitario': 35.0, 'valor_total': 70.0}
            ]
        }
        
        # Renderizar o template
        template = env.get_template('ordem_servico/pdf_os.html')
        html_content = template.render(**dados_teste)
        
        print("✅ Template renderizado com sucesso")
        
        # Gerar PDF
        html_doc = HTML(string=html_content)
        pdf_bytes = html_doc.write_pdf()
        
        # Salvar PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_bytes)
            temp_pdf_path = temp_file.name
        
        print(f"✅ PDF do template gerado com sucesso!")
        print(f"📁 Arquivo salvo em: {temp_pdf_path}")
        print(f"📊 Tamanho do PDF: {len(pdf_bytes)} bytes")
        
        return temp_pdf_path
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF do template: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🚀 Iniciando testes de geração de PDF\n")
    
    # Teste 1: PDF básico
    pdf_path1 = test_pdf_generation()
    
    # Teste 2: PDF com template
    pdf_path2 = test_template_pdf()
    
    print(f"\n📋 Resumo dos testes:")
    print(f"Teste básico: {'✅ Sucesso' if pdf_path1 else '❌ Falhou'}")
    print(f"Teste template: {'✅ Sucesso' if pdf_path2 else '❌ Falhou'}")
    
    if pdf_path1:
        print(f"PDF básico: {pdf_path1}")
    if pdf_path2:
        print(f"PDF template: {pdf_path2}")
