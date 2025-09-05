#!/usr/bin/env python3
"""
Teste de integração para o módulo financeiro com ordens de serviço
"""

import sys
import os
from datetime import date, timedelta
from decimal import Decimal

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app.app import app
from app.extensoes import db
from app.ordem_servico.os_model import OrdemServico
from app.cliente.cliente_model import Cliente
from app.financeiro.lancamento_os_service import gerar_lancamentos_financeiro, remover_lancamentos_da_os
from app.financeiro.lancamento_os_model import LancamentoFinanceiroOS

def test_integracao_financeira():
    """Testa a integração básica entre OS e financeiro"""
    with app.app_context():
        print("=== TESTE DE INTEGRAÇÃO FINANCEIRA ===")
        
        # Criar cliente de teste
        cliente = Cliente(
            nome="Cliente Teste Financeiro",
            cpf_cnpj="123.456.789-10",
            email="teste@example.com"
        )
        db.session.add(cliente)
        db.session.flush()
        
        # Criar OS de teste
        os_teste = OrdemServico(
            codigo="OSTESTE001",
            cliente_id=cliente.id,
            valor_total=1000.00,
            status="Concluída",
            status_pagamento="pago",
            forma_pagamento="PIX",
            condicao_pagamento="parcelado",
            qtd_parcelas=3,
            valor_entrada=200.00
        )
        db.session.add(os_teste)
        db.session.flush()
        
        print(f"OS criada: {os_teste.codigo}")
        print(f"Valor total: R$ {os_teste.valor_total}")
        print(f"Parcelas: {os_teste.qtd_parcelas}")
        print(f"Entrada: R$ {os_teste.valor_entrada}")
        
        # Teste 1: Pagamento parcelado com entrada
        print("\n--- TESTE 1: Parcelado com entrada ---")
        lancamentos = gerar_lancamentos_financeiro(
            os=os_teste,
            forma_pagamento="PIX",
            valor_total=Decimal("1000.00"),
            parcelas=3,
            entrada=Decimal("200.00")
        )
        
        print(f"Lançamentos criados: {len(lancamentos)}")
        for i, lanc in enumerate(lancamentos):
            print(f"  {i+1}. {lanc.descricao} - R$ {lanc.valor} - {lanc.data_vencimento}")
        
        # Verificar se os valores batem
        total_lancamentos = sum(float(lanc.valor) for lanc in lancamentos)
        print(f"Total dos lançamentos: R$ {total_lancamentos}")
        assert abs(total_lancamentos - 1000.00) < 0.01, "Valores não conferem!"
        
        # Teste 2: Idempotência - reprocessar deve remover e recriar
        print("\n--- TESTE 2: Idempotência ---")
        antes = len(lancamentos)
        lancamentos2 = gerar_lancamentos_financeiro(
            os=os_teste,
            forma_pagamento="PIX",
            valor_total=Decimal("1000.00"),
            parcelas=3,
            entrada=Decimal("200.00")
        )
        
        print(f"Lançamentos após reprocessar: {len(lancamentos2)}")
        assert len(lancamentos2) == antes, "Idempotência falhou!"
        
        # Teste 3: Cronograma personalizado
        print("\n--- TESTE 3: Cronograma personalizado ---")
        schedule_custom = [
            (Decimal("500.00"), date.today()),
            (Decimal("300.00"), date.today() + timedelta(days=15)),
            (Decimal("200.00"), date.today() + timedelta(days=45))
        ]
        
        lancamentos3 = gerar_lancamentos_financeiro(
            os=os_teste,
            forma_pagamento="PIX",
            valor_total=Decimal("1000.00"),
            schedule_custom=schedule_custom
        )
        
        print(f"Lançamentos com cronograma personalizado: {len(lancamentos3)}")
        for i, lanc in enumerate(lancamentos3):
            print(f"  {i+1}. {lanc.descricao} - R$ {lanc.valor} - {lanc.data_vencimento}")
        
        # Verificar se seguiu o cronograma
        assert len(lancamentos3) == 3, "Número de parcelas incorreto!"
        assert float(lancamentos3[0].valor) == 500.00, "Valor da primeira parcela incorreto!"
        
        # Teste 4: À vista
        print("\n--- TESTE 4: À vista ---")
        lancamentos4 = gerar_lancamentos_financeiro(
            os=os_teste,
            forma_pagamento="Dinheiro",
            valor_total=Decimal("1000.00"),
            parcelas=1
        )
        
        print(f"Lançamentos à vista: {len(lancamentos4)}")
        assert len(lancamentos4) == 1, "Deve ter apenas um lançamento à vista!"
        assert float(lancamentos4[0].valor) == 1000.00, "Valor à vista incorreto!"
        
        # Limpeza
        remover_lancamentos_da_os(os_teste.id)
        db.session.delete(os_teste)
        db.session.delete(cliente)
        db.session.commit()
        
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("🎯 Integração financeira funcionando corretamente!")

if __name__ == "__main__":
    test_integracao_financeira()
