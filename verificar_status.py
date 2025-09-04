"""
Script para verificar e registrar o status dos clientes em um arquivo de log.
"""

import sys
from datetime import datetime

# Redirecionar saída para arquivo
log_file = "status_clientes.log"
sys.stdout = open(log_file, "w")

print(f"=== Verificação de status dos clientes - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

try:
    from app.app import app
    from app.extensoes import db
    from app.cliente.cliente_model import Cliente

    with app.app_context():
        # Contar clientes
        total = Cliente.query.count()
        ativos = Cliente.query.filter_by(ativo=True).count()
        inativos = Cliente.query.filter_by(ativo=False).count()
        
        print(f"Total de clientes: {total}")
        print(f"Clientes ativos: {ativos}")
        print(f"Clientes inativos: {inativos}")
        
        # Listar clientes inativos se existirem
        if inativos > 0:
            print("\nClientes inativos:")
            for cliente in Cliente.query.filter_by(ativo=False).all():
                print(f"- ID: {cliente.id}, Nome: {cliente.nome}, CPF/CNPJ: {cliente.cpf_cnpj}")
        
        # Verificar cliente específico (Sergio Yoshio Fujiwara)
        cliente_sergio = Cliente.query.filter(Cliente.nome.like("%Sergio%Yoshio%Fujiwara%")).first()
        if cliente_sergio:
            print(f"\nStatus do cliente Sergio Yoshio Fujiwara:")
            print(f"- ID: {cliente_sergio.id}")
            print(f"- Nome: {cliente_sergio.nome}")
            print(f"- Ativo: {cliente_sergio.ativo}")
        else:
            print("\nCliente Sergio Yoshio Fujiwara não encontrado.")

except Exception as e:
    print(f"ERRO: {str(e)}")

# Restaurar saída padrão e fechar arquivo de log
sys.stdout.close()
sys.stdout = sys.__stdout__

print(f"Verificação concluída. Log salvo em {log_file}")
