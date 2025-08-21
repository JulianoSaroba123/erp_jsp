#!/usr/bin/env python3
"""
Script simples para testar valores dos serviços no PDF
"""

print("Iniciando teste...")

try:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
    
    print("Importando módulos...")
    from app import app
    from ordem_servico.os_model import OrdemServico
    from ordem_servico.simple_pdf_generator import SimplePDFGenerator
    
    print("Iniciando contexto da aplicação...")
    with app.app_context():
        print("Buscando OS...")
        os = OrdemServico.query.first()
        if os:
            print(f"=== OS: {os.codigo} ===")
            print(f"valor_servicos: {os.valor_servicos}")
            print(f"valor_total: {os.valor_total}")
            
            print("Testando gerador PDF...")
            generator = SimplePDFGenerator()
            context = generator._prepare_context(os)
            
            print(f"Context total_servicos: {context['total_servicos']}")
            print(f"Context valor_total: {context['valor_total']}")
            
            if context['total_servicos'] == float(os.valor_servicos or 0):
                print("✅ CORRETO!")
            else:
                print("❌ ERRO nos valores!")
        else:
            print("❌ Nenhuma OS encontrada")
            
except Exception as e:
    print(f"ERRO: {e}")
    import traceback
    traceback.print_exc()
