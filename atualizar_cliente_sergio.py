"""
Script para atualizar manualmente o cliente Sergio Yoshio Fujiwara para ativo
"""

from app.app import app
from app.extensoes import db
from app.cliente.cliente_model import Cliente
import sys

def atualizar_cliente():
    try:
        with app.app_context():
            # Verificar se o cliente existe
            cliente = Cliente.query.filter(Cliente.nome.ilike("%Sergio%Yoshio%Fujiwara%")).first() or \
                      Cliente.query.filter(Cliente.cpf_cnpj == "07714278838").first() or \
                      Cliente.query.get(2)  # ID baseado na captura de tela (CL10001)
            
            if cliente:
                print(f"Cliente encontrado: {cliente.nome} (ID: {cliente.id})")
                print(f"Status atual: {'Ativo' if cliente.ativo else 'Inativo'}")
                
                # Atualizar para ativo
                cliente.ativo = True
                db.session.commit()
                
                print(f"Status atualizado para: Ativo")
                return True
            else:
                print("Cliente Sergio Yoshio Fujiwara não encontrado no banco de dados local.")
                
                # Tentar criar o cliente com base nas informações da captura de tela
                novo_cliente = Cliente(
                    codigo="CL10001",
                    nome="Sergio Yoshio Fujiwara",
                    cpf_cnpj="07714278838",
                    telefone="(15) 97754-571",
                    email="sfujivara@uol.com.br",
                    cidade="Capão Bonito",
                    uf="SP",
                    ativo=True
                )
                
                db.session.add(novo_cliente)
                db.session.commit()
                
                print(f"Novo cliente criado com ID: {novo_cliente.id}")
                return True
    except Exception as e:
        print(f"Erro: {str(e)}")
        return False

if __name__ == "__main__":
    print("Atualizando cliente Sergio Yoshio Fujiwara...")
    if atualizar_cliente():
        print("Operação concluída com sucesso!")
    else:
        print("Falha na operação.")
        sys.exit(1)
