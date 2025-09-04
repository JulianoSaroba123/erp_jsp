"""
Script simplificado para corrigir o status do cliente Sergio Yoshio Fujiwara no Render.
Este script é especificamente focado em resolver apenas esse problema.
"""

from app.app import app
from app.cliente.cliente_model import Cliente
from app.extensoes import db

def corrigir_cliente_inativo():
    """Função para corrigir o status do cliente"""
    try:
        with app.app_context():
            # Verificar o banco de dados
            print("Conectando ao banco de dados...")
            
            # Tentar encontrar o cliente por CPF/CNPJ (conforme mostrado na screenshot)
            cliente = Cliente.query.filter_by(cpf_cnpj="07714278838").first()
            
            if not cliente:
                # Tentar por ID ou código (CL10001 na screenshot)
                cliente = Cliente.query.filter_by(codigo="CL10001").first()
            
            if not cliente:
                # Tentar pelo nome
                cliente = Cliente.query.filter(Cliente.nome.contains("Sergio")).filter(Cliente.nome.contains("Yoshio")).filter(Cliente.nome.contains("Fujiwara")).first()
            
            if cliente:
                print(f"Cliente encontrado: {cliente.nome}")
                print(f"Status atual: {'Ativo' if cliente.ativo else 'Inativo'}")
                
                # Atualizar para ativo
                if not cliente.ativo:
                    cliente.ativo = True
                    db.session.commit()
                    print(f"Status atualizado para: Ativo")
                else:
                    print("O cliente já está ativo. Nenhuma alteração necessária.")
                
                return True
            else:
                print("Cliente não encontrado no banco de dados.")
                print("Verifique se você está conectado ao banco correto.")
                return False
                
    except Exception as e:
        print(f"ERRO: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== CORREÇÃO DE CLIENTE INATIVO ===")
    if corrigir_cliente_inativo():
        print("Operação concluída com sucesso!")
    else:
        print("A operação falhou. Verifique os erros acima.")
