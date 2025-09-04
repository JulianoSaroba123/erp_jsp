"""
Este é um script de one-liner que pode ser executado diretamente no console do Render.
Copie e cole esta linha no console web do Render para corrigir o problema.
"""

from app.app import app; from app.extensoes import db; from app.cliente.cliente_model import Cliente; app.app_context().push(); cliente = Cliente.query.filter((Cliente.nome.like('%Sergio%Yoshio%')) | (Cliente.cpf_cnpj == '07714278838') | (Cliente.codigo == 'CL10001')).first(); print(f'Cliente encontrado: {cliente.nome if cliente else "Não encontrado"}'); print(f'Status atual: {"Ativo" if cliente and cliente.ativo else "Inativo"}' if cliente else ''); cliente.ativo = True if cliente else None; db.session.commit() if cliente else None; print('Status atualizado para: Ativo' if cliente else 'Cliente não encontrado')
