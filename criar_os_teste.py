#!/usr/bin/env python3
"""
Script para criar uma ordem de serviço de teste
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar app diretamente
from app.app import app
from app.extensoes import db
from app.ordem_servico.os_model import OrdemServico
from app.cliente.cliente_model import Cliente
from datetime import datetime, date
import json

def criar_os_teste():
    with app.app_context():
        try:
            # Verificar se já existe cliente de teste
            cliente = Cliente.query.filter_by(nome='Cliente Teste JSP').first()
            if not cliente:
                # Criar cliente de teste
                cliente = Cliente(
                    nome='Cliente Teste JSP',
                    cpf_cnpj='123.456.789-10',
                    telefone='(15) 99999-9999',
                    email='teste@jsp.com.br',
                    endereco='Rua Teste, 123 - Tiete/SP',
                    ativo=True
                )
                db.session.add(cliente)
                db.session.flush()  # Para obter o ID
                
            # Dados dos serviços (JSON)
            servicos_dados = [
                {
                    "nome": "Instalação Elétrica Residencial",
                    "quantidade": 8.0,
                    "valor_total": 800.0
                },
                {
                    "nome": "Manutenção Preventiva",
                    "quantidade": 4.0,
                    "valor_total": 400.0
                }
            ]
            
            # Dados dos produtos (JSON)
            produtos_dados = [
                {
                    "nome": "Disjuntor 25A",
                    "quantidade": 2,
                    "valor_unitario": 35.0,
                    "valor_total": 70.0
                },
                {
                    "nome": "Cabo Flexível 2,5mm",
                    "quantidade": 100,
                    "valor_unitario": 2.5,
                    "valor_total": 250.0
                }
            ]
            
            # Criar OS de teste
            os_teste = OrdemServico(
                codigo='OS0001',
                cliente_id=cliente.id,
                status='Concluída',
                prioridade='Normal',
                tipo_servico='Instalação',
                solicitante='João Silva',
                contato='(15) 99888-7777',
                data_emissao=date.today(),
                previsao_conclusao=date.today(),
                tecnico_responsavel='Juliano Saroba Pereira',
                equipamento_nome='Quadro Elétrico Principal',
                equipamento_marca='Schneider',
                equipamento_modelo='QDC-24',
                equipamento_numero_serie='SN123456789',
                problema_descrito='Necessário instalação de novo quadro elétrico e adequação da instalação conforme normas técnicas.',
                descricao_servico_realizado='Realizada instalação completa do quadro elétrico, substituição de fiação antiga, instalação de DPS e adequação às normas NBR 5410.',
                hora_inicio=datetime.strptime('08:00', '%H:%M').time(),
                hora_termino=datetime.strptime('17:00', '%H:%M').time(),
                total_horas=8.0,
                valor_servicos=1200.0,
                valor_produtos=320.0,
                valor_total=1520.0,
                forma_pagamento='À Vista',
                condicoes_pagamento='À vista',
                servicos_dados=json.dumps(servicos_dados),
                produtos_dados=json.dumps(produtos_dados),
                ativo=True
            )
            
            db.session.add(os_teste)
            db.session.commit()
            
            print(f"✅ Ordem de Serviço '{os_teste.codigo}' criada com sucesso!")
            print(f"   Cliente: {cliente.nome}")
            print(f"   Valor Total: R$ {os_teste.valor_total:.2f}")
            print(f"   ID da OS: {os_teste.id}")
            print(f"\n📋 Acesse:")
            print(f"   Visualizar: http://127.0.0.1:5000/os/{os_teste.id}/visualizar")
            print(f"   Relatório: http://127.0.0.1:5000/os/{os_teste.id}/relatorio")
            print(f"   PDF: http://127.0.0.1:5000/os/{os_teste.id}/pdf")
            
            return os_teste.id
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao criar OS de teste: {e}")
            import traceback
            traceback.print_exc()
            return None

if __name__ == '__main__':
    criar_os_teste()
