#!/usr/bin/env python3
"""
Exemplo de uso da integração financeira
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
from app.financeiro.lancamento_os_service import gerar_lancamentos_financeiro

def exemplo_uso():
    """Demonstra como usar a integração financeira"""
    with app.app_context():
        print("=== EXEMPLO DE USO DA INTEGRAÇÃO FINANCEIRA ===")
        
        # Buscar uma OS existente (substitua pelo ID real)
        os = OrdemServico.query.filter_by(codigo='OS00350').first()
        
        if not os:
            print("❌ OS OS00350 não encontrada. Crie uma OS primeiro.")
            return
            
        print(f"📋 OS encontrada: {os.codigo}")
        print(f"💰 Valor total: R$ {os.valor_total}")
        
        # Exemplo 1: Pagamento à vista
        print("\n🔥 EXEMPLO 1: Pagamento à vista")
        lancamentos_avista = gerar_lancamentos_financeiro(
            os=os,
            forma_pagamento="PIX",
            valor_total=Decimal(str(os.valor_total)),
            parcelas=1
        )
        
        for lanc in lancamentos_avista:
            print(f"  💳 {lanc.descricao}")
            print(f"     Valor: R$ {lanc.valor}")
            print(f"     Vencimento: {lanc.data_vencimento}")
            print(f"     Status: {lanc.status}")
        
        # Exemplo 2: Parcelado com entrada
        print("\n🔥 EXEMPLO 2: Parcelado com entrada")
        valor_total = Decimal(str(os.valor_total))
        valor_entrada = valor_total * Decimal("0.3")  # 30% de entrada
        
        lancamentos_parcelado = gerar_lancamentos_financeiro(
            os=os,
            forma_pagamento="Cartão",
            valor_total=valor_total,
            parcelas=4,
            entrada=valor_entrada
        )
        
        for lanc in lancamentos_parcelado:
            tipo = "Entrada" if lanc.parcela == 0 else f"Parcela {lanc.parcela}/{lanc.total_parcelas}"
            print(f"  💳 {tipo}")
            print(f"     Valor: R$ {lanc.valor}")
            print(f"     Vencimento: {lanc.data_vencimento}")
            print(f"     Status: {lanc.status}")
        
        # Exemplo 3: Cronograma personalizado
        print("\n🔥 EXEMPLO 3: Cronograma personalizado")
        
        # Cronograma: 40% hoje, 30% em 15 dias, 30% em 30 dias
        schedule_custom = [
            (valor_total * Decimal("0.4"), date.today()),
            (valor_total * Decimal("0.3"), date.today() + timedelta(days=15)),
            (valor_total * Decimal("0.3"), date.today() + timedelta(days=30))
        ]
        
        lancamentos_custom = gerar_lancamentos_financeiro(
            os=os,
            forma_pagamento="Boleto",
            valor_total=valor_total,
            schedule_custom=schedule_custom
        )
        
        for i, lanc in enumerate(lancamentos_custom, 1):
            print(f"  💳 Parcela personalizada {i}")
            print(f"     Valor: R$ {lanc.valor}")
            print(f"     Vencimento: {lanc.data_vencimento}")
            print(f"     Status: {lanc.status}")
        
        print("\n✅ Exemplos executados com sucesso!")
        print("🔄 A função é idempotente - executar novamente substituirá os lançamentos")

if __name__ == "__main__":
    exemplo_uso()
