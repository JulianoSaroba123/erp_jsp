#!/usr/bin/env python3
"""
Script para criar tabelas de condições de pagamento e parcelas
"""

import sys
import os

# Adicionar o diretório app ao path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app'))

from app import app
from extensoes import db

def criar_tabelas_pagamento():
    """Cria tabelas para condições de pagamento e parcelas"""
    
    with app.app_context():
        try:
            print("🔧 Criando tabelas de pagamento...")
            
            # Criar tabela de condições de pagamento
            create_condicoes_sql = """
            CREATE TABLE IF NOT EXISTS condicoes_pagamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL,
                descricao TEXT,
                tipo VARCHAR(20) NOT NULL,
                numero_parcelas INTEGER DEFAULT 1,
                dias_primeira_parcela INTEGER DEFAULT 0,
                intervalo_parcelas INTEGER DEFAULT 30,
                ativo BOOLEAN DEFAULT 1,
                data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Criar tabela de parcelas da OS
            create_parcelas_sql = """
            CREATE TABLE IF NOT EXISTS os_parcelas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ordem_servico_id INTEGER NOT NULL,
                numero_parcela INTEGER NOT NULL,
                valor_parcela FLOAT NOT NULL,
                data_vencimento DATE NOT NULL,
                status VARCHAR(20) DEFAULT 'Pendente',
                data_pagamento DATE,
                valor_pago FLOAT,
                forma_pagamento VARCHAR(50),
                FOREIGN KEY (ordem_servico_id) REFERENCES ordens_servico (id)
            )
            """
            
            db.engine.execute(create_condicoes_sql)
            print("✅ Tabela condicoes_pagamento criada")
            
            db.engine.execute(create_parcelas_sql)
            print("✅ Tabela os_parcelas criada")
            
            # Inserir condições padrão
            insert_condicoes_sql = """
            INSERT OR IGNORE INTO condicoes_pagamento (nome, tipo, numero_parcelas, dias_primeira_parcela)
            VALUES 
                ('À Vista', 'avista', 1, 0),
                ('30 dias', 'prazo', 1, 30),
                ('2x sem juros', 'parcelado', 2, 30),
                ('3x sem juros', 'parcelado', 3, 30)
            """
            
            db.engine.execute(insert_condicoes_sql)
            print("✅ Condições padrão inseridas")
            
            db.session.commit()
            print("\n✅ Tabelas de pagamento criadas com sucesso!")
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    criar_tabelas_pagamento()
