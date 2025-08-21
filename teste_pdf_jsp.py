#!/usr/bin/env python3
"""
Teste para geração de PDF com template JSP ELÉTRICA
"""

import sys
import os
from datetime import datetime

# Adicionar o diretório app ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.ordem_servico.pdf_generator import OSPDFGenerator

class MockOS:
    """Mock object para simular uma Ordem de Serviço com dados JSP"""
    
    def __init__(self):
        # Dados básicos da OS
        self.numero = "2024001"
        self.data_abertura = datetime.now()
        self.data_conclusao = datetime.now()
        
        # Dados do cliente
        self.cliente_nome = "EMPRESA EXEMPLO LTDA"
        self.cliente_endereco = "RUA DAS FLORES, 123"
        self.cliente_cidade = "SÃO PAULO"
        self.cliente_cep = "01234-567"
        self.cliente_telefone = "(11) 98765-4321"
        self.cliente_email = "contato@empresa.com.br"
        self.cliente_contato = "João Silva"
        
        # Dados do equipamento
        self.equipamento_nome = "Calandra 01"
        self.equipamento_marca = "Mirandópolis"
        self.equipamento_modelo = "CC440"
        self.equipamento_numero_serie = "123456789"
        self.equipamento_acessorios = "Rolos extras, Suporte"
        
        # Informações técnicas
        self.responsavel_tecnico = "Carlos Santos - Técnico Eletrônico"
        self.problema_relatado = "Equipamento apresentando ruído excessivo e aquecimento"
        self.problema_encontrado = "Rolamentos desgastados e sistema de ventilação obstruído"
        self.solucao = "Substituição dos rolamentos e limpeza do sistema de ventilação"
        self.observacoes = "Recomenda-se manutenção preventiva a cada 6 meses"
        
        # Valores financeiros
        self.valor_servicos = 450.00
        self.valor_produtos = 280.00
        self.valor_mao_obra = 150.00
        self.valor_deslocamento = 50.00
        self.valor_descontos = 30.00
        self.valor_total = 900.00
        
        # Mock de serviços e produtos
        self.servicos = [
            MockItem("Substituição de rolamentos", 1, 200.00, 200.00, "servico"),
            MockItem("Limpeza sistema ventilação", 1, 150.00, 150.00, "servico"),
            MockItem("Teste operacional", 1, 100.00, 100.00, "servico")
        ]
        
        self.itens = [
            MockItem("Rolamento SKF 6205", 2, 85.00, 170.00, "produto"),
            MockItem("Filtro de ar", 1, 45.00, 45.00, "produto"),
            MockItem("Óleo lubrificante", 1, 65.00, 65.00, "produto")
        ]
        
        # Mock arquivos (vazio para este teste)
        self.arquivos = []

class MockItem:
    """Mock para itens/serviços"""
    
    def __init__(self, descricao, quantidade, valor_unitario, valor_total, tipo_item):
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total
        self.tipo_item = tipo_item

def test_jsp_pdf():
    """Testa a geração de PDF com template JSP"""
    
    print("🔧 Iniciando teste de geração PDF JSP...")
    
    try:
        # Criar mock da OS
        os_mock = MockOS()
        
        # Criar gerador de PDF
        pdf_generator = OSPDFGenerator()
        
        # Gerar PDF
        output_path = "teste_os_jsp.pdf"
        pdf_path = pdf_generator.generate_pdf(os_mock, output_path)
        
        if os.path.exists(pdf_path):
            print(f"✅ PDF gerado com sucesso: {pdf_path}")
            print(f"📄 Tamanho do arquivo: {os.path.getsize(pdf_path)} bytes")
            
            # Informações do template JSP aplicado
            print("\n🎨 Template JSP ELÉTRICA aplicado:")
            print("   • Cabeçalho com logo e dados da empresa")
            print("   • Cores JSP: Azul, Laranja e Azul Claro") 
            print("   • Dados do cliente e equipamento")
            print("   • Seções de serviços e produtos")
            print("   • Informações técnicas detalhadas")
            print("   • Resumo financeiro com destaque")
            print("   • Dados bancários para transferência")
            print("   • Seção para assinaturas")
            
        else:
            print("❌ Erro: PDF não foi criado")
            
    except Exception as e:
        print(f"❌ Erro durante geração do PDF: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_jsp_pdf()
