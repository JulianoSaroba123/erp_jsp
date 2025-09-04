#!/usr/bin/env python3
"""
Script para corrigir clientes inativos no ambiente Render.
Este script deve ser executado no ambiente do Render.
"""

from app.app import app
from app.extensoes import db
from app.cliente.cliente_model import Cliente
from sqlalchemy import text

def corrigir_clientes():
    """Corrige todos os clientes para estarem ativos e com país Brasil"""
    with app.app_context():
        print("=== CORREÇÃO DE CLIENTES NO RENDER ===")
        
        try:
            # Corrigir clientes inativos
            clientes_inativos = Cliente.query.filter(Cliente.ativo == False).all()
            print(f"Encontrados {len(clientes_inativos)} clientes inativos")
            
            # Mostrar detalhes de clientes inativos
            for cliente in clientes_inativos:
                print(f"- Cliente: {cliente.nome} (ID: {cliente.id}, Código: {cliente.codigo})")
            
            # Atualizar todos para ativos
            resultado = db.session.execute(
                text("UPDATE clientes SET ativo = TRUE WHERE ativo = FALSE OR ativo IS NULL")
            )
            db.session.commit()
            print(f"✅ {resultado.rowcount} clientes atualizados para ATIVO")
            
            # Corrigir clientes sem país
            resultado_pais = db.session.execute(
                text("UPDATE clientes SET pais = 'Brasil' WHERE pais IS NULL OR pais = ''")
            )
            db.session.commit()
            print(f"✅ {resultado_pais.rowcount} clientes atualizados com país Brasil")
            
            # Verificar situação após correção
            total = Cliente.query.count()
            ativos = Cliente.query.filter(Cliente.ativo == True).count()
            inativos = Cliente.query.filter(Cliente.ativo == False).count()
            
            print("\n=== SITUAÇÃO APÓS CORREÇÃO ===")
            print(f"Total de clientes: {total}")
            print(f"Clientes ativos: {ativos}")
            print(f"Clientes inativos: {inativos}")
            
            # Verificar país
            sem_pais = Cliente.query.filter((Cliente.pais == None) | (Cliente.pais == '')).count()
            print(f"Clientes sem país: {sem_pais}")
            
            if inativos == 0 and sem_pais == 0:
                print("\n✅ CORREÇÃO CONCLUÍDA COM SUCESSO!")
            else:
                print("\n⚠️ Ainda existem problemas a corrigir.")
                
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    print("Iniciando correção de clientes...")
    corrigir_clientes()
