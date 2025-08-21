#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os as sistema

def verificar_banco():
    db_path = sistema.path.join(sistema.path.dirname(__file__), 'database', 'database.db')
    
    if not sistema.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado em: {db_path}")
        return
    
    print(f"✅ Banco encontrado: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estrutura da tabela ordens_servico
        cursor.execute("PRAGMA table_info(ordens_servico)")
        colunas = cursor.fetchall()
        
        print("\n📋 Estrutura da tabela ordens_servico:")
        for coluna in colunas:
            print(f"  - {coluna[1]} ({coluna[2]})")
        
        # Contar OS existentes
        cursor.execute("SELECT COUNT(*) FROM ordens_servico WHERE ativo = 1")
        total_os = cursor.fetchone()[0]
        print(f"\n📊 Total de OS ativas: {total_os}")
        
        # Listar últimas OS
        cursor.execute("""
            SELECT id, codigo, cliente_id, status, data_emissao, valor_total 
            FROM ordens_servico 
            WHERE ativo = 1 
            ORDER BY id DESC 
            LIMIT 5
        """)
        
        oss = cursor.fetchall()
        
        print("\n📄 Últimas OS:")
        for os in oss:
            print(f"  ID: {os[0]} | Código: {os[1]} | Cliente: {os[2]} | Status: {os[3]} | Valor: R$ {os[5] or 0:.2f}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")

if __name__ == "__main__":
    verificar_banco()
