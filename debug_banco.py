#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def verificar_tabelas():
    db_path = 'database/database.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()
        
        print("📋 Tabelas existentes no banco:")
        for tabela in tabelas:
            print(f"  - {tabela[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")

if __name__ == "__main__":
    verificar_tabelas()
