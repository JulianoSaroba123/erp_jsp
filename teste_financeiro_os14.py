#!/usr/bin/env python3
"""
Teste para verificar e corrigir a integração financeira da OS0014
"""

import sys
import os
sys.path.append('.')

from app.app import create_app
from app.ordem_servico.os_model import OrdemServico
from app.financeiro.financeiro_model import LancamentoFinanceiro
from extensoes import db
import json
from datetime import datetime

def main():
    app = create_app()
    
    with app.app_context():
        print("=== TESTE INTEGRAÇÃO FINANCEIRA OS0014 ===")
        print()
        
        # Buscar a OS0014
        os = OrdemServico.query.filter_by(codigo='OS0014').first()
        if not os:
            print("❌ OS0014 não encontrada!")
            return
        
        print(f"✅ OS encontrada:")
        print(f"   Código: {os.codigo}")
        print(f"   Status: {os.status}")
        print(f"   Valor Total: R$ {os.valor_total}")
        print(f"   Cliente: {os.cliente.nome if os.cliente else 'N/A'}")
        print(f"   Parcelas JSON: {os.parcelas_json[:100] if os.parcelas_json else 'Nenhuma'}")
        print()
        
        # Verificar lançamentos existentes
        lancamentos_existentes = LancamentoFinanceiro.query.filter(
            LancamentoFinanceiro.descricao.like(f'%{os.codigo}%')
        ).all()
        
        print(f"📊 Lançamentos existentes: {len(lancamentos_existentes)}")
        for lanc in lancamentos_existentes:
            print(f"   - {lanc.descricao}: R$ {lanc.valor:.2f} ({lanc.data})")
        print()
        
        # Se não tem lançamentos e está concluída, criar
        if len(lancamentos_existentes) == 0:
            print("🔧 Criando lançamentos financeiros...")
            
            try:
                # Verificar se tem parcelas
                parcelas = []
                if os.parcelas_json:
                    try:
                        parcelas = json.loads(os.parcelas_json)
                        print(f"   Parcelas encontradas: {len(parcelas)}")
                    except Exception as e:
                        print(f"   ⚠️ Erro ao parsear parcelas: {e}")
                
                if parcelas and len(parcelas) > 0:
                    # Criar lançamento para cada parcela
                    for i, parcela in enumerate(parcelas):
                        valor = float(parcela.get('valor', 0))
                        data_venc = parcela.get('data_vencimento') or parcela.get('vencimento')
                        
                        # Converter data
                        if isinstance(data_venc, str) and '-' in data_venc:
                            data_venc = datetime.strptime(data_venc.split('T')[0], '%Y-%m-%d').date()
                        else:
                            data_venc = datetime.today().date()
                        
                        lancamento = LancamentoFinanceiro(
                            tipo='Receita',
                            categoria='Serviços',
                            descricao=f'{os.codigo} - Parcela {i+1}/{len(parcelas)} - {os.cliente.nome if os.cliente else "Cliente"}',
                            valor=valor,
                            data=data_venc,
                            status='Pendente',
                            observacoes=f'Gerado automaticamente da {os.codigo}'
                        )
                        db.session.add(lancamento)
                        print(f"   ✅ Parcela {i+1}: R$ {valor:.2f} para {data_venc}")
                else:
                    # Criar lançamento à vista
                    valor_total = float(os.valor_total or 0)
                    lancamento = LancamentoFinanceiro(
                        tipo='Receita',
                        categoria='Serviços',
                        descricao=f'{os.codigo} - À Vista - {os.cliente.nome if os.cliente else "Cliente"}',
                        valor=valor_total,
                        data=datetime.today().date(),
                        status='Pendente',
                        observacoes=f'Gerado automaticamente da {os.codigo}'
                    )
                    db.session.add(lancamento)
                    print(f"   ✅ À vista: R$ {valor_total:.2f}")
                
                # Salvar no banco
                db.session.commit()
                print("   💾 Lançamentos salvos com sucesso!")
                
                # Verificar novamente
                novos_lancamentos = LancamentoFinanceiro.query.filter(
                    LancamentoFinanceiro.descricao.like(f'%{os.codigo}%')
                ).all()
                print(f"   📊 Total de lançamentos criados: {len(novos_lancamentos)}")
                
            except Exception as e:
                print(f"   ❌ Erro ao criar lançamentos: {e}")
                import traceback
                print(f"   📝 Traceback: {traceback.format_exc()}")
                db.session.rollback()
        else:
            print("ℹ️ Lançamentos já existem, nada a fazer.")
        
        print()
        print("=== TESTE CONCLUÍDO ===")

if __name__ == '__main__':
    main()
