"""
Script para corrigir clientes inativos no Render
Arquivo: corrigir_render.py

Este script deve ser executado diretamente no ambiente Render para
corrigir o problema de clientes inativos.
"""

from app.app import app
from app.extensoes import db
from app.cliente.cliente_model import Cliente

def corrigir_clientes():
    print("Iniciando correção de clientes no Render...")
    
    with app.app_context():
        # Verificar estado atual
        total = Cliente.query.count()
        ativos = Cliente.query.filter_by(ativo=True).count()
        inativos = Cliente.query.filter_by(ativo=False).count()
        
        print(f"Estado inicial: {total} clientes | {ativos} ativos | {inativos} inativos")
        
        # Listar clientes inativos
        if inativos > 0:
            print("\nClientes inativos antes da correção:")
            for cliente in Cliente.query.filter_by(ativo=False).all():
                print(f"- {cliente.id}: {cliente.nome}")
            
            # Corrigir clientes inativos
            for cliente in Cliente.query.filter_by(ativo=False).all():
                cliente.ativo = True
                print(f"Corrigindo: {cliente.nome} -> Ativo=True")
            
            # Salvar alterações
            db.session.commit()
            print("\nAlterações salvas com sucesso!")
        else:
            print("Não foram encontrados clientes inativos.")
        
        # Verificar clientes sem país
        sem_pais = Cliente.query.filter((Cliente.pais == '') | (Cliente.pais.is_(None))).count()
        if sem_pais > 0:
            print(f"\nEncontrados {sem_pais} clientes sem país definido. Corrigindo...")
            for cliente in Cliente.query.filter((Cliente.pais == '') | (Cliente.pais.is_(None))).all():
                cliente.pais = "Brasil"
                print(f"Definindo país para {cliente.nome} -> 'Brasil'")
            
            # Salvar alterações
            db.session.commit()
            print("Países atualizados com sucesso!")
        
        # Verificar estado final
        ativos_final = Cliente.query.filter_by(ativo=True).count()
        inativos_final = Cliente.query.filter_by(ativo=False).count()
        
        print(f"\nEstado final: {total} clientes | {ativos_final} ativos | {inativos_final} inativos")

if __name__ == "__main__":
    corrigir_clientes()
