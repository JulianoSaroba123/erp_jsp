#!/usr/bin/env python3
"""Script para debugar problema com criação de OS"""

from app import create_app
from extensoes import db
from cliente.cliente_model import Cliente
from ordem_servico.os_model import OrdemServico

app = create_app()

with app.app_context():
    print("=== DEBUG ORDEM DE SERVIÇO ===")
    
    # Verificar clientes
    clientes = Cliente.query.filter_by(ativo=True).all()
    print(f"\nClientes ativos: {len(clientes)}")
    for c in clientes[:3]:
        print(f"  ID: {c.id}, Nome: {c.nome}")
    
    # Verificar OS existentes
    ordens = OrdemServico.query.all()
    print(f"\nOrdens de Serviço: {len(ordens)}")
    for os in ordens[-3:]:
        print(f"  ID: {os.id}, Código: {os.codigo}, Cliente: {os.cliente_id}")
    
    # Verificar estrutura da tabela
    print(f"\nTabela OS existe: {db.engine.has_table('ordem_servico')}")
    
    # Teste básico de criação
    print("\n=== TESTE DE CRIAÇÃO ===")
    if len(clientes) > 0:
        dados_teste = {
            'cliente_id': str(clientes[0].id),
            'data_emissao': '2025-08-05',
            'status': 'Aberta',
            'equipamento_nome': 'Teste Debug',
            'problema_descrito': 'Teste de debug',
            'tecnico_responsavel': 'Debug Tester',
            'valor_total': '100.00'
        }
        
        from ordem_servico.os_calculos import CalculadoraOS
        is_valid, erros = CalculadoraOS.validar_dados_os(dados_teste)
        print(f"Dados válidos: {is_valid}")
        if not is_valid:
            print(f"Erros: {erros}")
        else:
            print("Dados passaram na validação!")
    else:
        print("Nenhum cliente encontrado para teste")
