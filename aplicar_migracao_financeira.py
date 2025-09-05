#!/usr/bin/env python3
"""
Script para aplicar migração de lançamentos financeiros
"""

import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app.app import app
from app.extensoes import db

def aplicar_migracao():
    """Aplica a migração para criar as tabelas financeiras"""
    with app.app_context():
        print("=== APLICANDO MIGRAÇÃO FINANCEIRA ===")
        
        try:
            # Importar modelos para garantir que sejam registrados
            from app.financeiro.lancamento_os_model import LancamentoFinanceiroOS
            from app.ordem_servico.os_model import OrdemServico
            
            # Verificar se a tabela já existe
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'financeiro_lancamentos_os' in existing_tables:
                print("✅ Tabela 'financeiro_lancamentos_os' já existe!")
            else:
                print("⚠️  Tabela 'financeiro_lancamentos_os' não encontrada.")
                print("🔨 Criando estrutura das tabelas...")
                
                # Criar todas as tabelas
                db.create_all()
                print("✅ Estrutura das tabelas criada com sucesso!")
            
            # Verificar se os campos foram adicionados à OS
            os_columns = [column['name'] for column in inspector.get_columns('ordens_servico')]
            
            novos_campos = ['condicao_pagamento', 'qtd_parcelas', 'valor_entrada', 'status_pagamento', 'schedule_json']
            campos_faltando = [campo for campo in novos_campos if campo not in os_columns]
            
            if campos_faltando:
                print(f"⚠️  Campos faltando na tabela 'ordens_servico': {campos_faltando}")
                print("💡 Execute: 'alembic upgrade head' para aplicar todas as migrações")
            else:
                print("✅ Todos os campos necessários estão presentes na tabela 'ordens_servico'!")
                
            print("\n🎯 Migração aplicada com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao aplicar migração: {str(e)}")
            return False
            
        return True

if __name__ == "__main__":
    sucesso = aplicar_migracao()
    if not sucesso:
        sys.exit(1)
